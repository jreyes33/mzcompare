import os

from google.appengine.dist import use_library
use_library('django', '1.2')

from django.conf import settings    # Force reload settings (conf/settings.py)
from django.utils import translation
from django.utils.formats import _format_cache  # Dirty fix for settings
os.environ['DJANGO_SETTINGS_MODULE'] = "conf.settings"
settings._target = None

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from mzc.comparal import ComparaLiga
from mzc.tcompare import TeamCompare
from mzc.compare import get_teams_from_match, get_match_dict
from mzc.storedata import save_team
from cookies import Cookies


class I18NRequestHandler(webapp.RequestHandler):

    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.request.COOKIES = Cookies(self)
        self.request.META = os.environ
        self.reset_language()

    def reset_language(self):
        # Decide the language from Cookies/Headers
        language = translation.get_language_from_request(self.request)
        # Dirty fix for settings
        cache_key = ('THOUSAND_SEPARATOR', language)
        _format_cache[cache_key] = ";psbn&"
        cache_key = ('DECIMAL_SEPARATOR', language)
        _format_cache[cache_key] = "."
        translation.activate(language)
        self.request.LANGUAGE_CODE = translation.get_language()
        # Set headers in response
        self.response.headers['Content-Language'] = translation.get_language()
        # translation.deactivate()


class StaticPage(I18NRequestHandler):
    """Serves 'static' pages"""
    
    def get(self, page):
        lang = self.request.get('l')
        if lang:
            self.request.COOKIES.set_cookie("language", lang)
            self.redirect("./" + page, permanent=True)
        if not page:
            page = "index.html"
        elif not page.endswith(".html"):
            page = "".join([page, ".html"])
        self.langDict = {'en': "en_US",
                         'es': "es_ES",
                         'pt': "pt_BR",
                         'id': "id_ID",
                         'sv': "sv_SE"}
        try:
            self.langFB = self.langDict[translation.get_language()[:2]]
        except:
            self.langFB = "en_US"
        path = os.path.join(os.path.dirname(__file__), "templates", page)
        self.response.out.write(template.render(path,
                      {'langFB': self.langFB}))


class MatchCompare(I18NRequestHandler):
    """Runs the script for a specific match"""
    
    def get(self):
        self.tid = self.request.get('tid')
        self.mid = self.request.get('mid')
        self.jug = bool(int(self.request.get('played')))
        teamIds = get_teams_from_match(self.tid, self.mid, jugados=self.jug)
        self.redirect("./mzc:" + ",".join(teamIds), permanent=True)


class MatchList(I18NRequestHandler):
    """Returns the list of played or scheduled matches"""
    
    def get(self):
        self.tid = self.request.get('tid')
        self.jug = bool(int(self.request.get('played')))
        matchList = get_match_dict(self.tid, jugados=self.jug).values()
        path = os.path.join(os.path.dirname(__file__),
                            "templates", "matches.html")
        self.response.out.write(template.render(path,
                                {'matches': matchList,
                                 'played': self.jug,
                                 'tid': self.tid}))


class Compare(I18NRequestHandler):
    """Runs the script using to usernames passed"""
    
    def get(self, teams):
        try:
            lang = self.request.get('l')
            getTeams = self.request.get_all('u')
            teams = teams.split('%2C')
            while '' in teams:
                teams.remove('')
            temp = []
            for t in teams:
                if not t in temp:
                    t = t.replace("%20", "").strip()    #Delete spaces
                    temp.append(t)
            teams = temp
            if lang:
                self.request.COOKIES.set_cookie("language", lang)
            if getTeams:
                self.redirect("./mzc:" + ",".join(getTeams), permanent=True)
            elif lang:
                self.redirect("./mzc:" + ",".join(teams), permanent=True)
            elif len(teams) == 1:
                cL = ComparaLiga(teams[0])
                standings = cL.getStandings()
                teamsList, teamId = cL.getTeams()
                for t in teamsList:
                    save_team(t)
                path = os.path.join(os.path.dirname(__file__),
                                    "templates", "oneTeam.html")
                self.response.out.write(template.render(path,
                                            {'standings': standings,
                                             'teams': teamsList,
                                             'teamId': teamId}))
            elif len(teams) == 2:
                cE = TeamCompare(teams)
                teamsList, teamId = cE.getTeams()
                path = os.path.join(os.path.dirname(__file__),
                                    "templates", "twoTeams.html")
                self.response.out.write(template.render(path,
                                            {'teams': teamsList,
                                             'teamId': teamId}))
            elif teams and len(teams) <= 6:
                cE = TeamCompare(teams)
                teamsList, teamId = cE.getTeams()
                path = os.path.join(os.path.dirname(__file__),
                                    "templates", "moreTeams.html")
                self.response.out.write(template.render(path,
                                            {'teams': teamsList,
                                             'teamId': teamId}))
            else:
                raise Exception
        except:
            path = os.path.join(os.path.dirname(__file__),
                                "templates", "error.html")
            self.response.out.write(template.render(path, {}))


def main():    
    application = webapp.WSGIApplication([(r'/mzc%3A(.*)', Compare),
                                          (r'/compare(.*)', Compare),
                                          ('/matches', MatchList),
                                          ('/match', MatchCompare),
                                          (r'/(.*)', StaticPage),
                                         ],
                                         debug=False)
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()