from flask import Flask, render_template, request, jsonify, redirect, url_for
from ..tools.run_sports import run_all_bets
from ..tools.get_sports import get_sports
from ..tools.bet_history import enter_bet
from ..tools.bet_history import get_pending_bets
from ..tools.bet_history import get_all_bets
from ..tools.bet_history import get_settled_bets
from ..tools.bet_history import get_bet
from ..tools.bet_history import update_outcome
from ..tools.bet_history import get_total_bankroll
from ..tools.bet_history import get_bookies_table
from ..tools.bet_history import update_bet_amount
from ..tools.bet_history import update_bet_odds
from ..tools.bet_history import update_date

import os
import sqlite3


def get_path():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database'))
    db_path = os.path.join(root_dir, 'bet_history.db')
    return db_path


def get_db():
    db_path = get_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_all', methods = ['GET', 'POST'])
def run_all():
    if request.method == 'POST':
        sports = get_sports(active=True, has_outrights=False)
        ev_bets = run_all_bets(sports)
        total_bankroll = get_total_bankroll()

        data_ids = get_pending_bets()
        current_ids = []
        for id in data_ids:
            current_ids.append(id["bet_id"])

        ev_bets = [bet for bet in ev_bets if bet[1] not in current_ids]

        for bet in ev_bets:
            kelly_percent = bet[6]
            kelly_wager = kelly_percent * total_bankroll
            bet.append(round(kelly_wager, 2))

        return render_template('select_bets.html', bets=ev_bets)
    return render_template('run_all.html')

@app.route('/select_bets')
def select_bets():
    return render_template('select_bets.html')

@app.route('/take_bet', methods = ['POST'])
def take_bet():
    id = request.form['bet_id']
    print(f'id: {id}')
    sport = request.form['sport']
    team = request.form['team']
    bookie_choice = request.form['bookie']
    bet_type = 'Moneyline'
    odds = int(request.form['odds'])
    #bet_amount = request.form['amount']
    bet_amount = float(request.form['amount'])  # If bet_amount is also from the form
    bet_ev = round(float(request.form['ev']), 2)
    #bet_ev = round(request.form['ev'] * bet_amount, 2)
    date = request.form['date']
    enter_bet(id, sport, team, bet_type, bookie_choice, odds, bet_amount, bet_ev, date)

    return(redirect(url_for('select_bets')))

@app.route('/current_bets', methods = ['GET'])
def current_bets():
    current_bets = sorted(get_pending_bets(), key=lambda bet: bet["date"])
    return render_template('current_bets.html', bets=current_bets)

@app.route('/all_bets', methods = ['GET'])
def all_bets():
    all_bets = get_all_bets()
    return render_template('all_bets.html', bets=all_bets)

@app.route('/settled_bets', methods = ['GET'])
def settled_bets():
    settled_bets = get_settled_bets()
    return render_template('settled_bets.html', bets=settled_bets)

@app.route('/edit_bet', methods=['POST'])
def edit_bet():
    id = request.form['bet_id']
    bet_id = str(id)
    new_date = request.form.get('date', None)
    new_outcome = request.form.get('outcome', None) 

    odds_str = request.form.get('odds', '').strip()
    new_odds = int(odds_str) if odds_str else 0

    amount_str = request.form.get('amount', '').strip()
    new_amount = float(amount_str) if amount_str else 0 

    if new_amount != 0:
        update_bet_amount(bet_id, new_amount)

    if new_odds != 0:
        update_bet_odds(bet_id, new_odds)

    if new_date is not None:
        update_date(bet_id, new_date)
    
    if new_outcome is not None:
        update_outcome(bet_id, new_outcome)  

    return redirect(url_for('current_bets')) 

@app.route('/bookie_stats', methods=['GET'])
def bookie_stats():
    bookie_data = get_bookies_table()
    bookies = []
    bankroll = []
    wagered = []
    wagerable = []
    nets = []
    for x in bookie_data:
        bookies.append(x['bookmaker'])
        bankroll.append(x['total_bankroll'])
        wagered.append(x['currently_wagered'])
        wagerable.append(x['wagerable'])
        nets.append(x['current_net'])

    combined = zip(bookies, bankroll, wagered, wagerable, nets)

    return render_template('bookie_stats.html', combined=combined)

if __name__ == '__main__':
    app.run(debug=True)