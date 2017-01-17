import concurrent.futures
from copy import deepcopy
from .SimulationResult import SimulationResult
from .Simulator import Simulation
from ..core.logger import Logger


class Coordinator:
    def __init__(self, game, logger, count=1000, parallels=5):
        self._game = game
        self._max = count
        self._parallels = parallels
        self._games_per_parallel = self._max // self._parallels

        self._logger = logger

        self._result = SimulationResult.create_empty_result(game._players)

    def _init_winners(self):
        players = self._game.get_players()
        for player in players:
            self._winners[player] = 0

    def run(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._parallels) as executor:
            servants = []

            for i in range(self._parallels):
                servants.append(executor.submit(_run_a_simulator, deepcopy(self._game), self._games_per_parallel))

            for future in concurrent.futures.as_completed(servants):
                self._result.merge(future.result())

        self._result.do_calculations()

        return self._result


def _run_a_simulator(game, count):
    sim = Simulation(game, count, Logger())

    return sim.run()
