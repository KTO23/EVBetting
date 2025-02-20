from ..sports.threeresult import get_three_result_moneyline_bets
from ..sports.tworesult import get_two_result_moneyline_bets
from .get_sports import get_sports
from .odds_calculator import *
from .get_sports import two_result_sport_list
from .get_sports import three_result_sport_list
from .bet_history import enter_bet
from .bet_history import bet_exists
from .bet_history import display_pending_bets
from .bet_history import get_pending_ids
from .bet_history import update_bet
from .bet_history import display_all_bets

ev_cutoff = 10
odds_cutoff = 1000

def run_all(sport_list):
    EVbetslist = []
    printdf = False
    for x in sport_list:
        if x in two_result_sport_list:
            get_two_result_moneyline_bets(EVbetslist, x, printdf)
        elif x in three_result_sport_list:
            get_three_result_moneyline_bets(EVbetslist, x, printdf)
        else:
            print(f'Sport not found: {x}')

    print('\n')
    print("EVbetslist: ")
    for x in EVbetslist:
        print(x)
        
    print('fuck you\n\n')
    for x in EVbetslist:
        id = x[1]
        print("test")
        alr_exists = bet_exists(id)
        if(alr_exists):
            print("Bet already exists")
            continue
        print(x)
        will_take = input("Would you like to take this? (y/n): ")
        if will_take == 'y':
            sport = x[0]
            team = x[2]
            bet_type = 'Moneyline'
            bookie_list = x[3]
            bookie = ""
            for bookies in bookie_list:
                bookie_bool = input(f'{bookies}? (y/n): ')
                if bookie_bool == 'y':
                    bookie = bookies
            odds = int(x[4])
            bet_amount = int(input("Bet amount: "))
            bet_ev = int(x[5])
            date = x[6]

            enter_bet(id, sport, team, bet_type, bookie, odds, bet_amount, bet_ev, date)
    
    display_all_bets()


def run_get_sports():
    active = True
    has_outrights = False

    #sports_list = get_sports(active, has_outrights)
    sports_list =['soccer_epl']
    global ev_cutoff
    global odds_cutoff

    ev_cutoff = 10
    odds_cutoff = 1000
    run_all(sports_list)

def update_bets():
    pending_bet_ids = get_pending_ids()
    display_pending_bets()
    print('\n')
    for x in pending_bet_ids:
        print(x)
        settled = input("Is the bet settled? (y/n): ")
        if settled == 'y':
            result = input("Result (win or loss): ")
            update_bet(x[0], result)
    
#run_get_sports()
