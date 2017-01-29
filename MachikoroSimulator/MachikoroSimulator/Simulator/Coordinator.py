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

        import math
        self._games_per_parallel = math.ceil(self._max / self._parallels)

        self._logger = logger

        # this is kind of hacky, but allowed the player list to be passed to the empty result.
        self._result = SimulationResult.create_empty_result(game._players)

    def run(self):
        # allows creation of specified number of parallel processes.
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._parallels) as executor:
            servants = []

            # assigns run_a_sim function to each process with their own copy of game.
            for i in range(self._parallels):
                servants.append(executor.submit(_run_a_simulator, deepcopy(self._game), self._games_per_parallel))

            # as the processes complete, merge in their results.
            for future in concurrent.futures.as_completed(servants):
                self._result.merge(future.result())

        # once all processes are complete, perform statistical calculations on collected results.
        self._result.do_calculations()

        return self._result


def _run_a_simulator(game, count):
    sim = Simulation(game, count, Logger())

    return sim.run()
