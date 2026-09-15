# NBA Stats Analyzer

A command-line Python application for exploring NBA player stats from a season dataset.

## Features
- **Player lookup** — search for any player and view their per-game stats (points, rebounds, assists, field goal %)
- **Top 5 leaderboard** — rank the top 5 players in a chosen stat category (points, rebounds, assists, steals, or blocks)
- **Head-to-head comparison** — compare two players side by side across key stats
- **Team roster filter** — view all players on a given team

## How it works
Player data is loaded from a CSV file using Python's built-in `csv` module. The tool handles real-world data quirks like accented player names (via Unicode normalization, so "Doncic" matches "Dončić") and blank stat cells that would otherwise break sorting.

## Tech
Python (standard library only — `csv`, `os`, `unicodedata`)

## How to run
1. Make sure `Final.py` and `nba_stats.csv` are in the same folder
2. Run `python Final.py`
3. Follow the on-screen menu
