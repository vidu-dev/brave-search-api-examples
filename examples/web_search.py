"""One Brave Search API request with the key read from the environment.

Usage: python3 examples/web_search.py 'your query'

The endpoint, auth header name and query parameter name below are ILLUSTRATIVE
defaults. Copy the current values from the developer docs on the API dashboard
and set them as environment variables if they differ.
"""
import json
import os
import sys

import requests

API_KEY = os.environ.get('BRAVE_SEARCH_API_KEY')
ENDPOINT = os.environ.get('BRAVE_SEARCH_ENDPOINT', 'https://api.search.brave.com/res/v1/web/search')  # illustrative
AUTH_HEADER = os.environ.get('BRAVE_SEARCH_AUTH_HEADER', 'X-Subscription-Token')  # illustrative
QUERY_PARAM = os.environ.get('BRAVE_SEARCH_QUERY_PARAM', 'q')  # illustrative


def search(query, timeout=15):
    if not API_KEY:
        raise SystemExit('Set BRAVE_SEARCH_API_KEY first (never put the key in code).')
    headers = {AUTH_HEADER: API_KEY, 'Accept': 'application/json'}
    resp = requests.get(ENDPOINT, headers=headers, params={QUERY_PARAM: query}, timeout=timeout)
    return resp


def main():
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python3 examples/web_search.py "your query"')
    resp = search(' '.join(sys.argv[1:]))
    print('status:', resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        print(resp.text[:500])
        return
    # Print the shape first; field names are defined by the developer docs.
    if isinstance(data, dict):
        print('top-level keys:', sorted(data.keys()))
    print(json.dumps(data, indent=2)[:2000])


if __name__ == '__main__':
    main()
