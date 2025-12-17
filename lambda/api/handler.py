"""
NFL Tackle Leaders - API Lambda Handler
Serves data from DynamoDB via Lambda Function URL
"""
import json
import os
import logging
from typing import Dict, Any, List, Optional
import boto3
from boto3.dynamodb.conditions import Key

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Environment variables
TABLE_NAME = os.environ['TABLE_NAME']
CURRENT_SEASON = os.environ['CURRENT_SEASON']

# AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Main API handler - routes requests to appropriate functions
    
    Supports:
    - GET /current - Get current week leaders
    - GET /week/{week_number} - Get specific week leaders
    - GET /season - Get all weeks for season
    - GET /stat/{stat_type} - Get all weeks for a stat type
    
    Args:
        event: Lambda event (from Function URL)
        context: Lambda context
    
    Returns:
        dict: HTTP response
    """
    try:
        # Parse request
        http_method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
        raw_path = event.get('rawPath', '/')
        query_params = event.get('queryStringParameters') or {}
        
        logger.info(f"Request: {http_method} {raw_path}")
        logger.info(f"Query params: {query_params}")
        
        # Route based on path
        if raw_path == '/current' or raw_path == '/':
            return get_current_week_leaders()
        
        elif raw_path.startswith('/week/'):
            week_str = raw_path.split('/')[-1]
            try:
                week = int(week_str)
                return get_week_leaders(week)
            except ValueError:
                return error_response(400, f"Invalid week number: {week_str}")
        
        elif raw_path == '/season':
            return get_season_leaders()
        
        elif raw_path.startswith('/stat/'):
            stat_type = raw_path.split('/')[-1].upper()
            return get_stat_history(stat_type)
        
        elif raw_path == '/health':
            return success_response({'status': 'healthy'})
        
        else:
            return error_response(404, f"Endpoint not found: {raw_path}")
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
        return error_response(500, str(e))


def get_current_week_leaders() -> Dict[str, Any]:
    """
    Get leaders for the most recent week in the database
    
    Returns:
        dict: HTTP response with current week leaders
    """
    try:
        # Query all items for current season
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"SEASON#{CURRENT_SEASON}")
        )
        
        items = response.get('Items', [])
        
        if not items:
            return error_response(404, "No data found for current season")
        
        # Find the most recent week
        max_week = max(item['week_number'] for item in items)
        
        # Filter to just that week's leaders
        current_leaders = [
            item for item in items 
            if item['week_number'] == max_week
        ]
        
        return success_response({
            'season': CURRENT_SEASON,
            'week': max_week,
            'leaders': format_leaders(current_leaders)
        })
        
    except Exception as e:
        logger.error(f"Error getting current week: {str(e)}")
        return error_response(500, str(e))


def get_week_leaders(week: int) -> Dict[str, Any]:
    """
    Get leaders for a specific week
    
    Args:
        week: Week number (1-18)
    
    Returns:
        dict: HTTP response with week leaders
    """
    try:
        if week < 1 or week > 18:
            return error_response(400, "Week must be between 1 and 18")
        
        # Query for specific week
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"SEASON#{CURRENT_SEASON}") & 
                                  Key('SK').begins_with(f"WEEK#{week:02d}#")
        )
        
        items = response.get('Items', [])
        
        if not items:
            return error_response(404, f"No data found for week {week}")
        
        return success_response({
            'season': CURRENT_SEASON,
            'week': week,
            'leaders': format_leaders(items)
        })
        
    except Exception as e:
        logger.error(f"Error getting week {week}: {str(e)}")
        return error_response(500, str(e))


def get_season_leaders() -> Dict[str, Any]:
    """
    Get all leaders for entire season
    
    Returns:
        dict: HTTP response with all season data
    """
    try:
        # Query all items for current season
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"SEASON#{CURRENT_SEASON}")
        )
        
        items = response.get('Items', [])
        
        if not items:
            return error_response(404, "No data found for current season")
        
        # Group by week
        weeks_data = {}
        for item in items:
            week = item['week_number']
            if week not in weeks_data:
                weeks_data[week] = []
            weeks_data[week].append(item)
        
        # Format response
        season_data = [
            {
                'week': week,
                'leaders': format_leaders(leaders)
            }
            for week, leaders in sorted(weeks_data.items())
        ]
        
        return success_response({
            'season': CURRENT_SEASON,
            'total_weeks': len(weeks_data),
            'weeks': season_data
        })
        
    except Exception as e:
        logger.error(f"Error getting season data: {str(e)}")
        return error_response(500, str(e))


def get_stat_history(stat_type: str) -> Dict[str, Any]:
    """
    Get history for a specific stat across all weeks
    
    Args:
        stat_type: TOTAL_TACKLES or SACKS
    
    Returns:
        dict: HTTP response with stat history
    """
    try:
        valid_stats = ['TOTAL_TACKLES', 'SACKS']
        if stat_type not in valid_stats:
            return error_response(400, f"Invalid stat type. Must be: {', '.join(valid_stats)}")
        
        # Use GSI to query by stat_type
        response = table.query(
            IndexName='StatTypeIndex',
            KeyConditionExpression=Key('stat_type').eq(stat_type)
        )
        
        items = response.get('Items', [])
        
        if not items:
            return error_response(404, f"No data found for {stat_type}")
        
        # Sort by week
        items_sorted = sorted(items, key=lambda x: x['week_number'])
        
        return success_response({
            'season': CURRENT_SEASON,
            'stat_type': stat_type,
            'total_weeks': len(items_sorted),
            'history': [format_leader_item(item) for item in items_sorted]
        })
        
    except Exception as e:
        logger.error(f"Error getting stat history for {stat_type}: {str(e)}")
        return error_response(500, str(e))


def format_leaders(items: List[Dict]) -> List[Dict[str, Any]]:
    """
    Format leader items for API response
    
    Args:
        items: Raw DynamoDB items
    
    Returns:
        list: Formatted leader data
    """
    return [format_leader_item(item) for item in items]


def format_leader_item(item: Dict) -> Dict[str, Any]:
    """
    Format a single leader item
    
    Args:
        item: Raw DynamoDB item
    
    Returns:
        dict: Formatted leader
    """
    return {
        'stat_type': item['stat_type'],
        'stat_name': item['stat_display_name'],
        'player': {
            'id': item['player_id'],
            'name': item['player_name'],
            'short_name': item['player_short_name']
        },
        'team': {
            'id': item['team_id'],
            'name': item['team_name'],
            'abbreviation': item['team_abbreviation']
        },
        'value': item['stat_value'],
        'display_value': item['stat_display_value'],
        'updated_at': item['updated_at']
    }


def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a successful HTTP response
    
    Args:
        data: Response data
    
    Returns:
        dict: HTTP response
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }


def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Create an error HTTP response
    
    Args:
        status_code: HTTP status code
        message: Error message
    
    Returns:
        dict: HTTP response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': message
        })
    }


# For local testing
if __name__ == "__main__":
    # Mock event for testing
    test_event = {
        'requestContext': {
            'http': {
                'method': 'GET'
            }
        },
        'rawPath': '/current',
        'queryStringParameters': None
    }
    test_context = {}
    
    result = lambda_handler(test_event, test_context)
    print(json.dumps(result, indent=2))