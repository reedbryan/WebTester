#!/usr/bin/env python3
"""
HTTP/2 Checker Module
Detects HTTP/2 support using multiple methods since Python requests doesn't natively support HTTP/2.
"""

import requests
from requests.exceptions import RequestException
import urllib3

# Disable SSL warnings since we're intentionally using verify=False for HTTP/2 detection
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_http2_support(url, timeout=10):
    """
    Check if a URL supports HTTP/2 using multiple detection methods.
    
    Args:
        url (str): The URL to check
        timeout (int): Request timeout in seconds
        
    Returns:
        dict: Dictionary containing HTTP/2 support information:
            - supports_http2 (bool): True if HTTP/2 is supported
            - detection_method (str): How HTTP/2 support was detected
            - details (str): Additional details about the detection
            - alt_svc_header (str): Alt-Svc header value if present
    """
    http2_info = {
        'supports_http2': False,
        'detection_method': 'None',
        'details': 'HTTP/2 not detected',
        'alt_svc_header': None
    }
    
    try:
        # Make HTTPS request (HTTP/2 requires TLS in most cases)
        https_url = url.replace('http://', 'https://') if url.startswith('http://') else url
        if not https_url.startswith('https://'):
            https_url = 'https://' + https_url.replace('http://', '').replace('https://', '')
        
        response = requests.get(https_url, timeout=timeout, verify=False)
        
        # Method 1: Check Alt-Svc header (most reliable indicator)
        alt_svc = response.headers.get('alt-svc', response.headers.get('Alt-Svc', ''))
        if alt_svc:
            http2_info['alt_svc_header'] = alt_svc
            alt_svc_lower = alt_svc.lower()
            
            # Look for h2 protocol in Alt-Svc
            if 'h2=' in alt_svc_lower or 'h2"' in alt_svc_lower or 'h2 ' in alt_svc_lower:
                http2_info['supports_http2'] = True
                http2_info['detection_method'] = 'Alt-Svc header (h2)'
                http2_info['details'] = f'HTTP/2 advertised in Alt-Svc header: {alt_svc}'
                return http2_info
            
            # Look for h3 protocol (HTTP/3 implies HTTP/2 support)
            elif 'h3=' in alt_svc_lower or 'h3"' in alt_svc_lower or 'h3 ' in alt_svc_lower:
                http2_info['supports_http2'] = True
                http2_info['detection_method'] = 'Alt-Svc header (h3 implies h2)'
                http2_info['details'] = f'HTTP/3 advertised (implies HTTP/2): {alt_svc}'
                return http2_info
        
        # Method 2: Check for HTTP/2 specific headers
        http2_headers = [
            ':status', ':method', ':path', ':scheme', ':authority'
        ]
        for header in response.headers:
            if header.startswith(':'):
                http2_info['supports_http2'] = True
                http2_info['detection_method'] = 'HTTP/2 pseudo-headers'
                http2_info['details'] = f'HTTP/2 pseudo-header detected: {header}'
                return http2_info
        
        # Method 3: Check Server header for HTTP/2 hints
        server_header = response.headers.get('server', '').lower()
        if 'h2' in server_header or 'http/2' in server_header:
            http2_info['supports_http2'] = True
            http2_info['detection_method'] = 'Server header'
            http2_info['details'] = f'HTTP/2 indicated in Server header: {response.headers.get("server")}'
            return http2_info
        
        # Method 4: Try to detect common HTTP/2 server patterns
        common_h2_servers = [
            'cloudflare', 'nginx/1.', 'apache/2.4', 'google', 'amazon', 'microsoft'
        ]
        
        if server_header and any(pattern in server_header for pattern in common_h2_servers):
            # These servers commonly support HTTP/2, but we can't be certain
            # Let's check if we're on HTTPS (required for most HTTP/2)
            if response.url.startswith('https://'):
                # Make educated guess based on modern server + HTTPS
                major_domains = ['google.', 'facebook.', 'amazon.', 'microsoft.', 'apple.', 'cloudflare.']
                if any(domain in response.url.lower() for domain in major_domains):
                    http2_info['supports_http2'] = True
                    http2_info['detection_method'] = 'Heuristic (major site + HTTPS)'
                    http2_info['details'] = f'Likely supports HTTP/2 (major site with HTTPS): {server_header}'
                    return http2_info
        
        # Method 5: Check for ALPN in TLS handshake (limited info from requests)
        # This is harder to detect with standard requests library
        
        # If we get here, no clear HTTP/2 indicators found
        if response.url.startswith('https://'):
            http2_info['details'] = 'No clear HTTP/2 indicators found (HTTPS site)'
        else:
            http2_info['details'] = 'HTTP/2 unlikely (not HTTPS)'
            
    except RequestException as e:
        # Try HTTP if HTTPS failed
        try:
            http_url = url.replace('https://', 'http://') if url.startswith('https://') else url
            response = requests.get(http_url, timeout=timeout)
            http2_info['details'] = 'HTTP/2 very unlikely (HTTP only, no encryption)'
        except RequestException:
            http2_info['details'] = f'Could not connect to check HTTP/2 support: {str(e)}'
    
    return http2_info


def format_http2_result(http2_info):
    """
    Format HTTP/2 check results for display.
    
    Args:
        http2_info (dict): HTTP/2 information dictionary
        
    Returns:
        str: "yes" or "no" for simple output
    """
    return "yes" if http2_info['supports_http2'] else "no"
