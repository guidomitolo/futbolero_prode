# from app import db
# from app.models import User, Points

# users = User.query.all()
# user_list = [{'nombre':user.username,'puntos': user.rank.first().points} for user in users]
# ranking = sorted(user_rank, key=lambda diccionario: diccionario['puntos'], reverse=True) 
# print(newlist)
# api= [{'season': '2020-2021', 'round': '1', 'date': '2020-09-13', 'homeTeam': 'Manchester City FC', 'awayTeam': 'Aston Villa FC', 'score': [None, None]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-13', 'homeTeam': 'Burnley FC', 'awayTeam': 'Manchester United FC', 'score': [None, None]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-12', 'homeTeam': 'Fulham FC', 'awayTeam': 'Arsenal FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-12', 'homeTeam': 'Crystal Palace FC', 'awayTeam': 'Southampton FC', 'score': [1, 0]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-12', 'homeTeam': 'Liverpool FC', 'awayTeam': 'Leeds United FC', 'score': [4, 3]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-12', 'homeTeam': 'West Ham United FC', 'awayTeam': 'Newcastle United FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-13', 'homeTeam': 'West Bromwich Albion FC', 'awayTeam': 'Leicester City FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-13', 'homeTeam': 'Tottenham Hotspur FC', 'awayTeam': 'Everton FC', 'score': [0, 1]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-14', 'homeTeam': 'Sheffield United FC', 'awayTeam': 'Wolverhampton Wanderers FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': '1', 'date': '2020-09-14', 'homeTeam': 'Brighton & Hove Albion FC', 'awayTeam': 'Chelsea FC', 'score': [1, 3]}]
# played = [x['score'] if x['score'][0] != None else 'Pospuesto' for x in api]
# print(played)


api = [{'team': 'Liverpool FC', 'teamlogo': 'https://crests.football-data.org/64.svg'}, {'team': 'Manchester City FC', 'teamlogo': 'https://crests.football-data.org/65.svg'}, {'team': 'Manchester United FC', 'teamlogo': 'https://crests.football-data.org/66.svg'}, {'team': 'Chelsea FC', 'teamlogo': 'https://crests.football-data.org/61.svg'}, {'team': 'Leicester City FC', 'teamlogo': 'https://crests.football-data.org/338.svg'}, {'team': 'Tottenham Hotspur FC', 'teamlogo': 'https://crests.football-data.org/73.svg'}, {'team': 'Wolverhampton Wanderers FC', 'teamlogo': 'https://crests.football-data.org/76.svg'}, {'team': 'Arsenal FC', 'teamlogo': 'https://crests.football-data.org/57.svg'}, {'team': 'Sheffield United FC', 'teamlogo': 'https://crests.football-data.org/356.svg'}, {'team': 'Burnley FC', 'teamlogo': 'https://crests.football-data.org/328.svg'}, {'team': 'Southampton FC', 'teamlogo': 'https://crests.football-data.org/340.svg'}, {'team': 'Everton FC', 'teamlogo': 'https://crests.football-data.org/62.svg'}, {'team': 'Newcastle United FC', 'teamlogo': 'https://crests.football-data.org/67.svg'}, {'team': 'Crystal Palace FC', 'teamlogo': 'https://crests.football-data.org/354.svg'}, {'team': 'Brighton & Hove Albion FC', 'teamlogo': 'https://crests.football-data.org/397.svg'}, {'team': 'West Ham United FC', 'teamlogo': 'https://crests.football-data.org/563.svg'}, {'team': 'Aston Villa FC', 'teamlogo': 'https://crests.football-data.org/58.svg'}, {'team': 'AFC Bournemouth', 'teamlogo': 'https://crests.football-data.org/1044.svg'}, {'team': 'Watford FC', 'teamlogo': 'https://crests.football-data.org/346.svg'}, {'team': 'Norwich City FC', 'teamlogo': 'https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg'}]
fixture = [{'season': '2019-2020', 'round': '1', 'date': '2019-08-09', 'homeTeam': 'Liverpool FC', 'awayTeam': 'Norwich City FC', 'score': [4, 1]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'West Ham United FC', 'awayTeam': 'Manchester City FC', 'score': [0, 5]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'Burnley FC', 'awayTeam': 'Southampton FC', 'score': [3, 0]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'Crystal Palace FC', 'awayTeam': 'Everton FC', 'score': [0, 0]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'Watford FC', 'awayTeam': 'Brighton & Hove Albion FC', 'score': [0, 3]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'AFC Bournemouth', 'awayTeam': 'Sheffield United FC', 'score': [1, 1]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-10', 'homeTeam': 'Tottenham Hotspur FC', 'awayTeam': 'Aston Villa FC', 'score': [3, 1]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-11', 'homeTeam': 'Leicester City FC', 'awayTeam': 'Wolverhampton Wanderers FC', 'score': [0, 0]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-11', 'homeTeam': 'Newcastle United FC', 'awayTeam': 'Arsenal FC', 'score': [0, 1]}, {'season': '2019-2020', 'round': '1', 'date': '2019-08-11', 'homeTeam': 'Manchester United FC', 'awayTeam': 'Chelsea FC', 'score': [4, 0]}]

tabla = []

for team in fixture:
    for logo in api:
        if team['homeTeam'] == logo['team']:
            team['homelogo'] = logo['teamlogo']
        if team['awayTeam'] == logo['team']:
            team['awaylogo'] = logo['teamlogo']


fixture_2 = [team['homelogo'] = logo['teamlogo'] if team['homeTeam'] == logo['team'] team['awaylogo'] = logo['teamlogo'] if team['awayTeam'] == logo['team'] for team in fixture for logo in api]


# primero creo una lista local visitante logos
# despues meto en fixture la nueva lista


