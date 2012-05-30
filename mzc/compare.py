from mzc.parser import MatchlistParser, MatchParser

def get_teams_from_match(tid, mid, limite="500", jugados=True):
    if jugados:
        lp = MatchParser(mid)
        lp.read_match_data()
        teamIds = [lp.matchDict['home']['id'], lp.matchDict['away']['id']]
    else:
        llp = MatchlistParser(tid, limite, jugados)
        llp.read_match(mid)
        teamIds = [llp.matchDict['home']['teamId'], llp.matchDict['away']['teamId']]
    
    if tid and tid != teamIds[0]:
        teamIds.reverse()
    
    return teamIds

def get_match_dict(tid, limite="500", jugados=True):
    llp = MatchlistParser(tid, limite, jugados)
    llp.read_full_list()
    return llp.matchesDict