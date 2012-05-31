from mzc.group import Group


class CompareTeams(object):
    """Class that uses the rest of objects in MZ Compare to compare teams"""

    def __init__(self, usernames):
        self.usernames = usernames
        self.g = Group(self.usernames)
        self.g.get_details()
        self.g.convert_currency()
        for t in self.g.teams_list:
            t.to_int(['age', 'birthDay', 'birthSeason', 'salary', 'value'])
            t.get_top_11_data()
            t.separate_juniors()
            t.count_players()
            t.get_sum_avg('age', True)
            t.get_sum_avg('value', True)
            t.get_sum_avg('salary', False)
            if len(self.usernames) == 2:
                t.get_max('age', True)
                t.get_max('salary', True)
                t.get_max('value', True)

    def get_teams(self):
        self.teams = []
        for t in self.g.teams_list:
            t.team_data['players'] = []
            t.team_data['players'].extend(t.seniors)
            t.team_data['players'].extend(t.juniors)
            self.teams.append(t.team_data)
            if t.team_data['teamId'] == self.g.team_data['teamId']:
                t.team_data['highlight'] = True

        return self.teams, self.g.teams_list[0].team_data['teamId']
