"""
Test alternative NFL APIs for tackles and sacks data
"""
import requests
import json

def test_balldontlie():
    """Test BALLDONTLIE NFL API"""
    print("="*60)
    print("TEST 1: BALLDONTLIE NFL API")
    print("="*60)
    print()
    
    # Note: This requires an API key (free tier available)
    url = "https://api.balldontlie.io/nfl/v1/stats/teams?season=2025"
    
    print(f"📍 URL: {url}")
    print("⚠️  Note: Requires free API key from balldontlie.io")
    print("   Sign up at: https://www.balldontlie.io/")
    print()
    
    try:
        # Without API key, will get 401
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print("❌ Requires API key (expected)")
            print("✅ But endpoint exists and is accessible!")
            return "needs_key"
        
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Success!")
        with open('balldontlie_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        return data
        
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_espn_core_api():
    """Test ESPN Core API (different from site API)"""
    print("\n" + "="*60)
    print("TEST 2: ESPN CORE API")
    print("="*60)
    print()
    
    # Try different ESPN core endpoints
    endpoints = [
        "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2025/types/2/leaders",
        "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2025/types/2/statistics",
    ]
    
    for url in endpoints:
        print(f"📍 Testing: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"   ✅ Success! Got response")
            print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'list'}")
            
            filename = f"espn_core_{url.split('/')[-1]}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   📝 Saved to: {filename}")
            
            return data
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def test_mysportsfeeds():
    """Test MySportsFeeds API"""
    print("\n" + "="*60)
    print("TEST 3: MYSPORTSFEEDS API")
    print("="*60)
    print()
    
    url = "https://api.mysportsfeeds.com/v2.1/pull/nfl/2025-regular/player_stats_totals.json"
    
    print(f"📍 URL: {url}")
    print("⚠️  Note: Requires free account at mysportsfeeds.com")
    print("   After signup, use: username + password as auth")
    print()
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print("❌ Requires authentication (expected)")
            print("✅ But endpoint exists!")
            return "needs_auth"
        
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Success!")
        with open('mysportsfeeds_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        return data
        
    except Exception as e:
        print(f"   Error: {e}")
        return None

def main():
    print("\n🔍 TESTING ALTERNATIVE NFL APIs")
    print("="*60)
    print()
    
    results = {}
    
    # Test all APIs
    results['balldontlie'] = test_balldontlie()
    results['espn_core'] = test_espn_core_api()
    results['mysportsfeeds'] = test_mysportsfeeds()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY & RECOMMENDATIONS")
    print("="*60)
    print()
    
    if results['espn_core']:
        print("✅ BEST OPTION: ESPN Core API")
        print("   - No authentication required")
        print("   - Has 2025 season data")
        print("   - Just need to find right endpoint structure")
        print()
    
    if results['balldontlie'] == "needs_key":
        print("✅ GOOD OPTION: BALLDONTLIE")
        print("   - Free API key available")
        print("   - Clean JSON structure")
        print("   - Sign up at: https://www.balldontlie.io/")
        print()
    
    if results['mysportsfeeds'] == "needs_auth":
        print("✅ GOOD OPTION: MYSPORTSFEEDS")
        print("   - Free for personal use")
        print("   - Comprehensive data")
        print("   - Sign up at: https://www.mysportsfeeds.com/")
        print()
    
    print("🎯 NEXT STEPS:")
    print("-"*60)
    print("1. If ESPN Core API worked: Use that (no auth needed)")
    print("2. Otherwise: Sign up for BALLDONTLIE (easiest free option)")
    print("3. Fallback: MySportsFeeds (more comprehensive)")

if __name__ == "__main__":
    main()