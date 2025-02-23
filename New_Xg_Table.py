from datetime import datetime
import numpy as np
import requests
from itertools import combinations


def event_probabilities(prob_list):
    n = len(prob_list)
    result = []

    # Probability of none of the events happening
    none_happening = 1
    for prob in prob_list:
        none_happening *= (1 - prob)
    result.append(none_happening)

    # Probabilities for k events happening (k = 1 to n)
    for k in range(1, n + 1):
        k_comb_prob = 0
        for comb in combinations(range(n), k):
            prod = 1
            for i in range(n):
                if i in comb:
                    prod *= prob_list[i]
                else:
                    prod *= (1 - prob_list[i])
            k_comb_prob += prod
        result.append(k_comb_prob)

    # Ensure the result list length is either 9 or the length of the input list + 1, whichever is smaller
    return result[:min(10, n + 1)]


def event_probabilities2(probabilities):
    n = len(probabilities)
    dp = np.zeros((n + 1, n + 1))  # DP table to store probabilities

    dp[0][0] = 1.0  # Base case: probability of 0 events happening is 1

    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] * (1 - probabilities[i - 1])  # No event happening
        for j in range(1, i + 1):
            dp[i][j] = dp[i - 1][j] * (1 - probabilities[i - 1]) + dp[i - 1][j - 1] * probabilities[i - 1]

    results = dp[n][1:].tolist()  # We skip dp[n][0] as it represents the probability of no events happening
    return results


def calculate_scorelines(team1_probs, team2_probs, hometm, awaytm):
    max_goals = 10
    scorelines = []

    # Calculate probabilities for each possible scoreline
    for team1_goals, team1_prob in enumerate(team1_probs):
        for team2_goals, team2_prob in enumerate(team2_probs):
            scoreline = (team1_goals, team2_goals)
            probability = round(team1_prob * team2_prob, 4)
            if probability > 0.0010:
                scorelines.append((scoreline, probability))

    # Sort by probability (descending) and then by total goals (ascending)
    scorelines.sort(key=lambda x: (-x[1], x[0][0] + x[0][1], x[0]))

    # Filter scorelines with total goals exceeding max_goals
    scorelines = [item for item in scorelines if item[0][0] + item[0][1] <= max_goals]

    # Display the scorelines and their probabilities
    for (scoreline, probability) in scorelines:
        print(f"{scoreline[0]} - {scoreline[1]} ({probability:.4f})")

    # Calculate the probabilities for each scenario
    home_win_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] > scoreline[1])
    draw_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] == scoreline[1])
    away_win_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] < scoreline[1])

    # Display the probabilities for each scenario
    print(f"Probability of " + hometm + f" winning = {home_win_prob:.2f}")
    print(f"Probability of a draw = {draw_prob:.2f}")
    print(f"Probability of " + awaytm + f" winning = {away_win_prob:.2f}")


def most_likely(team1_probs, team2_probs):
    scorelines = []

    # Calculate probabilities for each possible scoreline
    for team1_goals, team1_prob in enumerate(team1_probs):
        for team2_goals, team2_prob in enumerate(team2_probs):
            scoreline = (team1_goals, team2_goals)
            probability = round(team1_prob * team2_prob, 4)
            if probability > 0.0010:
                scorelines.append((scoreline, probability))

    # Sort by probability (descending) and then by total goals (ascending)
    scorelines.sort(key=lambda x: (-x[1], x[0][0] + x[0][1], x[0]))
    return scorelines[0][0]


##DADS

def fetch_and_parse_json(url):
    response = requests.get(url)
    response.raise_for_status(
    )  # Ensure we raise an error for bad status codes
    data = response.json()
    return data


def list_xg_from_shotmap(json_data, isHome):
    return [item['xg'] for item in json_data['shotmap'] if
            'xg' in item and item['isHome'] == isHome and item["situation"] != "shootout"]

def leagueid():
    league = input("What league would you like to view the true table of? ")
    leagueid = fetch_and_parse_json("http://www.sofascore.com/api/v1/search/unique-tournaments?q=" + league + "&page=0")['results'][0]['entity']['id']
    return leagueid
def seasonid(leagueid):
    year = input("Which season would you like to view the true table of? ")
    seasons = fetch_and_parse_json("http://www.sofascore.com/api/v1/unique-tournament/" + str(leagueid) + "/seasons")['seasons']
    for i in range (0,len(seasons)):
        if seasons[i]['year'] == year:
            return seasons[i]['id']

