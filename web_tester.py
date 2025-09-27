#!/usr/bin/env python3
"""
Web Tester - A simple HTTP request tool
Takes a URL from stdin and sends an HTTP GET request, printing the results.
"""

import sys
import requests
from requests.exceptions import RequestException
from datetime import datetime
from urllib.parse import urlparse


def main():
    try:
        # Get URL from stdin
        print("Enter a URL: ", end="", flush=True)
        url = input().strip()
        
        if not url:
            print("Error: No URL provided", file=sys.stderr)
            sys.exit(1)
        
        # Add http:// if no protocol is specified
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        print(f"\nSending request to: {url}")
        print("-" * 50)
        
        # Send HTTP GET request
        response = requests.get(url, timeout=10)
        
        # Extract website name from URL
        parsed_url = urlparse(response.url)
        website = parsed_url.netloc
        
        # Check HTTP version
        http_version = "Unknown"
        if hasattr(response.raw, 'version'):
            version_map = {9: "0.9", 10: "1.0", 11: "1.1", 20: "2.0"}
            http_version = version_map.get(response.raw.version, f"Unknown ({response.raw.version})")
        
        # Determine HTTP/2 support
        supports_http2 = "yes" if http_version == "2.0" or "h2" in response.headers.get('alt-svc', '').lower() else "no"
        
        # Print formatted output
        print(f"website: {website}")
        print(f"1. Supports http2: {supports_http2}")
        print("2. List of Cookies:")
        
        # Parse cookies
        cookies_found = False
        
        # Method 1: Using response.cookies (parsed cookies)
        if response.cookies:
            cookies_found = True
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
                
                print(cookie_info)
        
        # Method 2: Parse Set-Cookie headers directly for additional cookies
        set_cookie_headers = []
        if hasattr(response.headers, 'get_list'):
            set_cookie_headers = response.headers.get_list('Set-Cookie')
        elif 'Set-Cookie' in response.headers:
            # Handle single Set-Cookie header
            set_cookie_headers = [response.headers['Set-Cookie']]
        
        # Parse raw Set-Cookie headers for any missed cookies
        for cookie_header in set_cookie_headers:
            # Simple parsing of Set-Cookie header
            parts = cookie_header.split(';')
            if parts:
                name_value = parts[0].strip()
                if '=' in name_value:
                    cookie_name = name_value.split('=')[0].strip()
                    
                    # Check if we already processed this cookie
                    already_processed = False
                    if response.cookies:
                        for existing_cookie in response.cookies:
                            if existing_cookie.name == cookie_name:
                                already_processed = True
                                break
                    
                    if not already_processed:
                        cookies_found = True
                        cookie_info = f"cookie name: {cookie_name}"
                        
                        # Look for expires and domain in the parts
                        for part in parts[1:]:
                            part = part.strip().lower()
                            if part.startswith('expires='):
                                expires_value = part.split('=', 1)[1]
                                cookie_info += f", expires time: {expires_value}"
                            elif part.startswith('domain='):
                                domain_value = part.split('=', 1)[1]
                                cookie_info += f", domain name: {domain_value}"
                        
                        print(cookie_info)
        
        if not cookies_found:
            print("No cookies found")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
