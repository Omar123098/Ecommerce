#!/usr/bin/env python
"""
Simple script to test CSRF token generation and validation
"""
import os
import sys
import django

# Add the project to the path
sys.path.append('/workspaces/Ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

# Setup Django
django.setup()

from django.middleware.csrf import get_token
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware

def test_csrf():
    # Create a request factory
    factory = RequestFactory()
    
    # Create a GET request
    request = factory.get('/')
    
    # Add session middleware
    session_middleware = SessionMiddleware(lambda req: None)
    session_middleware.process_request(request)
    request.session.save()
    
    # Add CSRF middleware
    csrf_middleware = CsrfViewMiddleware(lambda req: None)
    csrf_middleware.process_request(request)
    
    # Get CSRF token
    token = get_token(request)
    print(f"Generated CSRF token: {token}")
    print(f"Token length: {len(token)}")
    print(f"Session key: {request.session.session_key}")
    
    return token

if __name__ == "__main__":
    test_csrf()
