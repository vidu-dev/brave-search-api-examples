#!/usr/bin/env bash
# One Brave Search API request with curl. Usage: bash examples/web_search.sh 'your query'
#
# Endpoint, header name and query parameter name are ILLUSTRATIVE defaults.
# Confirm them in the developer docs on the API dashboard and override via env.
set -euo pipefail

if [ -z "${BRAVE_SEARCH_API_KEY:-}" ]; then
  echo 'Set BRAVE_SEARCH_API_KEY first.' >&2
  exit 1
fi
if [ $# -lt 1 ]; then
  echo "Usage: bash examples/web_search.sh 'your query'" >&2
  exit 1
fi

ENDPOINT="${BRAVE_SEARCH_ENDPOINT:-https://api.search.brave.com/res/v1/web/search}"  # illustrative
AUTH_HEADER="${BRAVE_SEARCH_AUTH_HEADER:-X-Subscription-Token}"                     # illustrative
QUERY_PARAM="${BRAVE_SEARCH_QUERY_PARAM:-q}"                                          # illustrative

# --get with --data-urlencode builds the query string safely.
response=$(curl -sS --get "$ENDPOINT" \
  -H "Accept: application/json" \
  -H "$AUTH_HEADER: $BRAVE_SEARCH_API_KEY" \
  --data-urlencode "$QUERY_PARAM=$*")

if command -v jq >/dev/null 2>&1; then
  # Show the top-level keys first, then the body; field names come from the docs.
  echo "$response" | jq -r 'if type == "object" then (keys | join(", ")) else type end'
  echo "$response" | jq . | head -n 80
else
  echo "$response" | head -c 2000
  echo
fi
