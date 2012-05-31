from mzc.parser import ManagerParser, PlayersParser
from mzc.currency import Currency


class Team(object):
    """MZ Team"""

    def __init__(self, user, use_tid=False):
        mp = ManagerParser(user, use_tid)
        self.user_data, self.team_data = mp.read_manager_data()
        pp = PlayersParser(self.team_data['teamId'])
        self.seniors = pp.read_players_data()
        self.currency = pp.read_currency()
        if not self.currency:
            self.currency = "USD"
        # Fix error of series with bot teams.
        if not 'countryShortname' in self.user_data:
            self.user_data[u'countryShortname'] = pp.read_country().upper()
            self.team_data[u'teamName'] = pp.read_team_name()
        self.juniors = []

    def to_int(self, data):
        for player in self.seniors:
            for d in data:
                player[d] = int(player[d])
        for player in self.juniors:
            for d in data:
                player[d] = int(player[d])

    def separate_juniors(self):
        i = 0
        while i < len(self.seniors):
            if self.seniors[i]['junior'] == '0':
                i += 1
            else:
                self.juniors.append(self.seniors.pop(i))

    def get_sum_avg(self, field, include_juniors=True):
        # Seniors
        self.team_data['sumS_' + field] = 0
        for j in self.seniors:
            self.team_data['sumS_' + field] += int(j[field])
        if len(self.seniors):
            self.team_data['avgS_' + field] = (self.team_data['sumS_' + field]
                                               / float(len(self.seniors)))
        else:
            self.team_data['avgS_' + field] = 0.0

        # Juniors
        if include_juniors:
            self.team_data['sumJ_' + field] = 0
            for j in self.juniors:
                self.team_data['sumJ_' + field] += int(j[field])
            if len(self.juniors):
                self.team_data['avgJ_' + field] = (self.team_data['sumJ_' +
                                          field] / float(len(self.juniors)))
            else:
                self.team_data['avgJ_' + field] = 0.0

            # Totals
            self.team_data['sumT_' + field] = (self.team_data['sumS_' + field]
                                           + self.team_data['sumJ_' + field])
            if len(self.seniors) + len(self.juniors):
                self.team_data['avgT_' + field] = (self.team_data['sumT_' +
                      field] / float(len(self.juniors) + len(self.seniors)))
            else:
                self.team_data['avgT_' + field] = 0.0

    def count_players(self):
        self.team_data['nSen'] = len(self.seniors)
        self.team_data['nJun'] = len(self.juniors)
        self.team_data['nPla'] = (self.team_data['nSen'] +
                                  self.team_data['nJun'])
        self.team_data['nFor'] = len([1 for d in self.seniors if
                                 d['countryShortname'] !=
                                 self.user_data['countryShortname'].lower()])

    def sort(self, by, reverse=True):
        self.seniors.sort(key=lambda k: k[by], reverse=reverse)
        self.juniors.sort(key=lambda k: k[by], reverse=reverse)

    def get_max(self, field, include_juniors=True):
        self.sort(field, reverse=True)
        if (self.juniors and include_juniors and
           self.juniors[0][field] > self.seniors[0][field]):
            self.team_data['max_' + field] = [self.juniors[0]['name'],
                                              self.juniors[0][field]]
        elif self.seniors:
            self.team_data['max_' + field] = [self.seniors[0]['name'],
                                              self.seniors[0][field]]
        else:
            self.team_data['max_' + field] = ["-", 0]

    def get_min(self, field, include_juniors=True):
        self.sort(field, reverse=False)
        if (self.juniors and include_juniors and
           self.juniors[0][field] < self.seniors[0][field]):
            self.team_data['min_' + field] = [self.juniors[0]['name'],
                                              self.juniors[0][field]]
        elif self.seniors:
            self.team_data['min_' + field] = [self.seniors[0]['name'],
                                              self.seniors[0][field]]
        else:
            self.team_data['min_' + field] = ["-", 0]

    def get_top_11_data(self):
        # Run before separating juniors.
        self.team_data['sum11_value'] = 0
        self.team_data['sum11_salary'] = 0
        self.team_data['sum11_age'] = 0
        self.sort('value', reverse=True)
        for i in self.seniors[:11]:
            self.team_data['sum11_value'] += int(i['value'])
            self.team_data['sum11_salary'] += int(i['salary'])
            self.team_data['sum11_age'] += int(i['age'])
        length = float(len(self.seniors[:11]))
        if length != 0:
            self.team_data['avg11_value'] = (self.team_data['sum11_value'] /
                                             length)
            self.team_data['avg11_salary'] = (self.team_data['sum11_salary'] /
                                              length)
            self.team_data['avg11_age'] = self.team_data['sum11_age'] / length
        else:
            self.team_data['avg11_value'] = 0
            self.team_data['avg11_salary'] = 0
            self.team_data['avg11_age'] = 0

    def convert_currency(self, target):
        # Run before separating juniors.
        if target != self.currency:
            c = Currency(self.currency)
            for s in self.seniors:
                s['salary'] = c.convert_to(target, s['salary'])
                s['value'] = c.convert_to(target, s['value'])

        self.currency = target
