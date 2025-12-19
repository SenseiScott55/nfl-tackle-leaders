"""
NFL Tackle Leaders - Ingest Lambda Handler
Fetches weekly leaders from ESPN Core API and stores in DynamoDB
"""
from decimal import Decimal
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import boto3
import requests

# Configure logging
logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Environment variables
TABLE_NAME = os.environ['TABLE_NAME']
CURRENT_SEASON = os.environ['CURRENT_SEASON']
ESPN_API_BASE_URL = os.environ['ESPN_API_BASE_URL']

# AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Main Lambda handler - fetches ESPN data and stores in DynamoDB
    
    Args:
        event: Lambda event (can contain optional 'week' parameter)
        context: Lambda context
    
    Returns:
        dict: Response with status and data
    """
    try:
        logger.info("Starting NFL leaders ingest")
        logger.info(f"Event: {json.dumps(event)}")
        
        # Get week number (from event or auto-detect)
        week_number = event.get('week') if event else None
        
        # Fetch leaders from ESPN
        leaders_data = fetch_espn_leaders()
        
        if not leaders_data:
            raise Exception("Failed to fetch leaders data from ESPN")
        
        # Extract tackle leader
        tackles_leader = extract_stat_leader(leaders_data, 'totalTackles')
        
        # Extract sacks leader
        sacks_leader = extract_stat_leader(leaders_data, 'sacks')
        
        if not tackles_leader or not sacks_leader:
            raise Exception("Failed to extract leaders from ESPN data")
        
        # Store both leaders in DynamoDB
        results = []
        
        # Store tackles leader
        tackles_result = store_leader(
            season=CURRENT_SEASON,
            week=week_number,
            stat_type='TOTAL_TACKLES',
            leader_data=tackles_leader
        )
        results.append(tackles_result)
        
        # Store sacks leader
        sacks_result = store_leader(
            season=CURRENT_SEASON,
            week=week_number,
            stat_type='SACKS',
            leader_data=sacks_leader
        )
        results.append(sacks_result)
        
        logger.info(f"Successfully stored {len(results)} leaders")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully ingested NFL leaders',
                'season': CURRENT_SEASON,
                'week': week_number,
                'leaders': results
            })
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


def fetch_espn_leaders() -> Optional[Dict[str, Any]]:
    """
    Fetch season leaders from ESPN Core API
    
    Returns:
        dict: Leaders data from ESPN or None if failed
    """
    url = f"{ESPN_API_BASE_URL}/seasons/{CURRENT_SEASON}/types/2/leaders"
    
    logger.info(f"Fetching leaders from: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Successfully fetched leaders data")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from ESPN: {str(e)}")
        return None


def extract_stat_leader(data: Dict[str, Any], stat_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract the leader for a specific stat from ESPN data
    
    Args:
        data: ESPN API response data
        stat_name: Name of stat (e.g., 'totalTackles', 'sacks')
    
    Returns:
        dict: Leader information or None if not found
    """
    try:
        categories = data.get('categories', [])
        
        for category in categories:
            if category.get('name') == stat_name:
                leaders = category.get('leaders', [])
                
                if not leaders:
                    logger.warning(f"No leaders found for {stat_name}")
                    return None
                
                leader = leaders[0]  # Top leader
                
                # Fetch athlete details
                athlete_ref = leader.get('athlete', {}).get('$ref')
                team_ref = leader.get('team', {}).get('$ref')
                
                if not athlete_ref or not team_ref:
                    logger.error(f"Missing refs for {stat_name} leader")
                    return None
                
                athlete_data = fetch_reference(athlete_ref)
                team_data = fetch_reference(team_ref)
                
                if not athlete_data or not team_data:
                    logger.error(f"Failed to fetch athlete/team data for {stat_name}")
                    return None
                
                return {
                    'stat_name': stat_name,
                    'stat_display_name': category.get('displayName'),
                    'value': leader.get('value'),
                    'display_value': leader.get('displayValue'),
                    'player_id': athlete_data.get('id'),
                    'player_name': athlete_data.get('displayName'),
                    'player_short_name': athlete_data.get('shortName'),
                    'team_id': team_data.get('id'),
                    'team_name': team_data.get('displayName'),
                    'team_abbreviation': team_data.get('abbreviation')
                }
        
        logger.warning(f"Stat {stat_name} not found in categories")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting {stat_name}: {str(e)}")
        return None


def fetch_reference(ref_url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch data from an ESPN reference URL
    
    Args:
        ref_url: ESPN API reference URL
    
    Returns:
        dict: Referenced data or None if failed
    """
    try:
        response = requests.get(ref_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching reference {ref_url}: {str(e)}")
        return None


def store_leader(season: str, week: Optional[int], stat_type: str, 
                leader_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store a leader in DynamoDB
    
    Args:
        season: NFL season (e.g., "2025")
        week: Week number (None for season total)
        stat_type: Type of stat (TOTAL_TACKLES or SACKS)
        leader_data: Leader information from ESPN
    
    Returns:
        dict: Stored item summary
    """
    # Determine week (use current week if not specified)
    if week is None:
        week = get_current_nfl_week()
    
    # Construct DynamoDB keys
    pk = f"SEASON#{season}"
    sk = f"WEEK#{week:02d}#STAT#{stat_type}"
    
    item = {
    'PK': pk,
    'SK': sk,
    'season': season,
    'week_number': week,
    'stat_type': stat_type,
    'stat_display_name': leader_data['stat_display_name'],
    'player_id': leader_data['player_id'],
    'player_name': leader_data['player_name'],
    'player_short_name': leader_data['player_short_name'],
    'team_id': leader_data['team_id'],
    'team_name': leader_data['team_name'],
    'team_abbreviation': leader_data['team_abbreviation'],
    'stat_value': Decimal(str(leader_data['value'])), # Store as Decimal for DynamoDB
    'stat_display_value': leader_data['display_value'],
    'updated_at': datetime.utcnow().isoformat() + 'Z'
}
    
    logger.info(f"Storing leader: {stat_type} - {leader_data['player_name']} ({leader_data['display_value']})")
    
    table.put_item(Item=item)
    
    return {
        'stat_type': stat_type,
        'player': leader_data['player_name'],
        'team': leader_data['team_abbreviation'],
        'value': leader_data['display_value']
    }


def get_current_nfl_week() -> int:
    """
    Estimate current NFL week based on date
    
    Returns:
        int: Estimated current week (1-18)
    """
    # Simple estimation: Week 1 starts ~first week of September
    # For production, you'd want a more robust calculation
    # For now, return Week 15 as default (mid-December)
    return 15


# For local testing
if __name__ == "__main__":
    # Mock event and context for testing
    test_event = {}
    test_context = {}
    
    result = lambda_handler(test_event, test_context)
    print(json.dumps(result, indent=2))