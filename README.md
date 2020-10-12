# futbolero 
## prode

"Pronósticos Deportivos" or "PRODE" was a traditional bet game created by the national lotery agency ("Lotería Nacional") of Argentina in 1972. Being just a board printed in paper, the player would bet, with a simple cross made inside a cell, the results of the week's local football tournament. The following development pays tribute to such a popular tradition, discontinued since 2018.

FUTBOLERO is a forecast game based upon python and flask which rewards the users who guess the most number of match scores. The app compairs the user's expected outcomes for each round with the latest results of the current seasons' Premier League (2020-2021) and makes a ranking with the sum of the points obtained by each player.

In order to user the app, the human needs first to make himself/herself an account, including username, email and password. the data input is done through flask-forms and stored in a sqlalchemy database. Login/Register form fields are checked to avoid errors, such as repeated usernames, emails or incorrectly written passwords (which are hasshed before storage).

Session managment is based on flask-session library. After logging in, the user will see the welcome screen with all the info about the current round and the Premier League' standing updated. The user can make a bet, check the points gained after the last round or take a look at his/her profile, ranking and bets/points history. He/She can also modify his/her profile and change his/her favourite footbal squad. If ranked first at the end of the season, the user will receive a congratulations email from the apps'admin.

This project would not be possible without the amazing coding insight delivered by the CS50 course and all the info provided by the best sport API, football-data.org.