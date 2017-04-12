from all_pycco.pycco import main as m
import os
import flask
import re
import json
import traceback
from urllib import urlencode

import requests
from flask import Flask, session, request, redirect

# Comment here


def main():
    m.process("/Users/brianb/workspace/cheatsheet/instagram/app.py",
              outdir="/Users/brianb/workspace/cheatsheet/output",
              language="python",
              encoding="latin-1")

#main()


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


def process_status(data):
    # Now we are looking for PR where commit which status is updated is head
    state = data.get('state')
    context = data.get('context')
    target_url = data.get('target_url')
    sha = data.get('sha')
    author = data.get('commit').get('author')
    if author:
        username = author.get('login')
    else:
        print("Commit without author: {}".format(data.get('commit').get('commit')))
        return
    repository_owner = data.get('repository').get('owner').get('login')
    repository_name = data.get('repository').get('name')
    found_pr = None

    branch_names = [b['name'] for b in data.get('branches')]
    for branch_name in branch_names:
        prs = github.get('/repos/{}/{}/pulls?head={}:{}&state=open'.format(
            repository_owner,
            repository_name,
            repository_owner,
            branch_name
        ))
        for pr in prs:
            if pr.get('head').get('sha') == sha:
                found_pr = pr
                break

    if found_pr:
        # We've found PR where checked commit is head
        if state in ['error', 'failure']:
            _send_pr_check_failure_notification(username, pr, context, target_url)
        else:
            status = github.get('/repos/{}/{}/commits/{}/status'.format(
                repository_owner,
                repository_name,
                sha
            ))
            if status.get('state') == 'success':
                # All checks succeeded
                _send_pr_check_success_notification(username, pr)


def process_pull_request(data):
    if data['action'] == 'labeled':
        reviews.process_pr_labeled(data)
    elif data['action'] == 'closed':
        reviews.process_pr_closed(data)
    # elif data['action'] == 'opened':
    #     github_jira.process_pr_opened(data)
    # elif data['action'] == 'edited':
    #     github_jira.process_pr_edited(data)


@app.route('/github-hook', methods=['POST'])
def github_hook():
    try:
        event_name = request.headers.get('X-Github-Event')
        if event_name == 'status':
            process_status(request.json)
        if event_name == 'pull_request':
            process_pull_request(request.json)
    except Exception as e:
        print(request.data)
        traceback.print_exc()
        raise e

    return "OK"


@app.route('/ping')
def ping():
    return "pong"

def _authorize_on_github(redirect_path):
    params = {
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': '{}/github-callback?next={}'.format(BASE_URL, redirect_path)
    }
    return redirect('https://github.com/login/oauth/authorize?{}'.format(urlencode(params)))


if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 80))
    app.run(host=host, port=port)