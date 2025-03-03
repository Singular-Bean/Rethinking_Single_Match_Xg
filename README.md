# Match Outcomes From XG:

Program which takes the shots from a match and shows the match outcome probabilities.

Based on the idea that if you're looking at a stats sheet for a game, expected goals isn't a very good
way of telling you what happened in a game. Even if two teams finish with an xG of 1.0, the 
distribution of that xG can make a big difference. Consider two scenarios:

 - Team A: 20 shots, each with an xG of 0.05
 - Team B: 2 shots, each with an xG of 0.5

Although both teams have a total xG of 1.0, each shot can be thought of as an independent event with a 
conversion probability equal to its xG.


For Team A, the chance of missing a single shot is 1 – 0.05 = 0.95. The probability of missing all 20 
shots is 0.95²⁰ ≈ 35.8%, meaning they have about a 64.2% chance of scoring at least one goal.

For Team B, the chance of missing a single shot is 1 – 0.5 = 0.5. Missing both shots happens with 
probability 0.5² = 25%, so they have a 75% chance of scoring at least once.

With 2 high-quality shots, the outcomes (0, 1, or 2 goals) are more tightly clustered around the 
expected result. In contrast, 20 low-quality shots introduce greater variability and uncertainty, 
which means the team might not capitalize on their chances even though the total xG is the same. This
is the principle that this program is based on.

The program first asks the user to input the names of the home and away teams, and then presents a list
of those games where the expected goals statistics are available. The user can then select a game to use.
For example:

```
What is the name of the home team? man city
What is the name of the away team? real madrid
1. 2025-02-11 20:00:00
2. 2024-04-17 20:00:00
3. 2023-05-17 20:00:00
4. 2022-04-26 20:00:00
Which number match do you want to see? 1
```

In this instance, I have chosen to look at the first match, so the program will output the following:

```
1 - 3 (13.16%)
1 - 4 (10.44%)
2 - 3 (10.19%)
1 - 2 (9.24%)
2 - 4 (8.08%)
2 - 2 (7.16%)
1 - 5 (5.22%)
2 - 5 (4.04%)
3 - 3 (3.49%)
0 - 3 (2.86%)
1 - 1 (2.80%)
3 - 4 (2.77%)
3 - 2 (2.45%)
0 - 4 (2.27%)
2 - 1 (2.17%)
0 - 2 (2.01%)
1 - 6 (1.77%)
3 - 5 (1.39%)
2 - 6 (1.37%)
0 - 5 (1.13%)
3 - 1 (0.74%)
4 - 3 (0.66%)
0 - 1 (0.61%)
4 - 4 (0.52%)
3 - 6 (0.47%)
4 - 2 (0.46%)
1 - 7 (0.43%)
0 - 6 (0.38%)
2 - 7 (0.33%)
4 - 5 (0.26%)
4 - 1 (0.14%)
3 - 7 (0.11%)
Probability of Manchester City winning = 6.62%
Probability of a draw = 13.97%
Probability of Real Madrid winning = 78.53%
```

As you can see, for this example the most likely scoreline is 1-3, with a 13.16% chance of that 
happening. The most likely result is a Real Madrid win, with a 78.53% chance of that happening. I think
that the final probabilities especially are a much more useful statistic than an xG value which is 
somewhat arbitrary. You might notice that the probabilities don't add up to 100%, this is because I have
chosen not to include the scorelines with a probability of less than 0.1%, so some accuracy may be lost
because of that.

# New XG Table:

This is a program which uses a lot of the same features as the previous program, but instead of just 
displaying the calculated scorelines, it creates a new league table using the most likely outcomes.

First the program asks the user these questions (this includes the answers I gave for the example):

```
What league would you like to view the true table of? Premier league
Which season would you like to view the true table of? 23/24
How many rounds do you want to see? 38
```

The program then outputs the following:

```
Team                   Points GD   GS   GP  
Manchester City        87     43   68   38  
Arsenal                86     49   64   38  
Liverpool              86     45   79   38  
Newcastle United       70     15   64   38  
Chelsea                61     12   60   38  
Tottenham Hotspur      58     8    56   38  
Brighton & Hove Albion 57     4    48   38  
Aston Villa            55     3    52   38  
Everton                51     -1   44   38  
Nottingham Forest      50     0    40   38  
Brentford              48     4    50   38  
Bournemouth            47     -3   45   38  
Crystal Palace         47     -4   41   38  
West Ham United        42     -15  45   38  
Fulham                 42     -15  40   38  
Manchester United      38     -10  46   38  
Wolverhampton          36     -22  37   38  
Luton Town             26     -43  30   38  
Burnley                25     -32  29   38  
Sheffield United       24     -38  28   38
```

This shows some interesting results, for example, Man United are in 16th which I think is quite funny.
You might notice this is quite similar to a regular xG table, but it does have some differences, and I
needed a use for the previous program, so I thought this would be a good idea.

In the future I could add a feature that shows the differences between the actual table and the expected
table. I also had an idea where you could input a team and a position, and it would tell you the 
probability of them finishing in that position, so I might do that at one point.