"""
Purpose:
    Should be handed a game, and a number of times to run. Then manage
        running of game and collecting of game results.
"""
from .SimulationResult import SimulationResult


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



