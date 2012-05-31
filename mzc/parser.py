from xml.dom.minidom import parse
from xml.dom import Node
from urllib2 import urlopen


def remove_whitespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text descendants of a DOM node."""

    remove_list = []
    for child in node.childNodes:
        if child.nodeType == Node.TEXT_NODE and not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whitespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()


class Parser(object):
    """General superclass for XML parsing."""

    url_path = "http://www.managerzone.com/xml/"

    def __init__(self, url_suffix):
        self.doc = parse(urlopen(self.url_path + url_suffix))
        remove_whitespace_nodes(self.doc, unlink=True)


class ManagerParser(Parser):
    """Parser subclass that reads manager data."""

    def __init__(self, url_suffix, use_tid=False):
        self.use_tid = use_tid
        if self.use_tid:
            self.url_path = "".join([Parser.url_path,
                                     "manager_data.php?sport_id=1&team_id="])
            self.tid = url_suffix
        else:
            self.url_path = "".join([Parser.url_path,
                                     "manager_data.php?sport_id=1&username="])
        self.doc = parse(urlopen(self.url_path + url_suffix))
        remove_whitespace_nodes(self.doc, True)

    def read_manager_data(self):
        try:
            self.user_data = dict(self.doc.firstChild.firstChild.
                                  attributes.items())
        except:
            self.user_data = {}
        try:
            self.team_data = dict(self.doc.firstChild.firstChild.firstChild.
                                  attributes.items())
        except:
            # Fails if it is run using a username instead of teamID.
            if self.use_tid:
                self.team_data = {u'teamId': self.tid}
        return self.user_data, self.team_data


class SeriesParser(Parser):
    """Parser subclass that reads standings and other series data."""

    url_path = "".join([Parser.url_path,
                        "team_league.php?sport_id=1&league_id="])

    def read_series_data(self):
        self.series = []
        for child in self.doc.firstChild.childNodes:
            self.series.append(dict(child.attributes.items()))
        return self.series


class PlayersParser(Parser):
    """Parser subclass that reads the players of a team."""

    url_path = "".join([Parser.url_path,
                        "team_playerlist.php?sport_id=1&team_id="])

    def read_players_data(self):
        self.payers = []
        for child in self.doc.firstChild.firstChild.childNodes:
            self.payers.append(dict(child.attributes.items()))

        return self.payers

    def read_currency(self):
        return self.doc.firstChild.firstChild.getAttribute('teamCurrency')

    def read_country(self):
        return self.doc.firstChild.firstChild.getAttribute('countryShortname')

    def read_team_name(self):
        return self.doc.firstChild.firstChild.getAttribute('teamName')


class MatchlistParser(Parser):
    """Parser subclass that reads played or scheduled matches."""

    def __init__(self, url_suffix, limit="500", played=True):
        self.status = "1" if played else "2"
        self.url_path = "".join([Parser.url_path,
                                 "team_matchlist.php?sport_id=1&limit=", limit,
                                 "&match_status=", self.status, "&team_id="])
        self.doc = parse(urlopen(self.url_path + url_suffix))
        remove_whitespace_nodes(self.doc, unlink=True)

    def read_full_list(self):
        self.matches = {}
        self.counter = 1  # Used to keep the match order.
        for child in self.doc.firstChild.childNodes:
            self.matches[child.getAttribute('id')] = dict(child.attributes.
                                                             items())
            self.matches[child.getAttribute('id')][u'home'] = \
                            dict(child.firstChild.attributes.items())
            self.matches[child.getAttribute('id')][u'away'] = \
                            dict(child.lastChild.attributes.items())
            self.matches[child.getAttribute('id')][u'order'] = self.counter
            self.counter += 1

        return self.matches

    def read_match(self, mid):
        self.match = {}
        for child in self.doc.firstChild.childNodes:
            if child.getAttribute('mid') == mid:
                self.match = dict(child.attributes.items())
                self.match[u'home'] = dict(child.firstChild.attributes.items())
                self.match[u'away'] = dict(child.lastChild.attributes.items())
                break


class MatchParser(Parser):
    """Parser subclass that reads information of a single match."""

    url_path = "".join([Parser.url_path,
                        "match_info.php?sport_id=1&match_id="])

    def read_match_data(self):
        self.match = dict(self.doc.firstChild.firstChild.attributes.items())
        self.match[u'home'] = dict(self.doc.firstChild.firstChild.
                                     firstChild.attributes.items())
        self.match[u'away'] = dict(self.doc.firstChild.firstChild.
                                     lastChild.attributes.items())

        #TODO: Add player list to match.
