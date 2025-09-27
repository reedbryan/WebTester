#!/usr/bin/env python3
"""
Web Tester - A simple HTTP request tool
Takes a URL from stdin and sends an HTTP GET request, printing the results.
"""

import sys
import requests
from requests.exceptions import RequestException


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
        
        # Check HTTP version
        http_version = "Unknown"
        if hasattr(response.raw, 'version'):
            version_map = {9: "0.9", 10: "1.0", 11: "1.1", 20: "2.0"}
            http_version = version_map.get(response.raw.version, f"Unknown ({response.raw.version})")
        
        # Print status information
        print(f"Status Code: {response.status_code}")
        print(f"Status Text: {response.reason}")
        print(f"HTTP Version: {http_version}")
        print(f"URL: {response.url}")
        print(f"Content Length: {len(response.content)} bytes")
        print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
        
        # Check for HTTP/2 specific indicators
        if http_version == "2.0":
            print("✅ This server supports HTTP/2!")
        elif "h2" in response.headers.get('alt-svc', '').lower():
            print("🔍 Server advertises HTTP/2 support via Alt-Svc header")
        else:
            print("❌ HTTP/2 not detected in this connection")
        
        # Print headers
        print("\nResponse Headers:")
        print("-" * 30)
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        
        # Print response body
        print("\nResponse Body:")
        print("-" * 30)
        
        # Try to decode as text, fallback to raw bytes if needed
        try:
            content = response.text
            # Truncate very long responses for readability
            if len(content) > 5000:
                print(content[:5000])
                print(f"\n... [Response truncated - showing first 5000 characters of {len(content)} total]")
            else:
                print(content)
        except UnicodeDecodeError:
            print(f"[Binary content - {len(response.content)} bytes]")
            print("First 100 bytes (hex):")
            print(response.content[:100].hex())
        
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
