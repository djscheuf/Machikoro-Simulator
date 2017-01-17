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
from MachikoroSimulator.core.logger import *
import time


def routine():
    sim_logger = Logger()

    # should silence the game output... sadly.
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

    print("Set up a game between {0}, {1}, and {2} with the standard deck, and starting state.".format(p1.name,
                                                                                                       p2.name,
                                                                                                       p3.name))

    # game.run()

    # print("Winner: {0} on turn {1}".format(game.winner.name, game.total_turns))

    print("Creating a 1000 game simulation...")

    sim = BatchSimulator(game, sim_logger, 1000, 7)
    # sim = Simulation(game, 1000, sim_logger)

    import time
    t0 = time.time()
    result = sim.run()
    t1 = time.time()
    print("Simulation took {0} seconds".format(t1-t0))

    # but not silence the simulation.
    print(result)

if __name__ == "__main__":
    routine()
