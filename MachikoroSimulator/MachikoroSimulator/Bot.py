"""
Purpose: A Bot is the element which knows how ot use a strategy.
  It contains the state a given strategy acts upon, and provides the desicions
      to the game engine.

Has a strategy
Knows Bot's current state:
  - Bot's current deck ( separate from Game deck)
  - Bot's current money
Decides:
  - Roll 1 or 2
  - Purchase? (Boolean)
  - - Purchase what? (which card)
"""


class BotState:
    def __init__(self):
        self.Deck = {}
        self.Money = 0

    @staticmethod
    def default():
        from .CardEnum import CardEnum
        state = BotState()
        state.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}
        state.Money = 3

        return state


class Bot:
    def __init__(self, name="unassigned"):
        self._state = None
        self._strategy = None
        self.name = name

    def with_plan(self, strategy):
        """Provides Bot with a Plan to follow"""
        self._strategy = strategy

    def initialstate(self, state):
        """Initialized Bot state at the beginning of a game."""
        self._state = state

    def get_currentstate(self):
        """Returns the current state of the bot"""
        return self._state

    def get_number_toroll(self):
        """Asks bot how many dice to roll"""
        return self._strategy.get_number_toroll(self._state)

    def get_card_topurchase(self, availablecards):
        """Returns card to purchase or NoCard if undesired."""
        return self._strategy.get_card_topurchase(self._state, availablecards)

    def deduct_money(self, owed):

        if owed < 0:
            raise Exception("Cannot Deduct negative amount")

        result = 0
        if owed > self._state.Money:
            result = self._state.Money
            self._state.Money = 0
        else:
            result = owed
            self._state.Money -= owed

        return result

    def award_money(self, earned):
        if earned < 0:
            raise Exception("Cannot Award a negative amount.")

        self._state.Money += earned

    def award_card(self, card):
        if card in self._state.Deck.keys():
            self._state.Deck[card] += 1
        else:
            self._state.Deck[card] = 1
