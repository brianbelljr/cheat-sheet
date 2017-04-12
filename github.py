import os
import json
import urlparse

import requests

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN must be specified in the environment")


def get(path, access_token=GITHUB_TOKEN):
    uri = urlparse.urljoin("https://api.github.com", path)
    response = requests.get(
        uri,
        headers={
            'Authorization': 'token {}'.format(access_token)
        }
    )
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise RuntimeError("Could not get data from github ({}): {}\n{}".format(
            uri,
            response.status_code,
            response.text
        ))


def post(path, data):
    uri = urlparse.urljoin("https://api.github.com", path)
    response = requests.post(
        uri,
        data=json.dumps(data),
        headers={
            'Authorization': 'token {}'.format(GITHUB_TOKEN)
        }
    )
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise RuntimeError("Could not post data to github ({}): {}\n{}".format(
            uri,
            response.status_code,
            response.text
        ))


def patch(path, data):
    uri = urlparse.urljoin("https://api.github.com", path)
    response = requests.patch(
        uri,
        data=json.dumps(data),
        headers={
            'Authorization': 'token {}'.format(GITHUB_TOKEN)
        }
    )
    if response.status_code in [200, 201]:
        return json.loads(response.text)
    else:
        raise RuntimeError("Could not post data to github ({}): {}\n{}".format(
            uri,
            response.status_code,
            response.text
        ))


def delete(path):
    uri = urlparse.urljoin("https://api.github.com", path)
    response = requests.delete(
        uri,
        headers={
            'Authorization': 'token {}'.format(GITHUB_TOKEN)
        }
    )
    if response.status_code in [200, 204]:
        return None
    else:
        raise RuntimeError("Could not post DELETE request to github ({}): {}\n{}".format(
            uri,
            response.status_code,
            response.text
        ))