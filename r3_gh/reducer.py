#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict

class Reducer:
    job_type = 'percentage'

    def reduce(self, app, items):
        commits_per_user = defaultdict(int)
        total_commits = 0

        for commit in items:
            for user_data in commit:
                login = user_data[0]
                frequency = user_data[1]
                commits_per_user[login] += frequency
                total_commits += frequency

        percentages = {}
        for login, frequency in commits_per_user.iteritems():
            percentages[login] = float(frequency) / float(total_commits)

        return {
            'total_commits': total_commits,
            'commit_percentages': percentages
        }
