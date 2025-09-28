# Web Tester

A Python program that analyzes websites for HTTP/2 support, cookie information, and password protection. Takes a URL input and provides detailed analysis in a clean, formatted output.

## Files

- `web_tester.py` - Main program that analyzes URLs for HTTP/2 support, cookies, and password protection
- `cookie_parser.py` - Module for extracting and formatting cookie information from HTTP responses
- `auth_checker.py` - Module for detecting password-protected URLs and authentication requirements  
- `http2_checker.py` - Module for detecting if a website supports HTTP2
- `requirements.txt` - Dependencies for the main version
- `.gitignore` - Git ignore file for Python projects

## Installation and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the program:
   ```bash
   python web_tester.py
   ```

3. Enter a URL when prompted (e.g., `google.com` or `uvic.ca`)

## Examples

```bash
$ python web_tester.py
Enter a URL: google.com

website: www.google.com
1. Supports http2: no
2. List of Cookies:
cookie name: AEC, expires time: Thu, 26-Mar-2026 16:12:14 GMT, domain name: .google.com
cookie name: NID, expires time: Sun, 29-Mar-2026 16:12:14 GMT, domain name: .google.com
3. Password-protected: no - No authentication required
```

```bash
$ python web_tester.py  
Enter a URL: httpbin.org/basic-auth/user/pass

website: httpbin.org
1. Supports http2: no
2. List of Cookies:
No cookies found
3. Password-protected: yes - Password protection detected (401 Unauthorized) - Basic (Realm: Fake Realm)
```

## Error Handling

The program handles various error conditions:
- Invalid URLs
- Network timeouts
- HTTP errors (4xx, 5xx status codes)
- Connection refused
- DNS resolution failures
- Binary content that cannot be decoded as text
