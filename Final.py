import csv        # Read CSV files
import os          # Build file paths
import unicodedata # Handle special characters in player names


# ─────────────────────────────────────────
#  LOAD THE CSV FILE
# ─────────────────────────────────────────

def load_data(filename):
    players = []

    # Build the full path so the file loads correctly regardless of where the script is run from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    try:
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Each row becomes a dictionary keyed by column name
            for row in reader:
                players.append(row)
        print(f"Data loaded successfully — {len(players)} players found.\n")

    except FileNotFoundError:
        print(f"ERROR: Could not find '{filepath}'. Make sure nba_stats.csv is in the same folder as this script.")

    return players


# ─────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────

def show_menu():
    print("=" * 40)
    print("   NBA 2025-26 Season Stats Analyzer")
    print("=" * 40)
    print("1. Look up a player by name")
    print("2. View top 5 leaders in a stat category")
    print("3. Compare two players side by side")
    print("4. Filter players by team")
    print("5. Quit")
    print("=" * 40)


# ─────────────────────────────────────────
#  OPTION 1 — LOOK UP A PLAYER BY NAME
# ─────────────────────────────────────────

def lookup_player(players):
    name = input("\nEnter the player's full name: ").strip().lower()

    for player in players:
        if strip_accents(player["Player"]).lower() == strip_accents(name):
            print("\n" + "-" * 35)
            print(f"  {player['Player']} — {player['Team']} | {player['Pos']}")
            print("-" * 35)
            print(f"  Points per game:       {player['PTS']}")
            print(f"  Rebounds per game:     {player['TRB']}")
            print(f"  Assists per game:      {player['AST']}")
            print(f"  Field goal %:          {player['FG%']}")
            print("-" * 35 + "\n")
            return

    print(f"\nPlayer '{name.title()}' not found. Check the spelling and try again.\n")


# ─────────────────────────────────────────
#  OPTION 2 — TOP 5 STAT LEADERS
# ─────────────────────────────────────────

def top_five_leaders(players):
    print("\nStat Categories:")
    print("  1. Points Per Game")
    print("  2. Rebounds Per Game")
    print("  3. Assists Per Game")
    print("  4. Steals Per Game")
    print("  5. Blocks Per Game")

    choice = input("\nEnter your choice (1-5): ").strip()

    # Map the user's choice to the CSV column name and a display label
    if choice == "1":
        column, label = "PTS", "Points Per Game"
    elif choice == "2":
        column, label = "TRB", "Rebounds Per Game"
    elif choice == "3":
        column, label = "AST", "Assists Per Game"
    elif choice == "4":
        column, label = "STL", "Steals Per Game"
    elif choice == "5":
        column, label = "BLK", "Blocks Per Game"
    else:
        print("\nInvalid choice.\n")
        return

    # Sort highest to lowest — float() converts text values to numbers for correct ordering
    # "or 0" handles blank cells so float() doesn't crash on empty strings
    sorted_players = sorted(players, key=lambda p: float(p[column] or 0), reverse=True)

    print(f"\n  Top 5 in {label}:")
    print("-" * 35)
    for i in range(5):
        player = sorted_players[i]
        print(f"  {i + 1}. {player['Player']:<25} {player[column]}")
    print("-" * 35 + "\n")


# ─────────────────────────────────────────
#  OPTION 3 — COMPARE TWO PLAYERS
# ─────────────────────────────────────────

# Strips accent marks so "doncic" matches "Dončić"
def strip_accents(text):
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")


# Searches the player list and returns the matching player, or None if not found
def find_player(players, name):
    for player in players:
        if strip_accents(player["Player"]).lower() == strip_accents(name).lower():
            return player
    return None


def compare_players(players):
    name1 = input("\nEnter the first player's full name: ").strip()
    name2 = input("Enter the second player's full name: ").strip()

    player1 = find_player(players, name1)
    player2 = find_player(players, name2)

    if not player1:
        print(f"\nCould not find '{name1}'. Check the spelling and try again.\n")
        return
    if not player2:
        print(f"\nCould not find '{name2}'. Check the spelling and try again.\n")
        return

    p1 = player1['Player']
    p2 = player2['Player']

    # :<22 and :<26 left-align text in fixed-width columns to keep the table neat
    print(f"\n  {'STAT':<22} {p1:<26} {p2}")
    print("-" * 70)
    print(f"  {'Points per game':<22} {player1['PTS']:<26} {player2['PTS']}")
    print(f"  {'Rebounds per game':<22} {player1['TRB']:<26} {player2['TRB']}")
    print(f"  {'Assists per game':<22} {player1['AST']:<26} {player2['AST']}")
    print(f"  {'Field goal %':<22} {player1['FG%']:<26} {player2['FG%']}")
    print("-" * 70 + "\n")


# ─────────────────────────────────────────
#  OPTION 4 — FILTER PLAYERS BY TEAM
# ─────────────────────────────────────────

def filter_by_team(players):
    team = input("\nEnter team abbreviation (e.g. LAL, OKC, BOS): ").strip().upper()

    # Collect all players on the team
    roster = []
    for player in players:
        if player["Team"] == team:
            roster.append(player)

    if not roster:
        print(f"\nNo players found for '{team}'. Make sure you're using the correct abbreviation.\n")
        return

    print(f"\n  Players on {team}:")
    print("-" * 55)
    print(f"  {'Name':<25} {'Pos':<5} {'PTS':<7} {'TRB':<7} {'AST':<7} {'FG%'}")
    print("-" * 55)
    for player in roster:
        print(f"  {player['Player']:<25} {player['Pos']:<5} {player['PTS']:<7} {player['TRB']:<7} {player['AST']:<7} {player['FG%']}")
    print("-" * 55 + "\n")


# ─────────────────────────────────────────
#  MAIN PROGRAM — MENU LOOP
# ─────────────────────────────────────────

def main():
    players = load_data("nba_stats.csv")

    if not players:
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            lookup_player(players)
        elif choice == "2":
            top_five_leaders(players)
        elif choice == "3":
            compare_players(players)
        elif choice == "4":
            filter_by_team(players)
        elif choice == "5":
            print("\nThanks for using the NBA Stats Analyzer. See you next season!")
            break
        else:
            print("\nInvalid choice — please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()
