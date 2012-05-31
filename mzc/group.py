from mzc.parser import ManagerParser
from mzc.team import Team


class Group(object):
    """Class for managing comparisons between several teams."""

    def __init__(self, usernames):
        self.usernames = usernames
        self.users = {}
        for u in reversed(self.usernames):
            mp = ManagerParser(u, use_tid=u.isdigit())
            self.user_data, self.team_data = mp.read_manager_data()
            self.users[u] = self.user_data

    def get_details(self):
        self.teams_list = []
        for u in self.usernames:
            t = Team(u, use_tid=u.isdigit())
            # Adds missing fields
            t.team_data['username'] = self.users[u]['username']
            t.team_data['teamCurrency'] = t.currency
            t.team_data['countryShortname'] = (self.users[u]
                                               ['countryShortname'].lower())
            self.teams_list.append(t)

    def convert_currency(self):
        for t in self.teams_list[1:]:
            if t.currency != self.teams_list[0].currency:
                t.convert_currency(self.teams_list[0].currency)
