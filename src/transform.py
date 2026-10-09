from extract import get_standings
import pandas as pd



def standings_trfm():
    """ Uses get_standings() to transform into a pandas dataFrame"""

    response = get_standings()

    rows = []
    
    column_names = ['season','position','team_id','team','played', 'won', 'draw', 'lost', 'score_streak', 'goal_diff', 'points']


    for club in response:
        season          = 2025
        position        = club["idx"]
        team_id         = club["id"]
        team            = club["name"]
        played          = club["played"]
        won             = club["wins"]
        draw            = club["draws"]
        lost            = club["losses"]
        score_streak    = club["scoresStr"]
        goals_diff      = club["goalConDiff"]
        points          = club["pts"]

        tuple_of_club = (season, position, team_id, team, played, won, draw, lost, score_streak, goals_diff, points)
        
        rows.append(tuple_of_club)

        teamData = pd.DataFrame(rows, columns=column_names)
    return teamData
