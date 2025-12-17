"""
Test script to validate ESPN API for NFL defensive statistics.
Run this locally before building Lambda functions.

Usage: python scripts/test_espn_scraper.py
"""

import requests
import json
from datetime import datetime

def get_current_nfl_week():
    """
    Estimate current NFL week based on date.
    For testing, we'll use a recent completed week.
    """
    # For now, return Week 14 (completed)
    return 14

def get_defensive_stats_espn(season=2024, week=None):
    """
    Fetch defensive statistics from ESPN's API.
    
    Args:
        season (int): NFL season year
        week (int): NFL week number (None for season totals)
    
    Returns:
        dict: Defensive statistics data
    """
    # ESPN's site API endpoint
    # This endpoint provides player statistics
    base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
    
    # Try the statistics endpoint
    stats_url = f"{base_url}/statistics"
    
    print(f"🔍 Fetching data from ESPN API...")
    print(f"   URL: {stats_url}")
    
    try:
        response = requests.get(stats_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Successfully fetched data")
        
        # Save raw response for inspection
        with open('espn_api_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"📝 Raw API response saved to: espn_api_response.json")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def parse_leaders_from_html():
    """
    Alternative: Parse the HTML stats page if API doesn't work.
    We know from web_fetch that tackles and sacks are displayed.
    """
    from bs4 import BeautifulSoup
    
    url = "https://www.espn.com/nfl/stats/_/season/2024/seasontype/2"
    
    print(f"\n🔍 Fetching data from ESPN stats page...")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the defensive leaders section
        # Based on the HTML structure we saw
        print(f"✅ Successfully fetched page (length: {len(response.text)} chars)")
        
        # Look for tackles table
        tackles_section = soup.find('table', {'class': 'Table'})
        
        if tackles_section:
            print("✅ Found statistics tables")
        else:
            print("⚠️  Could not find statistics tables - may need to adjust parsing")
        
        return soup
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("ESPN NFL Defensive Stats - API Test")
    print("=" * 60)
    print()
    
    # Test 1: Try ESPN API
    print("TEST 1: ESPN Site API")
    print("-" * 60)
    api_data = get_defensive_stats_espn()
    
    if api_data:
        print("\n✅ API Test Successful!")
        print("   Next step: Parse JSON structure to extract tackle/sack leaders")
    else:
        print("\n⚠️  API approach may need refinement")
    
    print("\n")
    
    # Test 2: HTML Parsing fallback
    print("TEST 2: HTML Parsing (Fallback)")
    print("-" * 60)
    html_data = parse_leaders_from_html()
    
    if html_data:
        print("\n✅ HTML fetch successful!")
        print("   We can parse this if API doesn't provide what we need")
    
    print("\n")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    
    if api_data or html_data:
        print("✅ Data source validated!")
        print()
        print("Next steps:")
        print("1. Inspect espn_api_response.json to understand structure")
        print("2. Build parsing logic based on actual data format")
        print("3. Proceed with Lambda function development")
    else:
        print("❌ Could not access data - check internet connection")
    
    print()

if __name__ == "__main__":
    main()