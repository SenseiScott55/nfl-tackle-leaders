"""
Extract and verify tackle/sack leaders from ESPN Core API
"""
import requests
import json

def get_leaders():
    """Get leaders from ESPN Core API"""
    url = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2025/types/2/leaders"
    
    print("🔍 Fetching leaders from ESPN Core API...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def get_athlete_details(athlete_ref):
    """Fetch athlete details from reference URL"""
    print(f"   Fetching athlete: {athlete_ref}")
    response = requests.get(athlete_ref, timeout=10)
    response.raise_for_status()
    return response.json()

def get_team_details(team_ref):
    """Fetch team details from reference URL"""
    response = requests.get(team_ref, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_stat_leader(data, stat_name):
    """Extract leader for a specific stat"""
    categories = data.get('categories', [])
    
    for category in categories:
        if category.get('name') == stat_name:
            leaders = category.get('leaders', [])
            if leaders and len(leaders) > 0:
                return {
                    'category': category,
                    'leader': leaders[0]  # Top leader
                }
    return None

def main():
    print("="*60)
    print("ESPN CORE API - Leader Extraction Test")
    print("="*60)
    print()
    
    # Get leaders data
    data = get_leaders()
    print("✅ Got leaders data")
    print()
    
    # Extract Total Tackles
    print("🎯 EXTRACTING TOTAL TACKLES LEADER:")
    print("-"*60)
    tackles_data = extract_stat_leader(data, 'totalTackles')
    
    if tackles_data:
        leader = tackles_data['leader']
        category = tackles_data['category']
        
        print(f"   Stat: {category['displayName']}")
        print(f"   Value: {leader['displayValue']} tackles")
        print()
        
        # Fetch athlete details
        athlete_ref = leader['athlete']['$ref']
        athlete = get_athlete_details(athlete_ref)
        
        # Fetch team details
        team_ref = leader['team']['$ref']
        team = get_team_details(team_ref)
        
        print(f"   ✅ TACKLE LEADER:")
        print(f"      Player: {athlete.get('displayName', 'Unknown')}")
        print(f"      Team: {team.get('abbreviation', 'Unknown')}")
        print(f"      Tackles: {leader['displayValue']}")
        print()
        
        # Save for inspection
        result = {
            'stat': 'totalTackles',
            'value': leader['value'],
            'display_value': leader['displayValue'],
            'athlete': {
                'id': athlete.get('id'),
                'name': athlete.get('displayName'),
                'shortName': athlete.get('shortName')
            },
            'team': {
                'id': team.get('id'),
                'name': team.get('displayName'),
                'abbreviation': team.get('abbreviation')
            }
        }
        
        with open('tackles_leader.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"   📝 Full data saved to: tackles_leader.json")
    else:
        print("   ❌ Could not find totalTackles")
    
    print()
    
    # Extract Sacks
    print("🎯 EXTRACTING SACKS LEADER:")
    print("-"*60)
    sacks_data = extract_stat_leader(data, 'sacks')
    
    if sacks_data:
        leader = sacks_data['leader']
        category = sacks_data['category']
        
        print(f"   Stat: {category['displayName']}")
        print(f"   Value: {leader['displayValue']} sacks")
        print()
        
        # Fetch athlete details
        athlete_ref = leader['athlete']['$ref']
        athlete = get_athlete_details(athlete_ref)
        
        # Fetch team details
        team_ref = leader['team']['$ref']
        team = get_team_details(team_ref)
        
        print(f"   ✅ SACKS LEADER:")
        print(f"      Player: {athlete.get('displayName', 'Unknown')}")
        print(f"      Team: {team.get('abbreviation', 'Unknown')}")
        print(f"      Sacks: {leader['displayValue']}")
        print()
        
        # Save for inspection
        result = {
            'stat': 'sacks',
            'value': leader['value'],
            'display_value': leader['displayValue'],
            'athlete': {
                'id': athlete.get('id'),
                'name': athlete.get('displayName'),
                'shortName': athlete.get('shortName')
            },
            'team': {
                'id': team.get('id'),
                'name': team.get('displayName'),
                'abbreviation': team.get('abbreviation')
            }
        }
        
        with open('sacks_leader.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"   📝 Full data saved to: sacks_leader.json")
    else:
        print("   ❌ Could not find sacks")
    
    print()
    print("="*60)
    print("VERIFICATION")
    print("="*60)
    print()
    print("Expected values (from ESPN website):")
    print("   - Tackles: ~142 (Jordyn Brooks)")
    print("   - Sacks: ~19+ (Myles Garrett)")
    print()
    
    if tackles_data and sacks_data:
        tackles_value = int(tackles_data['leader']['value'])
        sacks_value = float(sacks_data['leader']['value'])
        
        if tackles_value > 100:
            print("✅ Tackles value looks correct! (> 100)")
        else:
            print(f"⚠️  Tackles value ({tackles_value}) seems low")
        
        if sacks_value > 10:
            print("✅ Sacks value looks correct! (> 10)")
        else:
            print(f"⚠️  Sacks value ({sacks_value}) seems low")
        
        print()
        print("="*60)
        print("🎯 DECISION:")
        print("="*60)
        print()
        
        if tackles_value > 100 and sacks_value > 10:
            print("✅ ESPN CORE API HAS CORRECT DATA!")
            print()
            print("Implementation Plan:")
            print("   1. Call: /leaders endpoint")
            print("   2. Extract tackle & sack leader values")
            print("   3. Call athlete $ref URLs (2 calls)")
            print("   4. Call team $ref URLs (2 calls)")
            print("   5. Store in DynamoDB")
            print()
            print("   Total: 5 API calls per week")
            print("   All calls return JSON")
            print("   No authentication required")
            print()
            print("🚀 READY TO BUILD!")
        else:
            print("⚠️  Data still seems incomplete")
            print("   Consider alternative APIs")

if __name__ == "__main__":
    main()