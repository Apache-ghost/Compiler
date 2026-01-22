#!/usr/bin/env python3
"""
Test script for Flask web API endpoints
Tests language detection in all analysis modes
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, data, description):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", 
                                json=data, 
                                headers={'Content-Type': 'application/json'},
                                timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Expression: {data.get('expression', 'N/A')}")
            
            if 'languages_detected' in result:
                languages = result['languages_detected']
                print(f"✓ Languages Detected: {', '.join(languages) if languages else 'None'}")
                print(f"  → Count: {len(languages)}")
            else:
                print("✗ Languages not detected (missing in response)")
            
            if 'accepted' in result:
                status = "✓ ACCEPTED" if result['accepted'] else "✗ REJECTED"
                print(f"✓ Parse Status: {status}")
                if 'parse_result' in result:
                    print(f"  → {result['parse_result'][:80]}...")
            
            if 'token_count' in result:
                print(f"✓ Token Count: {result['token_count']}")
            
            return True, result
        else:
            print(f"✗ Status: {response.status_code}")
            print(f"✗ Error: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("✗ Connection Error: Flask server is not running!")
        print("  → Start the server with: python app.py")
        return False, None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False, None

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FLASK WEB API TEST SUITE")
    print("Testing Language Detection in All Endpoints")
    print("="*60)
    
    # Wait a moment for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    # Test cases with expected languages
    test_cases = [
        {
            "expression": "bros drop me for Total",
            "expected_languages": ["English", "Franc-Anglais"],
            "description": "English + Franc-Anglais"
        },
        {
            "expression": "ICT est mal scia gars",
            "expected_languages": ["French", "Franc-Anglais"],
            "description": "French + Franc-Anglais"
        },
        {
            "expression": "masa network dey bad today",
            "expected_languages": ["English", "Pidgin", "Franc-Anglais"],
            "description": "English + Pidgin + Franc-Anglais"
        },
        {
            "expression": "walahi light don comot direct",
            "expected_languages": ["Fulfulde", "Pidgin", "English"],
            "description": "Fulfulde + Pidgin + English"
        },
        {
            "expression": "je wanda how far ?",
            "expected_languages": ["French", "Pidgin", "English"],
            "description": "French + Pidgin + English"
        },
        {
            "expression": "give me 500 francs",
            "expected_languages": ["English", "French"],
            "description": "English + French"
        }
    ]
    
    results = {
        "full_analysis": [],
        "tokenize_only": [],
        "parse_only": []
    }
    
    # Test Full Analysis endpoint
    print("\n" + "="*60)
    print("TESTING: /api/analyze (Full Analysis)")
    print("="*60)
    for test in test_cases:
        success, result = test_endpoint(
            "/api/analyze",
            {"expression": test["expression"]},
            f"Full Analysis - {test['description']}"
        )
        if success and result:
            results["full_analysis"].append({
                "expression": test["expression"],
                "languages": result.get("languages_detected", []),
                "accepted": result.get("accepted", False)
            })
    
    # Test Tokenize Only endpoint
    print("\n" + "="*60)
    print("TESTING: /api/tokenize (Tokenize Only)")
    print("="*60)
    for test in test_cases:
        success, result = test_endpoint(
            "/api/tokenize",
            {"expression": test["expression"]},
            f"Tokenize Only - {test['description']}"
        )
        if success and result:
            results["tokenize_only"].append({
                "expression": test["expression"],
                "languages": result.get("languages_detected", [])
            })
    
    # Test Parse Only endpoint
    print("\n" + "="*60)
    print("TESTING: /api/parse (Parse Only)")
    print("="*60)
    for test in test_cases:
        success, result = test_endpoint(
            "/api/parse",
            {"expression": test["expression"]},
            f"Parse Only - {test['description']}"
        )
        if success and result:
            results["parse_only"].append({
                "expression": test["expression"],
                "languages": result.get("languages_detected", []),
                "accepted": result.get("accepted", False)
            })
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    print(f"\nFull Analysis Tests: {len(results['full_analysis'])}/{len(test_cases)}")
    print(f"Tokenize Only Tests: {len(results['tokenize_only'])}/{len(test_cases)}")
    print(f"Parse Only Tests: {len(results['parse_only'])}/{len(test_cases)}")
    
    print("\n" + "-"*60)
    print("Language Detection Results:")
    print("-"*60)
    
    for mode, test_results in results.items():
        print(f"\n{mode.upper().replace('_', ' ')}:")
        for result in test_results:
            langs = result.get("languages", [])
            print(f"  • {result['expression'][:40]:<40} → {', '.join(langs) if langs else 'None'}")
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    print("\nTo view the web interface, open: http://localhost:5000")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

