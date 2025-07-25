#!/usr/bin/env python3
"""
Test script to verify login API endpoint
"""
import requests
import json

# Test the login API endpoint
def test_login():
    url = "http://localhost:8000/api/users/login"
    
    # Test with credentials from test_user.json
    test_credentials = {
        "username": "jumaji",
        "password": "password"  # Updated credentials from test_user.json
    }
    
    print("🧪 Testing login API endpoint...")
    print(f"URL: {url}")
    print(f"Testing with username: {test_credentials['username']}")
    
    try:
        response = requests.post(url, json=test_credentials)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Login successful!")
            print(f"Welcome: {user_data['first_name']} {user_data['last_name']}")
            print(f"Username: {user_data['username']}")
            print(f"Skill Level: {user_data['skill_level']}/10")
            if user_data['preferred_position']:
                print(f"Position: {user_data['preferred_position']}")
            return True
        else:
            error_data = response.json()
            print(f"❌ Login failed: {error_data.get('detail', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error testing login: {str(e)}")
        return False

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Backend API is running!")
            return True
        else:
            print("❌ Backend API responded with error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend API is not running")
        return False

if __name__ == "__main__":
    print("🔍 Testing Login Functionality")
    print("=" * 40)
    
    # First check if API is running
    if test_api_health():
        # Test login endpoint
        test_login()
    else:
        print("Please start the backend server first: python run.py")
