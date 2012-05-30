from mzc.parser import MatchlistParser, MatchParser


def get_teams_from_match(tid, mid, limit="500", played=True):
    if played:
        mp = MatchParser(mid)
        mp.read_match_data()
        team_ids = [mp.matchDict['home']['id'], mp.matchDict['away']['id']]
    else:
        mlp = MatchlistParser(tid, limit, played)
        mlp.read_match(mid)
        team_ids = [mlp.matchDict['home']['teamId'],
                    mlp.matchDict['away']['teamId']]

    if tid and tid != team_ids[0]:
        team_ids.reverse()

    return team_ids


def get_match_dict(tid, limit="500", played=True):
    mlp = MatchlistParser(tid, limit, played)
    mlp.read_full_list()
    return mlp.matchesDict
