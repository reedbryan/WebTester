#!/usr/bin/env python3
"""
Authentication Checker Module
Handles detection of password-protected URLs and authentication requirements.
"""

import requests
from requests.exceptions import RequestException


def check_password_protection(url, timeout=10):
    """
    Check if a URL is password-protected by analyzing the HTTP response.
    
    Args:
        url (str): The URL to check
        timeout (int): Request timeout in seconds
        
    Returns:
        dict: Dictionary containing authentication information:
            - is_protected (bool): True if password-protected
            - status_code (int): HTTP status code
            - auth_type (str): Type of authentication detected
            - realm (str): Authentication realm if available
            - details (str): Additional details about the protection
    """
    auth_info = {
        'is_protected': False,
        'status_code': None,
        'auth_type': None,
        'realm': None,
        'details': 'No authentication required'
    }
    
    try:
        # Make initial request without authentication
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        auth_info['status_code'] = response.status_code
        
        # Check for 401 Unauthorized
        if response.status_code == 401:
            auth_info['is_protected'] = True
            auth_info['details'] = 'Password protection detected (401 Unauthorized)'
            
            # Parse WWW-Authenticate header for more details
            www_auth = response.headers.get('WWW-Authenticate', '')
            if www_auth:
                auth_info['auth_type'] = parse_auth_type(www_auth)
                auth_info['realm'] = parse_auth_realm(www_auth)
                auth_info['details'] += f' - {auth_info["auth_type"]}'
                if auth_info['realm']:
                    auth_info['details'] += f' (Realm: {auth_info["realm"]})'
        
        # Check for 403 Forbidden (another form of access restriction)
        elif response.status_code == 403:
            auth_info['is_protected'] = True
            auth_info['details'] = 'Access forbidden (403 Forbidden)'
        
        # Check for other authentication-related status codes
        elif response.status_code == 407:
            auth_info['is_protected'] = True
            auth_info['details'] = 'Proxy authentication required (407)'
        
        # Check for common login page indicators in the content
        elif response.status_code == 200:
            content_lower = response.text.lower()
            login_indicators = [
                'password', 'login', 'signin', 'sign in', 'authenticate',
                'username', 'user name', 'email', 'log in'
            ]
            
            # Look for login forms
            if '<form' in content_lower and any(indicator in content_lower for indicator in login_indicators):
                # More specific check for login forms
                if ('type="password"' in content_lower or 
                    'input[type="password"]' in content_lower or
                    ('name="password"' in content_lower or 'id="password"' in content_lower)):
                    auth_info['is_protected'] = True
                    auth_info['details'] = 'Login form detected on page'
                    auth_info['auth_type'] = 'Form-based authentication'
        
        # Check for redirect to login page
        elif response.status_code in [302, 303, 307, 308]:
            location = response.headers.get('Location', '').lower()
            if any(keyword in location for keyword in ['login', 'signin', 'auth', 'authenticate']):
                auth_info['is_protected'] = True
                auth_info['details'] = f'Redirect to login page detected ({response.status_code})'
                auth_info['auth_type'] = 'Redirect-based authentication'
    
    except RequestException as e:
        auth_info['details'] = f'Error checking authentication: {str(e)}'
    
    return auth_info


def parse_auth_type(www_authenticate):
    """
    Parse the authentication type from WWW-Authenticate header.
    
    Args:
        www_authenticate (str): WWW-Authenticate header value
        
    Returns:
        str: Authentication type (Basic, Digest, Bearer, etc.)
    """
    auth_type = www_authenticate.split(' ')[0] if www_authenticate else 'Unknown'
    return auth_type


def parse_auth_realm(www_authenticate):
    """
    Parse the authentication realm from WWW-Authenticate header.
    
    Args:
        www_authenticate (str): WWW-Authenticate header value
        
    Returns:
        str: Authentication realm or None
    """
    if 'realm=' in www_authenticate:
        try:
            realm_part = www_authenticate.split('realm=')[1]
            # Remove quotes and get the realm value
            realm = realm_part.split(',')[0].strip().strip('"\'')
            return realm
        except (IndexError, AttributeError):
            return None
    return None


def format_auth_result(auth_info):
    """
    Format authentication check results for display.
    
    Args:
        auth_info (dict): Authentication information dictionary
        
    Returns:
        str: Formatted string for display
    """
    if auth_info['is_protected']:
        return f"yes - {auth_info['details']}"
    else:
        return f"no - {auth_info['details']}"
