"""
Purpose: The DeckManager will:
    + track purchased/available cards
    + support PlayerBot card purchases

Knows:
    + Total Available per type
    + Current Available per type
"""

from .CardEnum import *


_defaultStartingDeck = {
    CardEnum.WheatField: 6,
    CardEnum.Ranch: 6,
    CardEnum.Bakery: 6,
    CardEnum.Cafe: 6,
    CardEnum.ConvenienceStore: 6,
    CardEnum.Forest: 6,
    CardEnum.TVStation: 4,
    CardEnum.Stadium: 4,
    CardEnum.BusinessCenter: 4,
    CardEnum.CheeseFactory: 6,
    CardEnum.FurnitureFactory: 6,
    CardEnum.Mine: 6,
    CardEnum.FamilyRestaurant: 6,
    CardEnum.AppleOrchard: 6,
    CardEnum.FruitAndVegetableStand: 6
}

_majorImprovements = [CardEnum.TrainStation, CardEnum.ShoppingMall, CardEnum.AmusementPark, CardEnum.RadioTower]

class DeckManager:
    def __init__(self):
        from copy import deepcopy
        self._deck = deepcopy(_defaultStartingDeck)

    def _iscardavailable(self, card):
        """Returns boolean flag of card availability."""
        if card in _majorImprovements:
            return True

        if card not in self._deck.keys():
            return False

        cnt = self._deck[card]
        return cnt > 0

    def request_card(self, card):
        """Request a card from the deck. If available it is awarded,
             if not, then denied"""
        if not self._iscardavailable(card):
            return False

        if card in _majorImprovements:
            return True

        self._deck[card] -= 1
        return True

    def get_availablecards(self):
        result = []

        for key in self._deck.keys():
            if self._deck[key] > 0:
                result.append(key)

        for card in _majorImprovements:
            result.append(card)

        return result
