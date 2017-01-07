import unittest
from ...Engine import Engine
from ...Bot import *
from ...CardEnum import CardEnum
from ...DeckManager import _defaultStartingDeck
from copy import deepcopy


class EngineTest(unittest.TestCase):
    def setUp(self):
        state = BotState()
        state.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}
        state.Money = 3
        self.initPlayerState = state
        self.initDeck = _defaultStartingDeck

        self.subject = Engine.Engine(self.initPlayerState, self.initDeck)

        winState = BotState()
        winState.Deck = {CardEnum.TrainStation: 1, CardEnum.ShoppingMall: 1, CardEnum.AmusementPark: 1, CardEnum.RadioTower: 1}
        self.winningState = winState

    def tearDown(self):
        pass

    def _createPlayer(self,state):
        bot = Bot()
        bot.initialstate(state)
        return bot

    def test_Init(self):
        # Arrange
        # Act
        engine = Engine.Engine(self.initPlayerState, self.initDeck)
        # Assert
        self.assertEqual(engine._currentDeck, self.initDeck)
        self.assertEqual(engine._initPlayerState, self.initPlayerState)
        self.assertEqual(engine._initialDeck, self.initDeck)

    def test_WinCondition_1PlayerPasses(self):
        #Arrange
        players = [self._createPlayer(self.winningState)]
        #Act
        result = self.subject.winconditionmet(players)
        #Assert
        self.assertTrue(result)

    def test_WinCondition_NPlayersPasses(self):
        #Arrange
        players = [self._createPlayer(self.winningState), self._createPlayer(self.winningState),
                   self._createPlayer(self.winningState), self._createPlayer(self.winningState)]
        #Act
        result = self.subject.winconditionmet(players)
        #Assert
        self.assertTrue(result)

    def test_WinCondition_EmptyPlayers(self):
        #Arrange
        players = []
        #Act
        result = self.subject.winconditionmet(players)
        #Assert
        self.assertFalse(result)

    def test_WinContion_None(self):
        # Arrange
        # Act
        result = self.subject.winconditionmet(None)
        # Assert
        self.assertFalse(result)

    def test_GetWinner_LastPlayerWins(self):
        #Arrange
        winState = deepcopy(self.winningState)
        winState.Money=999
        players = [self._createPlayer(self.initPlayerState), self._createPlayer(winState)]
        #Act
        winner = self.subject.get_winner(players)
        #Assert
        self.assertEqual(winner.get_currentstate(), winState)

    def test_GetWinner_ReturnsFirstWinner(self):
        # Arrange
        winState = deepcopy(self.winningState)
        winState.Money = 999
        players = [self._createPlayer(self.initPlayerState), self._createPlayer(self.winningState),
                   self._createPlayer(winState)]
        # Act
        winner = self.subject.get_winner(players)
        # Assert
        self.assertEqual(winner.get_currentstate(), self.winningState)

    def test_Getwinner_ReturnsFirstWinner(self):
        # Arrange
        players = None
        # Act
        winner = self.subject.get_winner(players)
        # Assert
        self.assertEqual(winner, None)

    def test_EarnsMoney_FromGreenOnlyOnTurn(self):
        #Arrange
        #Act - 3 Activated Bakery, a green
        onTurn = self.subject.earns_money(self.initPlayerState, 3, True)
        offTurn = self.subject.earns_money(self.initPlayerState, 3, False)
        #Assert
        self.assertNotEqual(onTurn, offTurn)
        self.assertEqual(offTurn, 0)
        self.assertTrue(onTurn > 0)

    def test_EarnsMoney_FromBluesWhenever(self):
        # Arrange
        # Act - 1 Activated WheatField, a Blue
        onTurn = self.subject.earns_money(self.initPlayerState, 1, True)
        offTurn = self.subject.earns_money(self.initPlayerState, 1, False)
        # Assert
        self.assertEqual(onTurn, offTurn)
        self.assertTrue(onTurn > 0)
        self.assertTrue(offTurn > 0)

    def test_EarnsMoney_Zero_IfNoActivation(self):
        # Arrange
        # Act - 6 Technically activates a purple, but these are not implemented, so no activations.
        onTurn = self.subject.earns_money(self.initPlayerState, 6, True)
        offTurn = self.subject.earns_money(self.initPlayerState, 6, False)
        # Assert
        self.assertEqual(onTurn, offTurn)
        self.assertEqual(onTurn, 0)
        self.assertEqual(offTurn, 0)

    def test_EarnsMoney_FromRedsOnlyOffTurn(self):
        # Arrange
        redState = BotState()
        redState.Deck[CardEnum.Cafe] = 1
        # Act - 3 Activated Cafe, a red
        onTurn = self.subject.earns_money(redState, 3, True)
        offTurn = self.subject.steals_money(redState, 3)
        # Assert
        self.assertNotEqual(onTurn, offTurn)
        self.assertEqual(onTurn, 0)
        self.assertTrue(offTurn > 0)

    def test_EarnsMoney_FromCheeseFactory(self):
        #Arrange
        factoryState = BotState()
        factoryState.Deck[CardEnum.Ranch] = 2
        factoryState.Deck[CardEnum.CheeseFactory] = 1
        #Act
        result = self.subject.earns_money(factoryState, 7, True)
        #Assert
        self.assertEqual(result,6)

    def test_EarnsMoney_FromFurnitureFactory(self):
        #Arrange
        factoryState = BotState()
        factoryState.Deck[CardEnum.Forest] = 2
        factoryState.Deck[CardEnum.Mine] = 1
        factoryState.Deck[CardEnum.FurnitureFactory] = 1
        #Act
        result = self.subject.earns_money(factoryState, 8, True)
        #Assert
        self.assertEqual(result,9)

    def test_EarnsMoney_FromFruitAndVegetableStand(self):
        #Arrange
        factoryState = BotState()
        factoryState.Deck[CardEnum.WheatField] = 2
        factoryState.Deck[CardEnum.AppleOrchard] = 2
        factoryState.Deck[CardEnum.FruitAndVegetableStand] = 1
        #Act
        result = self.subject.earns_money(factoryState, 11, True)
        #Assert
        self.assertEqual(result,8)