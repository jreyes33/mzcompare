from xml.dom.minidom import parse
from xml.dom import Node
from urllib2 import urlopen

def remove_whitespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node."""

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

    URLPath = "http://www.managerzone.com/xml/"

    def __init__(self, URLSuffix):
        self.doc = parse(urlopen(self.URLPath + URLSuffix))
        remove_whitespace_nodes(self.doc, unlink=True)


class ManagerParser(Parser):
    """Parser subclass that reads manager data."""

    def __init__(self, URLSuffix, usingTeamID=False):
        self.usingTeamID = usingTeamID
        if self.usingTeamID:
            self.URLPath = "".join([Parser.URLPath,\
                                    "manager_data.php?sport_id=1&team_id="])
            self.tID = URLSuffix
        else:
            self.URLPath = "".join([Parser.URLPath,\
                                    "manager_data.php?sport_id=1&username="])
        self.doc = parse(urlopen(self.URLPath + URLSuffix))
        remove_whitespace_nodes(self.doc, True)

    def read_manager_data(self):
        try:
            self.userDataDict = dict(self.doc.firstChild.firstChild.\
                                    attributes.items())
        except:
            self.userDataDict = {}
        try:
            self.teamDict = dict(self.doc.firstChild.firstChild.firstChild.\
                                attributes.items())
        except:
            # Fails if it is run using a username instead of teamID.
            if self.usingTeamID:
                self.teamDict = {u'teamId': self.tID}
        return self.userDataDict, self.teamDict


class SeriresParser(Parser):
    """Parser subclass that reads standings and other series data."""

    URLPath = "".join([Parser.URLPath,\
                       "team_league.php?sport_id=1&league_id="])

    def read_series_data(self):
        self.seriesList = []
        for child in self.doc.firstChild.childNodes:
            self.seriesList.append(dict(child.attributes.items()))
        return self.seriesList


class PlayersParser(Parser):
    """Parser subclass that reads the players of a team."""

    URLPath = "".join([Parser.URLPath,\
                       "team_playerlist.php?sport_id=1&team_id="])

    def read_players_data(self):
        self.playersList = []
        for child in self.doc.firstChild.firstChild.childNodes:
            self.playersList.append(dict(child.attributes.items()))
        return self.playersList

    def read_currency(self):
        return self.doc.firstChild.firstChild.getAttribute('teamCurrency')

    def read_country(self):
        return self.doc.firstChild.firstChild.getAttribute('countryShortname')

    def read_team_name(self):
        return self.doc.firstChild.firstChild.getAttribute('teamName')


class MatchlistParser(Parser):
    """Parser subclass that reads played or scheduled matches."""

    def __init__(self, URLSuffix, limit="500", played=True):
        self.status = "1" if played else "2"
        self.URLPath = "".join([Parser.URLPath,
                                "team_matchlist.php?sport_id=1&limit=", limit,
                                "&match_status=", self.status, "&team_id="])
        self.doc = parse(urlopen(self.URLPath + URLSuffix))
        remove_whitespace_nodes(self.doc, unlink=True)

    def read_full_list(self):
        self.matchesDict = {}
        self.counter  = 1  # Used to keep the match order.
        for child in self.doc.firstChild.childNodes:
            self.matchesDict[child.getAttribute('id')] = dict(child.attributes.
                                                             items())
            self.matchesDict[child.getAttribute('id')][u'home'] = \
                            dict(child.firstChild.attributes.items())
            self.matchesDict[child.getAttribute('id')][u'away'] = \
                            dict(child.lastChild.attributes.items())
            self.matchesDict[child.getAttribute('id')][u'order'] = self.counter
            self.counter += 1

        return self.matchesDict

    def read_match(self, mid):
        self.matchDict = {}
        for child in self.doc.firstChild.childNodes:
            if child.getAttribute('mid') == mid:
                self.matchDict = dict(child.attributes.items())
                self.matchDict[u'home'] = dict(child.firstChild.attributes.
                                             items())
                self.matchDict[u'away'] = dict(child.lastChild.attributes.
                                             items())
                break


class MatchParser(Parser):
    """Parser subclass that reads information of a single match."""

    URLPath = "".join([Parser.URLPath,\
                       "match_info.php?sport_id=1&match_id="])

    def read_match_data(self):
        self.matchDict = dict(self.doc.firstChild.firstChild.attributes.items())
        self.matchDict[u'home'] = dict(self.doc.firstChild.firstChild.
                                     firstChild.attributes.items())
        self.matchDict[u'away'] = dict(self.doc.firstChild.firstChild.
                                     lastChild.attributes.items())

        #TODO: Add player list to matchDict.
