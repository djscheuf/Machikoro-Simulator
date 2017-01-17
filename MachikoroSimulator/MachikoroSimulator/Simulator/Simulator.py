"""
Purpose:
    Should be handed a game, and a number of times to run. Then manage
        running of game and collecting of game results.
"""


class SimulationResult:
    def __init__(self, count, winners, turns):
        self.count = count
        self._winner_counts = winners
        self._total_turns = turns

        self.avg_turns = (self._total_turns/self.count)
        self.win_percentages = {}
        self._calculate_win_percentage()

    def _calculate_win_percentage(self):
        for key in self._winner_counts.keys():
            self.win_percentages[key] = 100.00*(self._winner_counts[key]/self.count)

    def _get_overall_winner(self):
        keys = list(self.win_percentages.keys())

        winner = keys[0]
        keys.remove(winner)

        for player in keys:
            if self.win_percentages[winner] < self.win_percentages[player]:
                winner = player

        return winner

    def __repr__(self):
        first = "Simulation Results:\n\tTotal Games: {0}\n\tAvg. Turns per game: {1}".format(self.count,self.avg_turns)
        second = "\n\tPercentages: "
        for key in self.win_percentages.keys():
            second += "\n\t\t {0}: {1}%".format(key, self.win_percentages[key])

        winner = self._get_overall_winner()

        third = "\n\t Overall winner: {0} with a percentage of {1}".format(winner, self.win_percentages[winner])

        return first+second+third


class Simulation:
    def __init__(self, game, count, logger):
        self._game = game
        self._max = count
        self._count = 0

        self._winners = {}
        self._init_winners()

        self._turns = 0
        self._logger = logger

    def _init_winners(self):
        players = self._game.get_players()
        for player in players:
            self._winners[player] = 0.00

    def run(self):
        while self._count < self._max:
            self._logger.info("Running game {0}".format(self._count))
            self._game.reset()
            self._game.run()

            winner = self._game.winner
            self._increment_win_count(winner)

            self._turns += self._game.total_turns

            self._count += 1

        return SimulationResult(self._count, self._winners, self._turns)

    def _increment_win_count(self, winner):
        name = winner.name
        self._logger.debug("\tWinner: {0}".format(winner.name))
        self._winners[name] += 1



