#!/usr/bin/env python3
"""
Test script for Voyage Analytics Authentication API
Run this after starting the FastAPI server with: uvicorn app.main:app --reload
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/v1"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_response(response, title="Response"):
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health_check():
    print_header("HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def test_register():
    print_header("USER REGISTRATION")
    
    # Test data
    user_email = f"testuser_{datetime.now().timestamp()}@example.com"
    user_data = {
        "email": user_email,
        "password": "TestPassword123",
        "name": "Test User"
    }
    
    print(f"Registering user: {user_email}")
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_response(response, "Register Response")
    
    if response.status_code == 201:
        token = response.json()["access_token"]
        return True, token, user_email, user_data["password"]
    return False, None, None, None

def test_duplicate_registration(email):
    print_header("DUPLICATE REGISTRATION TEST")
    
    user_data = {
        "email": email,
        "password": "AnotherPassword123",
        "name": "Another User"
    }
    
    print(f"Attempting to register duplicate email: {email}")
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_response(response, "Duplicate Registration Response")
    
    return response.status_code == 400

def test_login(email, password):
    print_header("USER LOGIN")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    print(f"Logging in as: {email}")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "Login Response")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return True, token
    return False, None

def test_invalid_login(email):
    print_header("INVALID LOGIN TEST")
    
    login_data = {
        "email": email,
        "password": "WrongPassword123"
    }
    
    print(f"Attempting login with wrong password for: {email}")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "Invalid Login Response")
    
    return response.status_code == 401

def test_get_current_user(token):
    print_header("GET CURRENT USER")
    
    headers = {"Authorization": f"Bearer {token}"}
    print("Fetching current user information...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response, "Current User Response")
    
    return response.status_code == 200

def test_invalid_token():
    print_header("INVALID TOKEN TEST")
    
    headers = {"Authorization": "Bearer invalid_token_here"}
    print("Attempting to access /auth/me with invalid token...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response, "Invalid Token Response")
    
    return response.status_code == 401

def test_no_token():
    print_header("NO TOKEN TEST")
    
    print("Attempting to access /auth/me without token...")
    response = requests.get(f"{BASE_URL}/auth/me")
    print_response(response, "No Token Response")
    
    return response.status_code == 403

def main():
    print("\n" + "█"*60)
    print("█  VOYAGE ANALYTICS - AUTHENTICATION API TEST SUITE  █")
    print("█"*60)
    
    results = {}
    
    # Test 1: Health Check
    results["Health Check"] = test_health_check()
    
    # Test 2: Register
    success, token, email, password = test_register()
    results["Register"] = success
    
    if success:
        # Test 3: Duplicate Registration
        results["Duplicate Registration"] = test_duplicate_registration(email)
        
        # Test 4: Login
        success, new_token = test_login(email, password)
        results["Login"] = success
        
        # Test 5: Invalid Login
        results["Invalid Login"] = test_invalid_login(email)
        
        # Test 6: Get Current User
        results["Get Current User"] = test_get_current_user(token)
        
        # Test 7: Invalid Token
        results["Invalid Token"] = test_invalid_token()
        
        # Test 8: No Token
        results["No Token"] = test_no_token()
    else:
        print("\n❌ Registration failed, skipping dependent tests")
    
    # Print summary
    print_header("TEST SUMMARY")
    print("\nTest Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<30} {status}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Make sure the FastAPI server is running:")
        print("  cd ml-service")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
