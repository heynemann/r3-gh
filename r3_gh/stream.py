#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists, join, dirname
from urlparse import urlparse
import os
import sys
import urllib2

from ujson import loads

CACHE_PATH = '/tmp/r3-gh-cache'

class Stream:
    job_type = 'percentage'
    group_size = 10

    def process(self, app, arguments):
        if not exists(CACHE_PATH):
            os.makedirs(CACHE_PATH)
        user = arguments['user'][0]
        repo = arguments['repo'][0]

        return get_repo_commits(user, repo)

def get_repo_commits(user, repo):
    next_url = 'https://api.github.com/repos/%s/%s/commits?per_page=100' % (user, repo)
    commits = []
    index = 0

    while next_url:
        index += 1
        content, next_url = get_url_content(next_url, index)
        json = loads(content)
        for item in json:
            commits.append(item)

    return commits

def get_url_content(url, index):
    parts = urlparse(url)

    url_path = join(parts.path.lstrip('/'), parts.query.replace('&', '/').replace('=','_'))
    cache_path = join(CACHE_PATH, url_path, 'contents.json')
    next_path = join(CACHE_PATH, url_path, 'next.json')

    if exists(cache_path) and exists(next_path):
        print "%d - %s found in cache!" % (index, url)
        with open(cache_path) as cache_file:
            with open(next_path) as next_file:
                return cache_file.read(), next_file.read()

    print "%d - getting %s..." % (index, url)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    contents = response.read()
    print "%d - storing in cache" % index

    if not exists(dirname(cache_path)):
        os.makedirs(dirname(cache_path))

    with open(cache_path, 'w') as cache_file:
        cache_file.write(contents)

    next_url = None
    if 'link' in response.headers:
        link = response.headers['link']
        if 'next' in link:
            next_url = link.split(',')[0].split(';')[0][1:-1]

    if next_url is not None:
        with open(next_path, 'w') as next_file:
            next_file.write(next_url)

    return contents, next_url


if __name__ == '__main__':
    user = sys.argv[1]
    project = sys.argv[2]
    print get_repo_commits(user, project)

