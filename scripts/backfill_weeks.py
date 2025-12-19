"""
Backfill historical NFL leaders data into DynamoDB
Fetches data for all completed weeks of the current season
"""
import os
import sys
import json
import boto3
import requests
from decimal import Decimal
from datetime import datetime

# Configuration
TABLE_NAME = 'nfl_weekly_leaders'
CURRENT_SEASON = '2025'
ESPN_API_BASE_URL = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl'

# AWS client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def store_leader(table, season: str, week: int, stat_type: str, leader_data: dict):
    """
    Store a leader in DynamoDB
    
    Args:
        table: DynamoDB table resource
        season: NFL season
        week: Week number
        stat_type: Type of stat (TOTAL_TACKLES or SACKS)
        leader_data: Leader information
    """
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
        'stat_value': Decimal(str(leader_data['value'])),
        'stat_display_value': leader_data['display_value'],
        'updated_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    table.put_item(Item=item)


def fetch_leaders_for_week(season: str, week: int) -> dict:
    """
    Fetch leaders for a specific week
    
    Args:
        season: NFL season year
        week: Week number (1-18)
    
    Returns:
        dict: Leaders data or None if not available
    """
    print(f"\nFetching data for Week {week}...")
    
    # Fetch tackles leader
    tackles_url = f"{ESPN_API_BASE_URL}/seasons/{season}/types/2/weeks/{week}/leaders/6"
    sacks_url = f"{ESPN_API_BASE_URL}/seasons/{season}/types/2/weeks/{week}/leaders/8"
    
    leaders = {}
    
    try:
        # Fetch tackles
        print(f"  Fetching tackles from: {tackles_url}")
        tackles_response = requests.get(tackles_url, timeout=10)
        tackles_response.raise_for_status()
        tackles_data = tackles_response.json()
        
        if 'leaders' in tackles_data and tackles_data['leaders']:
            leaders['tackles'] = extract_leader_data(tackles_data, 'TOTAL_TACKLES', 'Total Tackles')
            print(f"  ✓ Found tackles leader: {leaders['tackles']['player_name']} - {leaders['tackles']['value']}")
        else:
            print(f"  ✗ No tackles data available for week {week}")
        
        # Fetch sacks
        print(f"  Fetching sacks from: {sacks_url}")
        sacks_response = requests.get(sacks_url, timeout=10)
        sacks_response.raise_for_status()
        sacks_data = sacks_response.json()
        
        if 'leaders' in sacks_data and sacks_data['leaders']:
            leaders['sacks'] = extract_leader_data(sacks_data, 'SACKS', 'Sacks')
            print(f"  ✓ Found sacks leader: {leaders['sacks']['player_name']} - {leaders['sacks']['value']}")
        else:
            print(f"  ✗ No sacks data available for week {week}")
        
        return leaders if leaders else None
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error fetching data for week {week}: {str(e)}")
        return None


def extract_leader_data(api_data: dict, stat_type: str, stat_display_name: str) -> dict:
    """
    Extract leader information from ESPN API response
    
    Args:
        api_data: Raw ESPN API response
        stat_type: Type of stat (TOTAL_TACKLES or SACKS)
        stat_display_name: Display name for the stat
    
    Returns:
        dict: Extracted leader data
    """
    leaders_list = api_data['leaders']
    
    if not leaders_list:
        return None
    
    # Get the first leader (highest stat)
    leader = leaders_list[0]
    athlete = leader['athlete']
    team = athlete['team']
    
    return {
        'stat_type': stat_type,
        'stat_display_name': stat_display_name,
        'player_id': athlete['id'],
        'player_name': athlete['displayName'],
        'player_short_name': athlete['shortName'],
        'team_id': team['id'],
        'team_name': team['name'],
        'team_abbreviation': team['abbreviation'],
        'value': leader['value'],
        'display_value': leader['displayValue']
    }


def backfill_season(season: str, start_week: int = 1, end_week: int = 15):
    """
    Backfill data for multiple weeks
    
    Args:
        season: NFL season year
        start_week: First week to backfill
        end_week: Last week to backfill
    """
    print(f"Starting backfill for {season} season, weeks {start_week}-{end_week}")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for week in range(start_week, end_week + 1):
        try:
            leaders = fetch_leaders_for_week(season, week)
            
            if not leaders:
                print(f"  ⚠ No data found for week {week}, skipping...")
                error_count += 1
                continue
            
            # Store each leader
            for stat_type, leader_data in leaders.items():
                if leader_data:
                    store_leader(
                        table=table,
                        season=season,
                        week=week,
                        stat_type=leader_data['stat_type'],
                        leader_data=leader_data
                    )
                    success_count += 1
            
            print(f"  ✓ Week {week} stored successfully")
            
        except Exception as e:
            print(f"  ✗ Error processing week {week}: {str(e)}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"Backfill complete!")
    print(f"  Successful: {success_count} records")
    print(f"  Errors: {error_count}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Backfill NFL leaders data')
    parser.add_argument('--season', default=CURRENT_SEASON, help='NFL season year')
    parser.add_argument('--start-week', type=int, default=1, help='Starting week')
    parser.add_argument('--end-week', type=int, default=15, help='Ending week')
    
    args = parser.parse_args()
    
    backfill_season(args.season, args.start_week, args.end_week)