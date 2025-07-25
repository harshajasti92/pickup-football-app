#!/usr/bin/env python3
"""
Test login API directly
"""
import requests
import json

def test_login():
    url = "http://localhost:8000/api/users/login"
    data = {
        "username": "john_striker",
        "password": "test123"
    }
    
    print("🧪 Testing login API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Login successful!")
            print(f"📝 User data: {json.dumps(user_data, indent=2)}")
        else:
            print("❌ Login failed!")
            try:
                error_data = response.json()
                print(f"🔍 Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"🔍 Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
