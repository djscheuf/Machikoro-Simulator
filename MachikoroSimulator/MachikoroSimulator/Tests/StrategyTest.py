import unittest
from copy import deepcopy
from ..Strategy import *
from ..Bot import BotState
from ..CardEnum import *

#TODO: I need a better way to share this between test and code
_defaultEndState = {
    CardEnum.WheatField: 1,
    CardEnum.Bakery: 1,
    CardEnum.TrainStation: 1,
    CardEnum.ShoppingMall: 1,
    CardEnum.AmusementPark: 1,
    CardEnum.RadioTower: 1
}

class StrategyTest(unittest.TestCase):
    def setUp(self):
        self.subject = Strategy()
        self.initState = BotState()
        self.initState.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}

    def tearDown(self):
        pass

    def test_Init_NoDesireGiven(self):
        #Arrange
        #Act
        strat = Strategy()
        #Assert
        self.assertEqual(strat.EndState, _defaultEndState)

    def test_Init_DesiredStateGiven(self):
        #Arrange
        desired = {CardEnum.Ranch: 2, CardEnum.CheeseFactory: 2}

        combo = deepcopy(desired)

        for key in _defaultEndState.keys():
            combo[key] = _defaultEndState[key]

        #Act
        strat = Strategy(desired)

        #Assert
        self.assertEqual(combo,strat.EndState)

    def test_HowManyToRoll_WithTrain(self):
        #Arrange
        state = BotState()
        state.Deck = {CardEnum.TrainStation: 1}

        #Act
        roll = self.subject.get_number_toroll(state)

        #Assert
        self.assertEqual(roll, 2)

    def test_HowManyToRoll_WithoutTrain(self):
        # Arrange
        state = BotState()
        state.Deck = {}

        # Act
        roll = self.subject.get_number_toroll(state)

        # Assert
        self.assertEqual(roll, 1)

    def test_DiffState_ReturnsMissingCards(self):
        #Arrange
        expected = {
            CardEnum.TrainStation: CardCosts[CardEnum.TrainStation],
            CardEnum.ShoppingMall: CardCosts[CardEnum.ShoppingMall],
            CardEnum.AmusementPark: CardCosts[CardEnum.AmusementPark],
            CardEnum.RadioTower: CardCosts[CardEnum.RadioTower]
        }

        #Act
        diff = self.subject._create_diff_state(self.initState)

        #Assert
        for key in expected.keys():
            self.assertTrue(key in diff.keys())
            self.assertEqual(diff[key], expected[key])

    def test_DiffState_ReturnsNoneIfHaveAll(self):
        #Arrange
        state = BotState()
        state.Deck = _defaultEndState
        #Act
        diff = self.subject._create_diff_state(state)

        #Assert
        self.assertEqual(diff, {})

    def test_PurchaseCard_ReturnsCheapestMissingAndAvailableCard(self):
        # Arrange
        available = [
            CardEnum.TrainStation
        ]

        # Act
        card = self.subject.get_card_topurchase(self.initState, available)

        # Assert
        self.assertEqual(card,CardEnum.TrainStation)

    def test_PurchaseCard_ReturnsNextCheapestIfCheapestIsnotAvailable(self):
        # Arrange
        available = [
            CardEnum.ShoppingMall
        ]

        # Act
        card = self.subject.get_card_topurchase(self.initState, available)

        # Assert
        self.assertEqual(card, CardEnum.ShoppingMall)
