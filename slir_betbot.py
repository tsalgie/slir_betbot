from iracing_client import IracingClient


class SLIRBetbot(object):
    def __init__(self, streamlabs_parent, command, iracing_user, currency):
        self.bets = {}
        self.parent = streamlabs_parent
        self.command = command
        self.iracing_user = iracing_user
        self.currency = currency
        self.iracing_client = IracingClient()

    def add_bet(self, user, bet_type, amount, multiplier):
        self.bets[user] = (bet_type, amount, multiplier)

    def resolve_winner(self, car_state, car_position):
        # determine if we crashed, finished, top5, win
        if car_position == 1: # 0?
            pass
        if car_state == "crashed":
            pass

    def win_multiplier(self):
        multiplier_floor = 1.15
        standings = self.iracing_client.standings()
        current_position = standings.index(iracing_user)  # 0 indexed

        session_status = self.iracing_client.session_status()
        green_light = session_status['green']  # boolean

        multiplier = 10 + current_position

        # after green light, divide by 4
        if green_light:
            multiplier /= 4.0

        race_type = 'laps'  # or 'timed'
        if race_type == 'laps':
            half_race_laps = session_status['total_race_laps'] / 2
            decrease_mult_amount_each_lap = multiplier - multiplier_floor / half_race_laps
            multiplier -= (session_status['elapsed_laps'] * decrease_mult_amount_each_lap)
        else:
            half_race_time = session_status['total_race_time'] / 2  # in seconds
            decrease_mult_amount_each_second = multiplier - multiplier_floor / half_race_time
            multiplier -= (session_status['elapsed_seconds'] * decrease_mult_amount_each_second)

        return multiplier

    def top5_multiplier(self):
        multiplier_floor = 1.15
        standings = self.iracing_client.standings()
        current_position = standings.index(iracing_user)  # 0 indexed

        session_status = self.iracing_client.session_status()
        green_light = session_status.json['green']  # boolean

        multiplier = 5 + ((current_position - 4) / 2)
        # value actually decreases throughout the race
        # after green light, divide by 3
        # how often does total get decreased? by how much?

        return multiplier

    def finish_multiplier(self):
        multiplier_floor = 1.15
        standings = self.iracing_client.standings()
        current_position = standings.index(iracing_user)  # 0 indexed

        session_status = self.iracing_client.session_status()
        green_light = session_status.json['green']  # boolean

        field_size = 0  # http
        multiplier = 1.5  # between 1.5 and 2 depending on distance from med pos
        # value actually decreases throughout the race
        # after green light, divide by 2
        # how often does total get decreased? by how much?

        return multiplier

    def crash_multiplier(self):
        multiplier_floor = 1.15
        standings = self.iracing_client.standings()
        current_position = standings.index(iracing_user)  # 0 indexed

        session_status = self.iracing_client.session_status()
        green_light = session_status.json['green']  # boolean

        field_size = 0  # http
        multiplier = 2  # between 2 and 4 depending on distance from med pos
        # value actually decreases throughout the race
        # after green light, divide by 2
        # how often does total get decreased? by how much?

        return multiplier

    def win(self, data):
        multiplier = self.win_multiplier()
        bet_value = data.GetParam(2)
        bet_state.add_bet(data.UserName, 'win', bet_value, multiplier)

        message = "Thank you for betting on {}!".format(self.iracing_user)
        self.parent.SendStreamWhisper(data.UserName, message)

    def top5(self, data):
        multiplier = self.top5_multiplier()
        bet_value = data.GetParam(2)
        bet_state.add_bet(data.UserName, 'top5', bet_value, multiplier)

        message = "Thank you for betting on {}!".format(self.iracing_user)
        self.parent.SendStreamWhisper(data.UserName, message)

    def finish(self, data):
        multiplier = self.finish_multiplier()
        bet_value = data.GetParam(2)
        bet_state.add_bet(data.UserName, 'finish', bet_value, multiplier)

        message = "Thank you for betting on {}....".format(self.iracing_user)
        self.parent.SendStreamWhisper(data.UserName, message)

    def crash(self, data):
        multiplier = self.finish_multiplier()
        bet_value = data.GetParam(2)
        bet_state.add_bet(data.UserName, 'crash', bet_value, multiplier)

        message = "Thank you for betting against {}....".format(self.iracing_user)
        self.parent.SendStreamWhisper(data.UserName, message)

    # Whispers the top 5 currency holders
    def stats(self, data):
        result = self.parent.GetTopCurrency(5)
        message = "The top 5 hoarders are: {}".format(", ".join(result))
        #self.parent.SendStreamWhisper(data.UserName, message)
        self.parent.SendStreamMessage(message)

    def execute(self, data):
        commands = {
            "win": self.win,
            "top5": self.top5,
            "finish": self.finish,
            "crash": self.crash,
        }

        if data.GetParam(0) != self.command:
            return

        bet_type = data.GetParam(1)

        if bet_type == 'stats':
            self.stats(data)
            return

        amount = data.GetParam(2)
        points = self.parent.GetPoints(data.User)

        if points < amount:
            message = data.UserName + ", you don't have enough " + currency_name + "!"
            self.parent.SendStreamWhisper(data.UserName, message)
            return

        # We now know the user can make a bet, they have enough points
        # Remove points
        self.parent.RemovePoints(data.User, data.UserName, amount)
        # Make the bet
        if bet_type in commands:
            commands[bet_type](data)