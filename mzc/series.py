from mzc.parser import SeriesParser, ManagerParser
from mzc.team import Team


class Series(object):
    """official MZ series"""

    def __init__(self, user):
        mp = ManagerParser(user, use_tid=user.isdigit())
        self.user_data, self.team_data = mp.read_manager_data()
        ll = SeriesParser(self.team_data['seriesId'])
        self.standings = ll.read_series_data()

    def to_int(self, data):
        for team in self.standings:
            for d in data:
                team[d] = int(team[d])

    def sort(self, by, reverse=True):
        self.standings.sort(key=lambda k: k[by], reverse=reverse)

    def get_details(self):
        self.teams_list = []
        for i in self.standings:
            t = Team(i['teamId'], use_tid=True)
            t.team_data['teamCurrency'] = t.currency
            self.teams_list.append(t)
