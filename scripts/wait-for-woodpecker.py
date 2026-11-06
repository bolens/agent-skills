#!/usr/bin/env python3
"""Join this exact source revision's native validation without rerunning it."""
import json
import os
import re
import time
import urllib.error
import urllib.request

REPOSITORY = 'bolens/agent-skills'
REPOSITORY_ID = 1355138486
CREATOR_ID = 1218380
TARGET = re.compile(r'https://woodpecker\.bolens\.dev/repos/28/pipeline/[1-9][0-9]*/1')


def select_state(payload, history, sha, context):
    if payload.get('sha') != sha:
        raise ValueError('status response revision mismatch')
    repo = payload.get('repository', {})
    if repo.get('id') != REPOSITORY_ID or repo.get('full_name') != REPOSITORY:
        raise ValueError('status response repository mismatch')
    entries = [entry for entry in payload.get('statuses', []) if entry.get('context') == context]
    if not entries:
        return 'missing'
    if len(entries) != 1:
        raise ValueError('ambiguous native status')
    entry = entries[0]
    identifier = entry.get('id')
    if not isinstance(identifier, int) or identifier <= 0:
        raise ValueError('invalid native status identity')
    raw = [item for item in history if item.get('context') == context]
    if not raw:
        raise ValueError('native status history incomplete')
    # The combined response omits creator. Bind the newest raw status by ID;
    # never accept an older success when a newer pending/failure has appeared.
    if any(not isinstance(item.get('id'), int) or item['id'] <= 0 for item in raw):
        raise ValueError('invalid native status history identity')
    newest = max(raw, key=lambda item: item['id'])
    if newest['id'] != identifier:
        return 'changed'
    if any(newest.get(key) != entry.get(key) for key in ('context', 'state', 'target_url')):
        raise ValueError('native status history mismatch')
    if newest.get('url') != f'https://api.github.com/repos/{REPOSITORY}/statuses/{sha}':
        raise ValueError('native status history repository mismatch')
    if newest.get('creator', {}).get('id') != CREATOR_ID:
        raise ValueError('native status publisher mismatch')
    if not TARGET.fullmatch(entry.get('target_url') or ''):
        raise ValueError('native status pipeline mismatch')
    state = entry.get('state')
    if state not in {'pending', 'success', 'failure', 'error'}:
        raise ValueError('unknown native status state')
    return state


def wait(read, sha, context, *, clock=time.monotonic, sleep=time.sleep, timeout=3300):
    deadline = clock() + timeout
    previous = None
    while clock() < deadline:
        state = select_state(*read(), sha, context)
        if clock() >= deadline:
            break
        if state != previous:
            print('Native validation: ' + state, flush=True)
            previous = state
        if state == 'success':
            return
        if state in {'failure', 'error'}:
            raise RuntimeError('native validation failed')
        sleep(min(15, max(0, deadline - clock())))
    raise TimeoutError('native validation did not succeed before the deadline')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('unexpected GitHub API redirect')


def main():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise ValueError('unexpected workflow repository')
    event = os.environ.get('GITHUB_EVENT_NAME')
    if event not in {'pull_request', 'push', 'workflow_dispatch'}:
        raise ValueError('unsupported workflow event')
    if event == 'workflow_dispatch' and os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise ValueError('manual redeployment requires main')
    sha = os.environ.get('TARGET_SHA', '')
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('invalid source revision')
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise ValueError('missing read-only GitHub token')
    context = 'ci/woodpecker/' + ('pr' if event == 'pull_request' else 'push') + '/portable'
    opener = urllib.request.build_opener(NoRedirect())

    def get(url):
        request = urllib.request.Request(url, headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + token,
            'X-GitHub-Api-Version': '2022-11-28',
        })
        try:
            with opener.open(request, timeout=15) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'GitHub status lookup failed: HTTP {error.code}') from None

    def read():
        base = f'https://api.github.com/repos/{REPOSITORY}/commits/{sha}'
        combined = get(base + '/status?per_page=100')
        selected = [item for item in combined.get('statuses', []) if item.get('context') == context]
        if not selected:
            return combined, []
        identifier = selected[0].get('id')
        history = []
        for page in range(1, 11):
            entries = get(base + f'/statuses?per_page=100&page={page}')
            if not isinstance(entries, list):
                raise ValueError('invalid native status history response')
            history.extend(entries)
            if any(item.get('id') == identifier for item in entries) or len(entries) < 100:
                return combined, history
        raise ValueError('native status history pagination bound exceeded')

    wait(read, sha, context)


if __name__ == '__main__':
    main()
