import concurrent.futures
from copy import deepcopy
from .SimulationResult import SimulationResult


class BatchSimulator:
    def __init__(self, game, logger, count=1000, batch_size=5):
        self._game = game
        self._max = count
        self._batch_size = batch_size
        self._batches = self._max//self._batch_size
        self._count = 0

        self._winners = {}
        self._init_winners()

        self._turns = 0
        self._logger = logger

    def _init_winners(self):
        players = self._game.get_players()
        for player in players:
            self._winners[player] = 0

    def run(self):

        for i in range(self._batches):
            self._run_a_batch()

        return SimulationResult(self._count, self._winners, self._turns)

    def _run_a_batch(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._batch_size) as executor:
            batch = []

            for i in range(self._batch_size):
                batch.append(executor.submit(self._run_a_game, deepcopy(self._game)))

            for future in concurrent.futures.as_completed(batch):
                game_result = future.result()
                self._increment_win_count(game_result.winner)
                self._turns += game_result.turns
                self._count += 1

    @staticmethod
    def _run_a_game(game):
        game.reset()
        game.run()
        return game.get_result()

    def _increment_win_count(self, winner):
        name = winner.name
        self._logger.debug("\tWinner: {0}".format(winner.name))
        self._winners[name] += 1
