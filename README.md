# Brave Search API examples

*Unofficial community examples for the Brave Search API. Not affiliated with Brave Software. All trademarks belong to their owners.*

Small, self-contained Brave Search API examples: a Python client that reads the key from the environment, the same call as a shell script, and a budget guard that keeps a development project inside the $5 of free monthly credits (1,000 requests at the Search plan rate of $5 per 1,000). Endpoint URL, header name and query parameter name are read from environment variables with defaults that are marked illustrative in the code; confirm them against the [developer docs](https://api-dashboard.search.brave.com/documentation/services/llm-context) before relying on them.

> Searching is often step one and generating is step two. [Try Synexa - one REST endpoint and a Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=brave-search-api-examples&utm_content=readme-top&utm_term=tier-r).

## Files

| Path | What it shows |
| --- | --- |
| examples/web_search.py | a single search request with the key from an environment variable, printing the raw JSON shape |
| examples/web_search.sh | the same request as a curl one-liner wrapped in a script |
| examples/budget_guard.py | a local counter that refuses to send request 1,001 in a calendar month |

## Setup

1. Register at the [API dashboard](https://api-dashboard.search.brave.com/register) and create a key. The account includes $5 in free credits every month.
2. Export the variables:

```
export BRAVE_SEARCH_API_KEY=your_key_here
# Optional overrides; copy the current values from the developer docs.
export BRAVE_SEARCH_ENDPOINT=...
export BRAVE_SEARCH_AUTH_HEADER=...
export BRAVE_SEARCH_QUERY_PARAM=...
```

3. Python examples need the `requests` package. The shell example needs curl and, for pretty printing, jq.

## web_search.py

Reads the key, endpoint, header name and query parameter name from the environment, sends one GET with the query from the command line, and prints the HTTP status plus the top-level keys of the JSON response before printing the first part of the body. Printing the shape first is deliberate: the response structure is defined in the developer docs and can change, so the script does not hard-code field names. Once you have seen the keys on your own account, pull out the fields you need.

## web_search.sh

The same call with curl. Useful for checking a key from a server where Python is not available, and for reproducing a request exactly when something looks off. Piping through jq is optional; without it you get the raw JSON.

## budget_guard.py

A tiny wrapper around the search call that keeps a per-month counter in a local JSON file and stops at 1,000 requests, the number the $5 free monthly credit covers on the Search plan. It is meant for development machines and side projects where you do not want a surprise charge; in production you would meter on the server side instead. The limit is a constant at the top so you can raise it once you move to paid usage. It also spaces requests to stay well under the Search plan's 50 queries per second capacity, which matters if you ever run it in a loop.

## When to use Synexa instead

None of these files generate anything; they retrieve. If the step after retrieval is to produce an image, a clip or a voice track, for example a product card with a generated hero image, or a news summary with narration, [Try Synexa - one REST endpoint and a Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=brave-search-api-examples&utm_content=readme-top&utm_term=tier-r). Pay-per-run pricing keeps the cost model the same shape as Brave's per-request pricing, and one endpoint covers the model catalogue instead of one SDK per vendor.


_Last reviewed: 2026-09-22_
