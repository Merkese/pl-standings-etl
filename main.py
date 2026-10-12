from src.transform import standings_trfm
from src.load import load_standings


def main():
    standings_df = standings_trfm()
    result = load_standings(standings_df)
    print(result)


if __name__ == "__main__":
    main()
