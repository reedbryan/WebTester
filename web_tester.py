#!/usr/bin/env python3
"""
Web Tester - A simple HTTP request tool
Takes a URL from stdin and sends an HTTP GET request, printing the results.
"""

import sys
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
from cookie_parser import parse_cookies, print_cookie_list
from auth_checker import check_password_protection, format_auth_result


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
        
        # Check for password protection
        auth_info = check_password_protection(url)
        password_protected = format_auth_result(auth_info)
        
        # Print formatted output
        print(f"website: {website}")
        print(f"1. Supports http2: {supports_http2}")
        print(f"2. List of Cookies:")
        
        # Parse and print cookies using the cookie_parser module
        cookie_list = parse_cookies(response)
        print_cookie_list(cookie_list)
        
        print(f"3. Password-protected: {password_protected}")
        
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