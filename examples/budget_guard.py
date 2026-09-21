"""Keep a development project inside the Brave Search API free monthly credit.

Brave's Search plan is $5 per 1,000 requests and every account gets $5 in free
credits each month, so 1,000 requests a month are covered. This wrapper counts
requests per calendar month in a local JSON file and refuses to send more than
MONTHLY_LIMIT. It also spaces calls to stay far below the plan's 50 queries per
second capacity. Server-side metering belongs in production; this is for laptops.

Usage: python3 examples/budget_guard.py 'your query'
"""
import datetime
import json
import os
import sys
import time

from web_search import search  # examples/web_search.py, same env vars

MONTHLY_LIMIT = 1000            # requests covered by the $5 free credit on the Search plan
MIN_INTERVAL_SECONDS = 0.1      # 10 requests per second, well under the 50 qps capacity
STATE_FILE = os.environ.get('BRAVE_BUDGET_FILE', os.path.expanduser('~/.brave_search_budget.json'))


def _load():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)


def guarded_search(query):
    month = datetime.date.today().strftime('%Y-%m')
    state = _load()
    if state.get('month') != month:
        state = {'month': month, 'count': 0, 'last': 0.0}
    if state['count'] >= MONTHLY_LIMIT:
        raise SystemExit(f'Monthly limit of {MONTHLY_LIMIT} requests reached for {month}; not sending.')
    wait = MIN_INTERVAL_SECONDS - (time.time() - state.get('last', 0.0))
    if wait > 0:
        time.sleep(wait)
    resp = search(query)
    state['count'] += 1
    state['last'] = time.time()
    _save(state)
    remaining = MONTHLY_LIMIT - state['count']
    print(f'status {resp.status_code}; {remaining} free requests left this month', file=sys.stderr)
    return resp


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python3 examples/budget_guard.py "your query"')
    r = guarded_search(' '.join(sys.argv[1:]))
    print(r.text[:1000])
