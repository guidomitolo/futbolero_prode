# futbolero

## Prode

![](https://raw.githubusercontent.com/guidomitolo/futbolero_prode/master/Boleta_Prode.jpg)


_"Pronósticos Deportivos"_ or _"PRODE"_ was a traditional bet game created by the national lotery agency ("Lotería Nacional") of Argentina in 1972. Being just a board printed in paper, the player would bet, with a simple cross made inside a cell, the upcoming results of the week's local football tournament. The following development pays tribute to such a popular tradition, discontinued since 2018.

**FUTBOLERO** is a forecast game based on python and flask which rewards the users who guess the most number of match scores. The app compairs the user's expected outcomes for each round with the latest results of the current seasons' Premier League (2020-2021) and makes a ranking with the sum of the points obtained by each player.

In order to user the app, the human needs first to make himself/herself an account, including username, email and password. the data input is done through flask-forms and stored in a sqlalchemy database. Login/Register form fields are checked to avoid errors, such as repeated usernames, emails or incorrectly written passwords (which are hashed before storage).

Session managment is based on flask-session library on redis. After logging in, the user will see the welcome screen with all the info about the current round and the Premier League' standing updated. The user can make a bet, check the points gained after the last round or take a look at his/her profile, ranking and bets/points history. He/She can also modify his/her profile and change his/her favourite footbal squad. If ranked first at the end of the season, the user will receive a congratulations email from the apps'admin.

## Deploy

1- Set environment variables or create .env

a- postgres config vars

```
PSQL_PASS=SuperPassword
PSQL_USER=YourPSQLuser
PSQL_HOST_DB=DockerNamedDB
```

b- redis config vars

```
REDIS_HOST=redis
```

c. set api key

```
API_KEY=SomeAPIKey
```
Get an api key from https://www.football-data.org/

2- Deploy through docker-compose

```
docker-compose up -d
```