def teamid(name):
    url = "http://www.sofascore.com/api/v1/search/teams?q=" + name + "&page=0"
    data = fetch_and_parse_json(url)['results'][0]['entity']['id']
    return data

def match_list(seasonid, leagueid, round):
    full_list = []
    for p in range(0, int(round)):
        print("Loading round " + str(p+1) + "...")
        roundmatches = fetch_and_parse_json("http://www.sofascore.com/api/v1/unique-tournament/" + str(leagueid) + "/season/" + str(seasonid) + "/events/round/" + str(p+1))["events"]
        for i in range(0, len(roundmatches)):
            match = roundmatches[i]
            matchid = match["id"]
            if fetch_and_parse_json(f"https://www.sofascore.com/api/v1/event/{matchid}")['event']['status']['code'] == 100:
                hometeam = match["homeTeam"]["name"]
                awayteam = match["awayTeam"]["name"]


                homexg = list_xg_from_shotmap(
                    fetch_and_parse_json("http://www.sofascore.com/api/v1/event/" + str(matchid) + "/shotmap"), True)

                x = 1
                for j in homexg:
                    x = x * (1 - j)

                homegoalprobs = event_probabilities2(homexg)

                homegoalprobs.insert(0, x)

                awayxg = list_xg_from_shotmap(
                    fetch_and_parse_json("http://www.sofascore.com/api/v1/event/" + str(matchid) + "/shotmap"), False)

                y = 1
                for j in awayxg:
                    y = y * (1 - j)

                awaygoalprobs = event_probabilities2(awayxg)

                awaygoalprobs.insert(0, y)

                emptytuple = ()

                homename = str(hometeam)

                homescore = most_likely(homegoalprobs, awaygoalprobs)[0]

                awayscore = most_likely(homegoalprobs, awaygoalprobs)[1]

                awayname = str(awayteam)

                full_list.append((homename, [homescore, awayscore], awayname, "Round " + str(p+1)))
    return full_list


##print(str(homefull) + " [" + str(most_likely(homegoalprobs, awaygoalprobs)[0]) + ", " + str(most_likely(homegoalprobs, awaygoalprobs)[1]) + "] " + str(awayfull))

def create_league_table(matches):
    # Initialize a dictionary to store team statistics
    league_table = {}

    for match in matches:
        # Parse the match data
        home_team, home_score, away_score, away_team, round_info = match[0], match[1][0], match[1][1], match[2], match[3]

        # Initialize teams in the league table if not already present
        if home_team not in league_table:
            league_table[home_team] = {'points': 0, 'goal_difference': 0, 'goals_scored': 0, 'games_played': 0}
        if away_team not in league_table:
            league_table[away_team] = {'points': 0, 'goal_difference': 0, 'goals_scored': 0, 'games_played': 0}

        # Update games played
        league_table[home_team]['games_played'] += 1
        league_table[away_team]['games_played'] += 1

        # Update goals scored
        league_table[home_team]['goals_scored'] += home_score
        league_table[away_team]['goals_scored'] += away_score

        # Update goal difference
        league_table[home_team]['goal_difference'] += (home_score - away_score)
        league_table[away_team]['goal_difference'] += (away_score - home_score)

        # Update points
        if home_score > away_score:
            league_table[home_team]['points'] += 3
        elif home_score < away_score:
            league_table[away_team]['points'] += 3
        else:
            league_table[home_team]['points'] += 1
            league_table[away_team]['points'] += 1

    # Sort the league table based on points, goal difference, and goals scored
    sorted_teams = sorted(league_table.items(), key=lambda x: (x[1]['points'], x[1]['goal_difference'], x[1]['goals_scored']), reverse=True)

    # Create the table
    print(f"{'Team':<22} {'Points':<6} {'GD':<4} {'GS':<4} {'GP':<4}")
    for team, stats in sorted_teams:
        print(f"{team:<22} {stats['points']:<6} {stats['goal_difference']:<4} {stats['goals_scored']:<4} {stats['games_played']:<4}")

# Example usage
matches = [
    ("Burnley", [1, 2], "Arsenal", "Round 1"),
    ("Chelsea", [3, 1], "Liverpool", "Round 1"),
    ("Burnley", [0, 0], "Chelsea", "Round 2"),
    ("Arsenal", [2, 1], "Liverpool", "Round 2")
]



lgid = leagueid()
ssid = seasonid(lgid)

roundnum = int(input("How many rounds do you want to see? "))

create_league_table(match_list(ssid, lgid, roundnum))