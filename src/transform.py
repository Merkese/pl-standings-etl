from src.extract import get_standings, league_details
import pandas as pd


def get_latestSeason():
    """
    Returns the latest season start year from API response

    """
    response = league_details()

    season = response["latestSeason"]
    
    season.split("/")
    
    season = int(season[0:4]) 

    return season

LATEST_SEASON = get_latestSeason()

def standings_trfm():
    """ 
    Uses get_standings() to transform response data into a pandas dataFrame
    """
    # api response
    response = get_standings()

    rows = []

    # Used for gathering specific columns/attributes from response data 
    column_names = ['season','position','team_id','team','played', 'won', 'draw', 'lost', 'score_streak', 'goal_diff', 'points']

    # iterates over response data and adds each row to a tuple 
    for club in response:
        season          = LATEST_SEASON
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

    # Creates standings DataFrame
    teamData = pd.DataFrame(rows, columns=column_names)
    return teamData

