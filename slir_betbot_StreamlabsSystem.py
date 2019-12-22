from slir_betbot import SLIRBetbot

ScriptName = "slir_betbot"
Command = "!bet"
Website = "https://en.wikipedia.org"
Description = "Bet on how well a racer will do"
Creator = "tsalgie"
Version = "0.1.1"

currency_name = "ploods"
bet_state = None
iracing_user = 'Complx'

"""
get current top 5
get current race state to start (grid button appears)
get whether green flag out
get total race time
get current race time (to find halfway mark)
determine race finish

get faq
get current currency amount

show bets table with payouts, include multipliers

rules

"""


def Init():
    global bet_state
    global Command
    global currency_name
    global iracing_user

    bet_state = SLIRBetbot(Parent, Command, iracing_user, currency_name)
    return


def Execute(data):
    bet_state.execute(data)
    return


def Tick():
    return
