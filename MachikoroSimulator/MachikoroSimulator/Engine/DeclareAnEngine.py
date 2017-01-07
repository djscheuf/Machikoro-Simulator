from ..Bot import BotState
from .Engine import Engine


class DeclareAnEngine:
    # May need more context for the engine ( needs a win condition)
    @staticmethod
    def with_initial_state(deck, money):
        """"provides initialization context for an engine"""
        state = BotState()
        state.Deck = deck
        state.Money = money

        return Engine(state)
