#!/usr/bin/python
# -*- coding: utf-8 -*-


from r3.worker.mapper import Mapper

class CommitsPercentageMapper(Mapper):
    job_type = 'percentage'

    def map(self, commits):
        return list(self.split_commits(commits))

    def split_commits(self, commits):
        if commits is None:
            import ipdb;ipdb.set_trace()
        for commit in commits:
            commit = commit['commit']
            yield commit['committer']['email'], 1
