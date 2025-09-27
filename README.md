# Web Tester

A simple Python program that takes a URL input from stdin, sends an HTTP GET request, and prints the results to the terminal.

## Files

- `web_tester.py` - Main version using the `requests` library (recommended)
- `requirements.txt` - Dependencies for the main version

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

## Features

- Accepts URLs with or without protocol (automatically adds http:// if missing)
- Displays comprehensive response information:
  - Status code and reason
  - Final URL (after redirects)
  - Response headers
  - Content length and type
  - Response body (truncated if very long)
- Handles binary content gracefully
- Error handling for various network issues
- Timeout protection (10 seconds)

## Examples

```bash
$ python web_tester.py
Enter a URL: httpbin.org/json
Sending request to: http://httpbin.org/json
--------------------------------------------------
Status Code: 200
Status Text: OK
URL: https://httpbin.org/json
Content Length: 429 bytes
Content Type: application/json

Response Headers:
------------------------------
Date: Fri, 27 Sep 2025 10:30:00 GMT
Content-Type: application/json
Content-Length: 429
...

Response Body:
------------------------------
{
  "slideshow": {
    "author": "Yours Truly",
    "date": "date of publication",
    ...
  }
}
```

## Error Handling

The program handles various error conditions:
- Invalid URLs
- Network timeouts
- HTTP errors (4xx, 5xx status codes)
- Connection refused
- DNS resolution failures
- Binary content that cannot be decoded as text
