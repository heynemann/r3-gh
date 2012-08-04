#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2

from ujson import loads

class Stream:
    job_type = 'percentage'
    group_size = 10

    def process(self, app, arguments):
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
    print "%d - getting %s..." % (index, url)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    next_url = None
    if 'link' in response.headers:
        link = response.headers['link']
        if 'next' in link:
            next_url = link.split(',')[0].split(';')[0][1:-1]
    return response.read(), next_url


if __name__ == '__main__':
    user = sys.argv[1]
    project = sys.argv[2]
    print get_repo_commits(user, project)

