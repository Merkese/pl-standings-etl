import os
import psycopg as pg
from dotenv import load_dotenv

def load_standings(standings_df): 
    """ 
    Loads standings data into standings table via Postgre. This assumes you have created the suggested schema and table as named within the function 
    """
    load_dotenv()

    # Grabs credentials from env
    PGHOST = os.getenv("host")
    PGPORT = os.getenv("port")
    PGUSER = os.getenv("username")
    PGPASS = os.getenv("pass")
    PGDB = os.getenv("dbname")

    # dataframe reference (standings_df)
    table_cols = ['season','position','team_id','team','played', 'won', 'draw', 'lost', 'score_streak', 'goal_diff', 'points']

    # Used to assign each dataframe row into standard tuples (see last cell to unpack) 
    standings_records_tuples = standings_df[table_cols].itertuples(index= False, name= None)

    # Data upsert query to insert records into postgre "standings" table 
    UPSERT_SQL = """
    INSERT INTO staging.standings (
    season, position, team_id, team, played, won, draw, lost, score_streak, goal_diff, points

    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    ON CONFLICT (season, team_id) DO UPDATE SET

    position        = EXCLUDED.position,
    team            = EXCLUDED.team,
    played          = EXCLUDED.played,
    won             = EXCLUDED.won,
    draw            = EXCLUDED.draw,
    lost            = EXCLUDED.lost,
    score_streak    = EXCLUDED.score_streak,
    goal_diff       = EXCLUDED.goal_diff,
    points          = EXCLUDED.points;
"""
    # Used to store each tuple and count of rows
    list_standings_tuple = list(standings_records_tuples)

    num_of_updated_rows = len(list_standings_tuple)

    # Connects to database and initialize cursor, will rollback on 
    with pg.connect( 
            dbname= PGDB,
            user= PGUSER,
            password= PGPASS,
            host= PGHOST,
            port= PGPORT) as conn:
        
        # Creates cursor
        cursor = conn.cursor()
        

        # Checks if table exists
        cursor.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'staging' AND table_name = %s
                )
                """, ("standings",)
            )
        table_check = cursor.fetchone()[0]
        if not table_check:
            raise ValueError(f"The table staging.standings was not found")
        
        # Executes upsert query (will automatically commit on exit and rollback on error)
        cursor.executemany(UPSERT_SQL, list_standings_tuple)
        return f"Upsert completed - {num_of_updated_rows} added. "

