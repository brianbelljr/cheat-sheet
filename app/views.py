#!/usr/bin/env python
import io
import os
import re
import sys
import json
import subprocess
import requests
import ipaddress
import hmac
from hashlib import sha1
from flask import Flask, request, abort
from app import app
import os
import re
import json
import traceback
from urllib import urlencode

import requests

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/github-hook/', methods=['GET'])
def reply():
    out = requests.get('https://api.github.com/')
    parsed = json.loads(out.text)
    return json.dumps(parsed, indent=4, sort_keys=True)

@app.route('/github-hook/', methods=['POST'])
def github_hook():
    try:
        # Store the IP address of the requester
        request_ip = ipaddress.ip_address(u'{0}'.format(request.remote_addr))

        event_name = request.headers.get('X-Github-Event')
        #if event_name == 'status':
        #    github_hooks.process_status(request.json)
        if event_name == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event_name == 'pull_request':
            github_hooks.process_pull_request(request.json)
    except Exception as e:
        print(request.data)
        traceback.print_exc()
        raise e

    return "OK"

@app.route('/login', methods=['GET'])
def login():
    return github.authorize()


# @github.access_token_getter
# def token_getter():
#     return session.get('oauth_token', None)


# @app.route('/github/callback')
# @github.authorized_handler
# def github_authorized(oauth_token):
#     if oauth_token is None:
#         flash("Authorization failed.")
#         return redirect(url_for('index'))

#     session['oauth_token'] = oauth_token

#     me = github.get('user')
#     user_id = me['login']

#     # is user exist
#     user = User.query.get(user_id)

#     if user is None:
#         # not exist, add
#         user = User(id=user_id)

#     # update github user information
#     user.last_login = DateUtil.now_datetime()
#     user.name = me.get('name', user_id)
#     user.location = me.get('location', '')
#     user.avatar = me.get('avatar_url', '')

#     user.save()

#     RequestUtil.login_user(user.dict())

#     return redirect(url_for('index'))


@app.route('/logout', methods=['GET'])
def logout():
    RequestUtil.logout()
    return redirect(url_for('index'))