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
    sumY_value = db.IntegerProperty()
    avgY_value = db.FloatProperty()
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
    teamDet = TeamDetails(parent=t_key)
    teamDet.teamName = t['teamName']
    teamDet.nameShort = t['nameShort']
    teamDet.seriesName = t['seriesName']
    teamDet.seriesId = t['seriesId']  
    teamDet.playerQty = t['nJug']
    teamDet.seniorQty = t['nMay']
    teamDet.youthQty = t['nJuv']
    teamDet.foreignQty = t['nExt']
    teamDet.sumS_salary = t['sumM_salary']
    teamDet.avgS_salary = t['avgM_salary']
    teamDet.sum11_salary = t['sum11_salary']
    teamDet.avg11_salary = t['avg11_salary']
    teamDet.sumS_value = t['sumM_value']
    teamDet.avgS_value = t['avgM_value']
    teamDet.sumY_value = t['sumJ_value']
    teamDet.avgY_value = t['avgJ_value']
    teamDet.sumT_value = t['sumT_value']
    teamDet.avgT_value = t['avgT_value']
    teamDet.sum11_value = t['sum11_value']
    teamDet.avg11_value = t['avg11_value']
    teamDet.sumS_age = t['sumM_age']
    teamDet.avgS_age = t['avgM_age']
    teamDet.sumT_age = t['sumT_age']
    teamDet.avgT_age = t['avgT_age']
    teamDet.sum11_age = t['sum11_age']
    teamDet.avg11_age = t['avg11_age']
    teamDet.dateWritten = datetime.datetime.now()
    
    teamDet.put()