#!/usr/bin/env python3
"""
Cookie Parser Module
Handles extraction and formatting of cookie information from HTTP responses.
"""

from datetime import datetime


def parse_cookies(response):
    """
    Parse cookies from HTTP response and return formatted cookie information.
    
    Args:
        response: requests.Response object
        
    Returns:
        list: List of formatted cookie strings
    """
    cookie_list = []
    
    # Method 1: Using response.cookies (parsed cookies)
    if response.cookies:
        for cookie in response.cookies:
            cookie_info = f"cookie name: {cookie.name}"
            
            # Add expiration time if available
            if cookie.expires:
                expire_date = datetime.fromtimestamp(cookie.expires)
                expires_str = expire_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
                cookie_info += f", expires time: {expires_str}"
            
            # Add domain if available
            if cookie.domain:
                cookie_info += f", domain name: {cookie.domain}"
            
            cookie_list.append(cookie_info)
    
    # Method 2: Parse Set-Cookie headers directly for additional cookies
    set_cookie_headers = []
    if hasattr(response.headers, 'get_list'):
        set_cookie_headers = response.headers.get_list('Set-Cookie')
    elif 'Set-Cookie' in response.headers:
        # Handle single Set-Cookie header
        set_cookie_headers = [response.headers['Set-Cookie']]
    
    # Parse raw Set-Cookie headers for any missed cookies
    processed_names = set()
    if response.cookies:
        processed_names = {cookie.name for cookie in response.cookies}
    
    for cookie_header in set_cookie_headers:
        # Simple parsing of Set-Cookie header
        parts = cookie_header.split(';')
        if parts:
            name_value = parts[0].strip()
            if '=' in name_value:
                cookie_name = name_value.split('=')[0].strip()
                
                # Check if we already processed this cookie
                if cookie_name not in processed_names:
                    cookie_info = f"cookie name: {cookie_name}"
                    
                    # Look for expires and domain in the parts
                    for part in parts[1:]:
                        part_clean = part.strip()
                        part_lower = part_clean.lower()
                        
                        if part_lower.startswith('expires='):
                            expires_value = part_clean.split('=', 1)[1]
                            cookie_info += f", expires time: {expires_value}"
                        elif part_lower.startswith('domain='):
                            domain_value = part_clean.split('=', 1)[1]
                            cookie_info += f", domain name: {domain_value}"
                    
                    cookie_list.append(cookie_info)
                    processed_names.add(cookie_name)
    
    return cookie_list


def print_cookie_list(cookie_list):
    """
    Print the list of cookies in the specified format.
    
    Args:
        cookie_list: List of formatted cookie strings
    """
    if cookie_list:
        for cookie_info in cookie_list:
            print(cookie_info)
    else:
        print("No cookies found")
