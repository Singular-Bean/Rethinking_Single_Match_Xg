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
        print(f"{scoreline[0]} - {scoreline[1]} ({probability*100:.2f}%)")

    # Calculate the probabilities for each scenario
    home_win_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] > scoreline[1])
    draw_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] == scoreline[1])
    away_win_prob = sum(prob for (scoreline, prob) in scorelines if scoreline[0] < scoreline[1])

    # Display the probabilities for each scenario
    print(f"Probability of " + hometm + f" winning = {home_win_prob*100:.2f}%")
    print(f"Probability of a draw = {draw_prob*100:.2f}%")
    print(f"Probability of " + awaytm + f" winning = {away_win_prob*100:.2f}%")


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


hometeam = input("What is the name of the home team? ")

awayteam = input("What is the name of the away team? ")

matchesurl = "http://www.sofascore.com/api/v1/search/events?q=" + hometeam + "%20" + awayteam + "&page=0"
clashlist = fetch_and_parse_json(matchesurl)

matches = []
epochs = []
for i in range(len(clashlist["results"])):
    clash = clashlist["results"][i]
    entity = clash["entity"]
    if entity["homeTeam"]["id"] == teamid(hometeam) and entity["awayTeam"]["id"] == teamid(
            awayteam) and "hasXg" in entity and entity["hasXg"] == True:
        dateepoch = entity["startTimestamp"]
        date = datetime.fromtimestamp(dateepoch).strftime('%Y-%m-%d %H:%M:%S')
        matches.append(date)
        epochs.append(dateepoch)

dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in matches]

# Sort the dates in reverse chronological order
sorted_dates = sorted(dates, reverse=True)

sorted_epochs = sorted(epochs, reverse=True)

# If needed, convert back to strings or use as is
sorted_date_strs = [date.strftime('%Y-%m-%d %H:%M:%S') for date in sorted_dates]

for a in range(len(sorted_date_strs)):
    print(str(a + 1) + ".", sorted_date_strs[a])

choiceepoch = int(input("Which number match do you want to see? "))

for i in range(len(clashlist["results"])):
    clash = clashlist["results"][i]
    entity = clash["entity"]
    if entity["startTimestamp"] == sorted_epochs[choiceepoch - 1]:
        matchid = entity["id"]

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

homefull = fetch_and_parse_json("http://www.sofascore.com/api/v1/event/" + str(matchid))["event"]["homeTeam"]["name"]

awayfull = fetch_and_parse_json("http://www.sofascore.com/api/v1/event/" + str(matchid))["event"]["awayTeam"]["name"]

calculate_scorelines(homegoalprobs, awaygoalprobs, homefull, awayfull)