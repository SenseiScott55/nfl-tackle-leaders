"""
Extract tackle and sack leaders from ESPN API response
"""
import json

def find_stat_leader(categories, stat_name):
    """
    Find the leader for a specific stat category.
    
    Args:
        categories (list): List of stat categories from ESPN API
        stat_name (str): Name of stat to find (e.g., 'totalTackles', 'sacks')
    
    Returns:
        dict: Leader info or None if not found
    """
    for category in categories:
        if category.get('name') == stat_name:
            leaders = category.get('leaders', [])
            if leaders and len(leaders) > 0:
                leader = leaders[0]  # First leader is #1
                return {
                    'stat_name': stat_name,
                    'display_name': category.get('displayName'),
                    'value': leader.get('value'),
                    'display_value': leader.get('displayValue'),
                    'athlete': {
                        'id': leader['athlete']['id'],
                        'name': leader['athlete']['displayName'],
                        'short_name': leader['athlete']['shortName']
                    },
                    'team': {
                        'id': leader['team']['id'],
                        'name': leader['team']['name'],
                        'abbreviation': leader['team']['abbreviation']
                    } if 'team' in leader else None
                }
    return None

def main():
    print("="*60)
    print("ESPN NFL Leaders Extraction Test")
    print("="*60)
    print()
    
    # Load the API response
    with open('espn_api_response.json', 'r') as f:
        data = json.load(f)
    
    categories = data.get('stats', {}).get('categories', [])
    print(f"📊 Found {len(categories)} stat categories")
    print()
    
    # List all available categories
    print("📋 Available stat categories:")
    print("-"*60)
    for i, cat in enumerate(categories[:20], 1):  # Show first 20
        print(f"   {i}. {cat.get('name')} - {cat.get('displayName')}")
    if len(categories) > 20:
        print(f"   ... and {len(categories) - 20} more")
    print()
    
    # Find Total Tackles leader
    print("🎯 TOTAL TACKLES LEADER:")
    print("-"*60)
    tackles_leader = find_stat_leader(categories, 'totalTackles')
    
    if tackles_leader:
        print(f"✅ Found!")
        print(f"   Player: {tackles_leader['athlete']['name']}")
        print(f"   Team: {tackles_leader['team']['abbreviation']}")
        print(f"   Total Tackles: {tackles_leader['display_value']}")
        print()
        print(f"   Full data:")
        print(f"   {json.dumps(tackles_leader, indent=4)}")
    else:
        print("❌ Not found - stat name might be different")
    
    print()
    
    # Find Sacks leader
    print("🎯 SACKS LEADER:")
    print("-"*60)
    sacks_leader = find_stat_leader(categories, 'sacks')
    
    if sacks_leader:
        print(f"✅ Found!")
        print(f"   Player: {sacks_leader['athlete']['name']}")
        print(f"   Team: {sacks_leader['team']['abbreviation']}")
        print(f"   Sacks: {sacks_leader['display_value']}")
        print()
        print(f"   Full data:")
        print(f"   {json.dumps(sacks_leader, indent=4)}")
    else:
        print("❌ Not found - stat name might be different")
    
    print()
    print("="*60)
    
    if tackles_leader and sacks_leader:
        print("✅ SUCCESS! Both stats found and extracted!")
        print()
        print("Next steps:")
        print("1. This parsing logic works for Lambda function")
        print("2. Start building Terraform modules")
        print("3. Implement Lambda with this exact code structure")
    else:
        print("⚠️  Need to check stat names")
        print("Review the 'Available stat categories' list above")
        print("to find the correct names for tackles/sacks")

if __name__ == "__main__":
    main()