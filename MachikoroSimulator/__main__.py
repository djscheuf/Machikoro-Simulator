"""
Purpose: Main interaction point for User

Responsibilities:
+ Collect User input
+ Route to Simulator
+ Present Results
"""

from MachikoroSimulator.Bot import *
from MachikoroSimulator.CardEnum import CardEnum
from MachikoroSimulator import Strategy
from MachikoroSimulator.Engine.DeclareAnEngine import DeclareAnEngine
from MachikoroSimulator.DeckManager import DeckManager
from MachikoroSimulator.Game.StartAGame import StartAGame
from MachikoroSimulator.Simulator.BatchSimulator import BatchSimulator
from MachikoroSimulator.Simulator.Simulator import Simulation
from MachikoroSimulator.Simulator.Coordinator import Coordinator
from MachikoroSimulator.core.logger import *
import time


def routine():
    # Simulator logging events are simply swallowed.
    sim_logger = Logger()

    # Game logging events are simply swallowed.
    logger = Logger()

    p1 = Bot("Cheese Bot")
    p1.with_plan(Strategy.StrategyFactory.cheese_factory_strategy())

    p3 = Bot("Dev Bot")
    p3.with_plan(Strategy.StrategyFactory.developer_strategy())

    p2 = Bot("Furniture Bot")
    p2.with_plan(Strategy.StrategyFactory.furniture_factory_strategy())

    engine = DeclareAnEngine.with_initial_state({CardEnum.WheatField: 1, CardEnum.Bakery: 1}, 3)

    deck = DeckManager()

    game = StartAGame.with_(p1, p2).and_(p3).using(engine, deck, logger)

    summary = "Set up a game between {0}, {1}, and {2} with the standard deck, and starting state."
    print(summary.format(p1.name,
                         p2.name,
                         p3.name))

    # To run a single game:
    # game.run()
    # print("Winner: {0} on turn {1}".format(game.winner.name, game.total_turns))

    # To run a multi-game simulation:
    print("Creating a 1000 game simulation...")

    sim = Coordinator(game, sim_logger, 1000, 7)
    # Coordinator runs simulation in multiple forked processes. (Best performance)

    # sim = BatchSimulator(game, sim_logger, 1000, 7)
    #  Batch simulator attempts to run a batch of games at the same time.

    # sim = Simulation(game, 1000, sim_logger)
    # The simulator runs the given game the given number of times in series.

    import time
    t0 = time.time()
    result = sim.run()
    t1 = time.time()
    print("Simulation took {0} seconds".format(t1-t0))

    print(result)

if __name__ == "__main__":
    routine()
