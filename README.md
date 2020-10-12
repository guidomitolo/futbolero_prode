# futbolero 
## prode

"pronósticos deportivos" or "PRODE" was a traditional bet game created by the national lotery agency ("Lotería Nacional") of Argentina in 1972. Being just a board printed in paper, the player would bet with a simple cross inside a cell the matches'results of the local football tournament. the following basic app pays tribute to such a popular tradition, discontinued since 2018.

FUTBOLERO is a forecast game based upon python and flask which rewards the users who guess the most number of matches scores. the app compairs the user's expected outcomes for each round with the latest results of the current seasons' Premier League (2020-2021) and makes a ranking with the sum of the points obtained by each user.

In order to user the app, the human needs first to make himself/herself and account, with and username, a email and a password. the data input is done through flask forms and stored in a database based on sqlalchemy. each field is checked to avoid errors, such as repeated usernames, emails or incorrectly written passwords (which are hasshed before storage).

After logging in, he/she will see the welcome screen with the info about the current round and the premier league' standing updated. the user can make a bet, check the points gained after the last round or take a look at his/her profile, ranking and bets/points history. he/she can also modify the users'profile and change favourite footbal squad. If ranked first at the end of the season, the user will receive a congratulations email from the apps'admin.

this project would not be possible without the amazing coding insight delivered by the CS50 course and all the info provided by the best sport API, football-data.org.