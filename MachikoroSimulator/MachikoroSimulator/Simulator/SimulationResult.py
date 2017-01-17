class SimulationResult:
    def __init__(self, count, winners, turns, do_calculations=True):
        self.count = count
        self.wins = winners
        self.total_turns = turns
        self.avg_turns = 0
        self.win_percentages = {}

        if do_calculations:
            self.do_calculations()

    def do_calculations(self):
        self.avg_turns = (self.total_turns / self.count)
        self._calculate_win_percentage()

    def _calculate_win_percentage(self):
        for key in self.wins.keys():
            self.win_percentages[key] = 100.00*(self.wins[key]/self.count)

    def _get_overall_winner(self):
        keys = list(self.win_percentages.keys())

        winner = keys[0]
        keys.remove(winner)

        for player in keys:
            if self.win_percentages[winner] < self.win_percentages[player]:
                winner = player

        return winner

    def __repr__(self):
        first = "Simulation Results:\n\tTotal Games: {0}\n\tAvg. Turns per game: {1}".format(self.count, self.avg_turns)
        second = "\n\tPercentages: "
        for key in self.win_percentages.keys():
            second += "\n\t\t {0}: {1}%".format(key, self.win_percentages[key])

        winner = self._get_overall_winner()

        third = "\n\t Overall winner: {0} with a percentage of {1}".format(winner, self.win_percentages[winner])

        return first+second+third

    def merge(self, result):
        self.count += result.count

        for player in result.wins.keys():
            self.wins[player] += result.wins[player]

        self.total_turns += result.total_turns

    @staticmethod
    def create_empty_result(players):
        winners = {}
        for player in players:
            winners[player.name] = 0

        return SimulationResult(0, winners, 0, False)

