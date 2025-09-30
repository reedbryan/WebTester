#!/usr/bin/env python3
"""
Web Tester - A HTTP/2, Cookie, and Authentication Analyzer
Interactive tool that analyzes websites in a loop until the user exits.
Provides information about HTTP/2 support, cookies, and password protection.
"""

import sys
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
from cookie_parser import parse_cookies, print_cookie_list
from auth_checker import check_password_protection, format_auth_result
from http2_checker import check_http2_support, format_http2_result


def main():
    print("Web Tester - HTTP/2, Cookie, and Authentication Analyzer")
    print("Enter 'quit' or 'exit' to stop the program")
    print("=" * 60)
    
    while True:
        try:
            # Get URL from stdin
            print("\nEnter a URL: ", end="", flush=True)
            url = input().strip()
            
            # Check for exit commands
            if url.lower() in ['quit', 'exit', 'q', '']:
                print("Goodbye!")
                break
            
            # Add http:// if no protocol is specified
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            print(f"\nSending request to: {url}")
            print("-" * 50)
            
            try:
                # Send HTTP GET request
                response = requests.get(url, timeout=10)
                
                # Extract website name from URL
                parsed_url = urlparse(response.url)
                
                # Check for HTTP/2 support using improved detection
                http2_info = check_http2_support(url)
                supports_http2 = format_http2_result(http2_info)
                
                # Check for password protection
                auth_info = check_password_protection(url)
                password_protected = format_auth_result(auth_info)
                
                # Print formatted output
                print(f"1. Supports http2: {supports_http2}")
                print(f"2. List of Cookies:")
                
                # Parse and print cookies using the cookie_parser module
                cookie_list = parse_cookies(response)
                print_cookie_list(cookie_list)
                
                print(f"3. Password-protected: {password_protected}")
                
            except RequestException as e:
                print(f"Request failed: {e}")
                print("Please try another URL or check your internet connection.")
            except Exception as e:
                print(f"Unexpected error: {e}")
                print("Please try another URL.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()