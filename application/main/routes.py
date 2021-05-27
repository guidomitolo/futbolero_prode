# flask core libs
from re import search
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_required
from flask import request
from sqlalchemy.sql.expression import null

# app modules
from application import current_app as app
from application.main import bp
from application.auth.models import User
from application.main.models import Points, Bets, Seasons
from application import db
from application.main.forms import EditProfileForm, GamblingForm
from application.main import connect, helpers

# external libs
from sqlalchemy import desc
from datetime import datetime


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    session['leagues'] = {
        "La Liga": "PD",
        "Serie A": "SA",
        "Ligue 1": "FL1",
        "Bundesliga": "BL1",
        "Premier League": "PL"
    }
    # get league
    session['league'] = request.form.get('button', 'PL')

    # august end of season
    current_year = datetime.now().date().year
    half = datetime.strptime(f"{current_year}-08-01", '%Y-%m-%d').date()

    # get current season and load in session
    if half > datetime.now().date():
        session['season'] = datetime.now().date().year - 1
    else:
        session['season'] = datetime.now().date().year
    
    # fixture api call
    if not session.get('fixture') or request.method == 'POST':
        session['fixture'] = connect.fixture(session['league'], session['season'])
        session['tabla'], session['logos'] = connect.standings(session['league'], session['season'])
        # add logo for each team in fixture
        for team in session['fixture']:
            for logo in session['logos'] :
                if team['homeTeam'] == logo['team']:
                    team['homelogo'] = logo['teamlogo']
                if team['awayTeam'] == logo['team']:
                    team['awaylogo'] = logo['teamlogo']

        
    fixture = session['fixture']
    tabla = session['tabla']

    # get current round matches and currrent round first date
    current_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture)]

    # current round date
    current_round_date = datetime.strptime(current_round[0]['date'], '%d-%m-%Y').date()

    # load all users points if any
    users = User.query.all()
    for user in users:
        user_bets = Bets.query.filter_by(user_id = user.id).all()
        for bet in user_bets:
            bet_points = Points.query.filter(Points.user_id==user.id, Points.match_id==bet.match_id).first()
            if not bet_points:
                for match in session['fixture']:
                    if bet.match_id == match['matchID']:
                        if match['score'][0] is not None or match['score'][0] is not null:
                            user_points = helpers.score(bet.score_home, match['score'][0], match['score'][1], bet.score_away)
                            hits = 0
                            if user_points == 6:
                                hits =+ 1
                            load_points = Points(
                                user_id=user.id,
                                match_id=match['matchID'],
                                points = user_points,
                                hits = hits,
                                season = session['season'],
                                league = session['league']
                            )
                            db.session.add(load_points)
                            db.session.commit()


    # check for not past/present/future not played games
    remaining = helpers.pending(fixture)
    
    if not remaining:
        # no matches remaing in the season
        flash('Esta temporada ya ha finalizado')
        end_season = Seasons.query.filter_by(season=session['season'], league=session['league']).first()
        if not end_season:

            winner = db.session.query(
                Points.user_id, 
                db.func.sum(Points.points).label('sum'), 
                db.func.sum(Points.hits).label('sum_2')
                ) \
                .group_by(Points.user_id) \
                .order_by(desc('sum')) \
                .order_by(desc('sum_2')) \
                .filter(Points.season == session['season'], Points.league == session['league']
            ).first()
            
            user = None
            points = None
            hits = None
            if winner:
                user = User.query.filter_by(id = winner.user_id).first().username
                points = winner[1]
                hits = winner[2]

            load_season = Seasons(
                season=session['season'],
                league=session['league'],
                finished=True,
                winner = user,
                total_points = points,
                matches_hits =  hits,
            )
            db.session.add(load_season)
            db.session.commit()
    else:
        # get only pengind matches BEFORE current round and erase the rest
        for match in remaining:
            if datetime.strptime(match['date'], '%d-%m-%Y').date() >= current_round_date:
                remaining.remove(match)
            else:
                if match['score'][0] != None:
                    remaining.remove(match)
                   
    return render_template("main/index.html", 
        title='Bienvenido', 
        table=tabla, 
        fixture=current_round,
        postponed = remaining
    )


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):

    # get league with post
    if request.method == 'POST':
        session['league'] = request.form.get('button')
        session['tabla'], session['logos'] = connect.standings(session['league'], session['season'])
        session['fixture'] = connect.fixture(session['league'], session['season'])
        
        # add logo for each team in fixture
        for team in session['fixture']:
            for logo in session['logos'] :
                if team['homeTeam'] == logo['team']:
                    team['homelogo'] = logo['teamlogo']
                if team['awayTeam'] == logo['team']:
                    team['awaylogo'] = logo['teamlogo']

    users_points = db.session.query(
        Points.user_id, 
        db.func.sum(Points.points).label('sum'), 
        db.func.sum(Points.hits).label('sum_2')
        ) \
        .group_by(Points.user_id) \
        .order_by(desc('sum')) \
        .filter(Points.season == session['season'], Points.league == session['league']) \
    .all()
    
    # prepare ranking
    ranking = []
    if users_points:
        for row in range(len(users_points)):
            for i, user in enumerate(User.query.all()):
                if user.id == users_points[row][0]:
                    ranking.append({
                        'position': i,
                        'name': user.username,
                        'mail': user.email,
                        'points': users_points[row][1],
                        'hits': users_points[row][2]
                        })

    # make a line chart with the users points of each round
    line_chart = None

    current_user = User.query.filter_by(username=username).first_or_404()

    # check if season has ended in current session. if so, name winner
    if not helpers.pending(session['fixture']):
        if ranking:
            if current_user.username == ranking[0]['name']:
                flash('¡Has ganado la temporada!')

        get_season = Seasons.query.filter_by(season=session['season'], league=session['league']).first()           
        if not get_season:
            winner = db.session.query(
                Points.user_id, 
                db.func.sum(Points.points).label('sum'), 
                db.func.sum(Points.hits).label('sum_2')
                ) \
                .group_by(Points.user_id) \
                .order_by(desc('sum')) \
                .order_by(desc('sum_2')) \
                .filter(Points.season == session['season'], Points.league == session['league']
            ).first()
            
            user = None
            points = None
            hits = None
            if winner:
                user = User.query.filter_by(id = winner.user_id).first().username
                points = winner[1]
                hits = winner[2]

            load_season = Seasons(
                season=session['season'],
                league=session['league'],
                finished=True,
                winner = user,
                total_points = points,
                matches_hits =  hits,
            )
            db.session.add(load_season)
            db.session.commit()

    else:
        # check if first place
        if ranking:
            if username == ranking[0]['name']:
                flash('¡Felicitaciones, vas ganando!')

    # get past winners
    past_winners = Seasons.query.filter(Seasons.league == session['league'], Seasons.finished == True).all()
    
    return render_template('main/user.html',
                    user=current_user, 
                    logo=current_user.fav_squad_logo,
                    ranking=ranking,
                    current_season = session['season'],
                    league = session['league'],
                    winners = past_winners,
                    plot=line_chart)


