from mzc.series import Series


class CompareSeries(object):
    """Class to control and use the rest of objects in MZ Compare"""

    def __init__(self, username):
        self.username = username
        self.s = Series(self.username)
        self.s.get_details()
        for t in self.s.teams_list:
            t.to_int(['age', 'birthDay', 'birthSeason', 'salary', 'value'])
            t.get_top_11_data()
            t.separate_juniors()
            t.count_players()
            t.get_sum_avg('age', include_juniors=True)
            t.get_sum_avg('value', include_juniors=True)
            t.get_sum_avg('salary', include_juniors=False)

    def get_standings(self):
        return self.s.standings

    def get_teams(self):
        self.teams = []
        for t in self.s.teams_list:
            t.team_data = dict(t.team_data.items() + t.user_data.items())
            t.team_data['players'] = []
            t.team_data['players'].extend(t.seniors)
            t.team_data['players'].extend(t.juniors)
            self.teams.append(t.team_data)
            if t.team_data['teamId'] == self.s.team_data['teamId']:
                t.team_data['highlight'] = True

        return self.teams, self.s.team_data['teamId']
