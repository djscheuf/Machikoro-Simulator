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


def routine():
    print("Machikoro Simulator v0.0")

    p1 = Bot("Cheese Bot")
    p1.with_plan(Strategy.StrategyFactory.cheese_factory_strategy())

    p3 = Bot("Dev Bot")
    p3.with_plan(Strategy.StrategyFactory.developer_strategy())

    p2 = Bot("Furniture Bot")
    p2.with_plan(Strategy.StrategyFactory.furniture_factory_strategy())

    engine = DeclareAnEngine.with_initial_state({CardEnum.WheatField: 1, CardEnum.Bakery: 1}, 3)

    deck = DeckManager()

    game = StartAGame.with_(p1, p2).and_(p3).using(engine, deck)
    print("Set up a game between {0}, {1}, with the standard deck, and starting state.".format(p1.name, p2.name))
    game.Run()

    #print some result info
    print("Game completed in {0} turns.".format(game.total_turns))
    winner = game.winner
    print("Winner is {0}, with {1} money.".format(winner.name, winner.get_currentstate().Money))


if __name__ == "__main__":
    routine()
