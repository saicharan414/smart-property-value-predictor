#!/usr/bin/env python3

from app import app
from forms import RegistrationForm
from flask import Flask
import sys

def test_registration():
    """Test the registration functionality"""
    print("Testing Registration Functionality...")
    
    with app.test_client() as client:
        # Test GET request to register page
        response = client.get('/register')
        print(f'GET /register status: {response.status_code}')
        
        if response.status_code == 200:
            print("✅ Registration page loads successfully")
        else:
            print("❌ Registration page failed to load")
            return False
        
        # Test POST request with valid data
        form_data = {
            'username': 'testuser123',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'csrf_token': ''
        }
        
        response = client.post('/register', data=form_data, follow_redirects=False)
        print(f'POST /register status: {response.status_code}')
        
        if response.status_code == 302:
            print("✅ Registration successful (redirect)")
            print(f"Redirect to: {response.location}")
        elif response.status_code == 200:
            print("❌ Registration failed - form validation errors")
            print("Response content:")
            print(response.get_data(as_text=True)[:500])
        else:
            print(f"❌ Registration failed with status {response.status_code}")
        
        return response.status_code in [200, 302]

if __name__ == '__main__':
    test_registration()