@bp.route('/history/<username>')
@login_required
def history(username):
    
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(id=current_user.id).first()

    user_points = user.rank.filter(
        Points.season == session['season'], Points.league == session['league']
    ) \
    .order_by(Points.match_id) \
    .paginate(page, app.config['ROWS_PER_PAGE'], False)

    user_bets = user.bet.filter(
        Bets.season == session['season'], Bets.league == session['league']
    ) \
    .order_by(Bets.match_id) \
    .paginate(page, app.config['ROWS_PER_PAGE'], False)

    historial = helpers.get_history(session['fixture'], user_points.items, user_bets.items, session['season'])

    next_url = url_for('history', username=current_user.username, page = user_bets.next_num) if user_bets.has_next else None
    prev_url = url_for('history', username=current_user.username, page = user_bets.prev_num) if user_bets.has_prev else None
    

    return render_template('main/history.html', user=username, history=historial, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    if not session.get('league_team'):
        session['league_team'] = 'PL'
    teams = connect.team(session['league_team'])
    form = EditProfileForm(current_user.username)
    form.username.data = current_user.username

    if request.form.get('button_league'):
        session['league_team'] = request.form.get('button_league')
        teams = connect.team(session['league_team'])

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.fav_squad = request.form.get('teams')
        current_user.fav_squad_logo = connect.logo(session['league_team'],request.form.get('teams'))
        db.session.commit()
        flash('Los cambios han sido guardados')
        return redirect(url_for('main.edit_profile'))

    return render_template(
        'main/edit_profile.html',
        title='Editar Perfil',
        form=form,
        leagues = session['leagues'],
        teams = teams)


@bp.route('/bet', methods=['GET', 'POST'])
@login_required
def bet():

    # make list of matches in bets
    bet_matches = Bets.query.filter_by(user_id=current_user.id).all()
    bet_list = [int(str(bet)) for bet in bet_matches]
       
    # get matches of next round, if None there are no more matches left
    next_round_matches = [matches for matches in session['fixture'] if matches['round'] == helpers.up_rounds(session['fixture']) + 1]

    # make a list to pass as value attribute of each field
    attributes = []
    for match in next_round_matches:
        if match['matchID'] in bet_list:
            for bet in bet_matches:
                if int(str(bet.match_id)) == match['matchID']:
                    attributes.append({'home':int(str(bet.score_home)),'away':int(str(bet.score_away))})

    form = GamblingForm()

    if form.validate_on_submit():
        # first check if the bet is already done to overwrite the scores
        for value, match in zip(form.bet.data, next_round_matches):
            # check if the user has not place any bet and add a new user and a new bet
            if len(bet_matches) == 0:
                new_user_bets = Bets(
                    user_id=current_user.id,
                    season = session['season'],
                    league = session['league'],
                    match_id=match['matchID'],
                    timestamp = datetime.utcnow(),
                    score_home = value['home'],
                    score_away = value['away']
                )
                db.session.add(new_user_bets)
                db.session.commit()
            # check if the already existing user has already place a bet in the database
            else:
                if match['matchID'] in bet_list:
                    for bet in bet_matches:
                        if int(str(bet.match_id)) == match['matchID']:
                            bet.timestamp = datetime.utcnow()
                            bet.score_home = value['home']
                            bet.score_away = value['away']
                            bet.season = session['season']
                            bet.league = session['league']
                            db.session.commit()
                else:
                    new_bet = Bets(
                        user_id=current_user.id,
                        season = session['season'],
                        league = session['league'],
                        match_id=match['matchID'],
                        timestamp = datetime.utcnow(),
                        score_home = value['home'],
                        score_away = value['away']
                    )
                    db.session.add(new_bet)
                    db.session.commit()
        flash('Has enviado una apuesta')
        return redirect(url_for('bet'))

    return render_template("main/bet.html", 
        title ='Apostar', 
        table = next_round_matches, 
        form = form, 
        value = attributes
    )

@bp.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    # get matches of current and next round
    current_round_matches = [matches for matches in session['fixture'] if matches['round'] == helpers.up_rounds(session['fixture'])]    
    # get last round last date
    current_round_date = datetime.strptime(current_round_matches[-1]['date'], '%d-%m-%Y').date()

    # check bets are placed before current round
    user_bets = Bets.query.filter(Bets.user_id == current_user.id, Bets.timestamp <= current_round_date).all()
    
    # test past bets
    # user_bets = Bets.query.filter(Bets.user_id == current_user.id, Bets.timestamp >= datetime.now().date()).all()

    # if user has no bets for last round, nothing will be loaded
    # once the round is over, the next round will be loaded
    total = 0
    if not user_bets:
        total = 'no_bets'
    elif datetime.utcnow().date() > current_round_date:
        for match in current_round_matches:
            for bet in user_bets:
                if match['matchID'] == int(str(bet.match_id)):
                    if bet.score_home:
                        match['bet_local'] = bet.score_home
                        match['bet_away'] = bet.score_away
                        # query user and match id points
                        get_points = Points.query.filter(Points.user_id == current_user.id, Points.match_id == match['matchID']).first()
                        # if query doesnt exist, load points
                        if get_points:
                            match['points'] = get_points.points
                        else:
                            if match['score'][0] is not None or match['score'][0] is not null:
                                match_points = helpers.score(bet.score_home, match['score'][0], match['score'][1], bet.score_away)
                                hits = 0
                                if match_points == 6:
                                    hits = 1
                                new_points = Points(user_id=current_user.id,
                                    match_id=match['matchID'],
                                    points = match_points,
                                    hits = hits,
                                    season = session['season'],
                                    league = session['league']
                                )
                                db.session.add(new_points)
                                db.session.commit()
                                match['points'] = match_points
                                total = total + match['points']
                    else:
                        # para el futuro (cuando sea posible no apostar para un partido en particular)
                        match['bet_local'] = 'No Bet'
                        match['bet_away'] = 'No Bet'
    else:
        total = 'closed'
        
    return render_template("main/results.html",
        title='Puntos',
        table=current_round_matches,
        total=total
    )