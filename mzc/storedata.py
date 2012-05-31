from google.appengine.ext import db
import datetime


class StoreData(object):
    """Controls the saved data on the Datastore"""

    def __init__(self):
        pass


class Team(db.Model):
    username = db.StringProperty()
    userId = db.StringProperty()
    countryShortname = db.StringProperty()
    teamId = db.StringProperty()
    startDate = db.StringProperty()


class TeamDetails(db.Model):
    teamName = db.StringProperty()
    nameShort = db.StringProperty()
    seriesName = db.StringProperty()
    seriesId = db.StringProperty()
    playerQty = db.IntegerProperty()
    seniorQty = db.IntegerProperty()
    youthQty = db.IntegerProperty()
    foreignQty = db.IntegerProperty()
    sumS_salary = db.IntegerProperty()
    avgS_salary = db.FloatProperty()
    sum11_salary = db.IntegerProperty()
    avg11_salary = db.FloatProperty()
    sumS_value = db.IntegerProperty()
    avgS_value = db.FloatProperty()
    sumJ_value = db.IntegerProperty()
    avgJ_value = db.FloatProperty()
    sumT_value = db.IntegerProperty()
    avgT_value = db.FloatProperty()
    sum11_value = db.IntegerProperty()
    avg11_value = db.FloatProperty()
    sumS_age = db.IntegerProperty()
    avgS_age = db.FloatProperty()
    sumT_age = db.IntegerProperty()
    avgT_age = db.FloatProperty()
    sum11_age = db.IntegerProperty()
    avg11_age = db.FloatProperty()
    dateWritten = db.DateTimeProperty()


def save_team(t):
    team = db.get(db.Key.from_path('Team', t['teamId']))
    if not team:
        team = Team(key_name=t['teamId'],
                    username=t['username'], userId=t['userId'],
                    countryShortname=t['countryShortname'], teamId=t['teamId'],
                    startDate=t['startDate'])
        team.put()
        save_team_details(t, team.key())


def save_team_details(t, t_key):
    team_det = TeamDetails(parent=t_key)
    team_det.teamName = t['teamName']
    team_det.nameShort = t['nameShort']
    team_det.seriesName = t['seriesName']
    team_det.seriesId = t['seriesId']
    team_det.playerQty = t['nPla']
    team_det.seniorQty = t['nSen']
    team_det.youthQty = t['nJun']
    team_det.foreignQty = t['nFor']
    team_det.sumS_salary = t['sumS_salary']
    team_det.avgS_salary = t['avgS_salary']
    team_det.sum11_salary = t['sum11_salary']
    team_det.avg11_salary = t['avg11_salary']
    team_det.sumS_value = t['sumS_value']
    team_det.avgS_value = t['avgS_value']
    team_det.sumY_value = t['sumJ_value']
    team_det.avgY_value = t['avgJ_value']
    team_det.sumT_value = t['sumT_value']
    team_det.avgT_value = t['avgT_value']
    team_det.sum11_value = t['sum11_value']
    team_det.avg11_value = t['avg11_value']
    team_det.sumS_age = t['sumS_age']
    team_det.avgS_age = t['avgS_age']
    team_det.sumT_age = t['sumT_age']
    team_det.avgT_age = t['avgT_age']
    team_det.sum11_age = t['sum11_age']
    team_det.avg11_age = t['avg11_age']
    team_det.dateWritten = datetime.datetime.now()

    team_det.put()
