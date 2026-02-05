#!/usr/bin/env python3
"""
Test script for AI Operations Assistant
Run this after starting the server to verify functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

test_queries = [
    "Find top AI GitHub repositories and Bangalore weather",
    "Show me Python trending repos and Delhi weather",
    "Get machine learning projects on GitHub and Mumbai weather",
]

def test_endpoint(query):
    """Test a single query"""
    print(f"\n{'='*80}")
    print(f"Testing: {query}")
    print(f"{'='*80}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/run",
            params={"query": query},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Verified: {result.get('verified', False)}")
            print(f"✅ Data Sources: {result.get('data_sources', [])}")
            print(f"\n📊 Summary: {result.get('summary', 'N/A')}")
            
            if result.get('results', {}).get('github'):
                print(f"\n🔍 GitHub Results: {len(result['results']['github'])} repositories")
            
            if result.get('results', {}).get('weather'):
                weather = result['results']['weather']
                print(f"🌤️  Weather: {weather.get('city')} - {weather.get('temperature_c')}°C")
            
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the server running?")
        print("Start it with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("\n🚀 AI Operations Assistant - Test Suite")
    print("=" * 80)
    print("Make sure the server is running: uvicorn main:app --reload")
    print("=" * 80)
    
    time.sleep(2)
    
    results = []
    for query in test_queries:
        success = test_endpoint(query)
        results.append(success)
        time.sleep(1)
    
    print(f"\n{'='*80}")
    print("📈 Test Summary")
    print(f"{'='*80}")
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✅ All tests passed! System is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
