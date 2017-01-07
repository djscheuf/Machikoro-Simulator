"""
Purpose: The Strategy represents, the desired final state of Owned cards.

+ utilize it's known end-state, and a given current-state to
    determine what action to take for the turn ( what cards to buy)
"""

from .CardEnum import *

_defaultEndState = {
    CardEnum.WheatField: 1,
    CardEnum.Bakery: 1,
    CardEnum.TrainStation: 1,
    CardEnum.ShoppingMall: 1,
    CardEnum.AmusementPark: 1,
    CardEnum.RadioTower: 1
}


class Strategy:
    def __init__(self, desired_end_state=None):
        from copy import deepcopy
        self.EndState = deepcopy(_defaultEndState)

        if desired_end_state is not None:
            for key in desired_end_state.keys():
                self.EndState[key] = desired_end_state[key]

    def get_number_toroll(self, state):
        """Returns how many dice to roll. If have train station always roll 2"""
        if CardEnum.TrainStation in state.Deck.keys() and state.Deck[CardEnum.TrainStation] > 0:
            return 2

        return 1

    def get_card_topurchase(self, state, available_cards):
        """Returns card to purchase, or NoCard"""
        #get diff_state
        diff_state = self._create_diff_state(state)

        available = False
        while not available:
            #get Cheapest next desired Card
            next_get = self._get_next_cheapest_desired_card(diff_state)

            if next_get == CardEnum.NoCard:
                next_get = CardEnum.NoCard
                available = True
                continue

            diff_state[next_get] = None
            # removes next cheapest from possibles, prevents inf loop

            if next_get in available_cards:
                available = True

        return next_get

    def _create_diff_state(self, cur_state):
        """Determines difference between current and desired states"""
        diffState = {}
        for key in list(self.EndState.keys()):
            curCnt = 0
            try:
                curCnt = cur_state.Deck[key]
            except KeyError:
                pass

            diff = self.EndState[key] - curCnt
            if diff > 0:
                diffState[key] = CardCosts[key]

        return diffState

    @staticmethod
    def _get_next_cheapest_desired_card(diff_state):
        """Finds the next cheapest card that is desirable to purchase"""
        # search for min within in Dict
        # may optimize later

        next_card = CardEnum.NoCard
        min_cost = 1e6  # Arbitrarily Large Number

        for key in list(diff_state.keys()):
            if diff_state[key] is not None:
                if diff_state[key] < min_cost:
                    next_card = key
                    min_cost = diff_state[key]

        return next_card


class StrategyFactory:
    def __init__(self):
        pass

    @staticmethod
    def default():
        end_state = {}
        return Strategy(end_state)

    @staticmethod
    def cheese_factory_strategy():
        end_state = {CardEnum.Ranch: 3, CardEnum.CheeseFactory: 3}
        return Strategy(end_state)

    @staticmethod
    def furniture_factory_strategy():
        end_state = {CardEnum.Forest: 3, CardEnum.FurnitureFactory: 3}
        return Strategy(end_state)

    @staticmethod
    def developer_strategy():
        end_state = {CardEnum.Ranch: 2, CardEnum.Bakery: 2,
                     CardEnum.ConvenienceStore: 2, CardEnum.Mine: 2,
                     CardEnum.CheeseFactory: 2, CardEnum.Forest: 2,
                     CardEnum.FurnitureFactory: 2}
        return Strategy(end_state)
