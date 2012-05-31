from mzc.parser import MatchlistParser, MatchParser


def get_teams_from_match(tid, mid, limit="500", played=True):
    if played:
        mp = MatchParser(mid)
        mp.read_match_data()
        team_ids = [mp.match['home']['id'], mp.match['away']['id']]
    else:
        mlp = MatchlistParser(tid, limit, played)
        mlp.read_match(mid)
        team_ids = [mlp.match['home']['teamId'],
                    mlp.match['away']['teamId']]

    if tid and tid != team_ids[0]:
        team_ids.reverse()

    return team_ids


def get_match_dict(tid, limit="500", played=True):
    mlp = MatchlistParser(tid, limit, played)
    mlp.read_full_list()
    return mlp.matches
