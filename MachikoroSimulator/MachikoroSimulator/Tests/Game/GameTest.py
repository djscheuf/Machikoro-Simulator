import unittest
from ...DeckManager import *
from ...Bot import *
from ...Engine.Engine import Engine
from ...Game.Game import Game
from ...Strategy import StrategyFactory

class GameTest(unittest.TestCase):
    def setUp(self):
        state = BotState()
        state.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}
        state.Money = 3

        self._initPlayerState = state
        self.engine = Engine(self._initPlayerState)
        self.deck = DeckManager()

        self.basePlayers = [Bot(), Bot()]
        self.subject = Game(self.basePlayers,self.engine, self.deck)

    def _initState(self):
        state = BotState()
        state.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}
        state.Money = 3

        return state

    def _goodState(self):
        state = self._initState()

        state.Deck[CardEnum.Ranch] = 3
        state.Deck[CardEnum.CheeseFactory] = 2
        state.Money = 10

        return state

    def _badState(self):
        state = self._initState()
        state.Money = 1

        return state

    def _createSmartPlayer(self):
        state = BotState()
        state.Deck = {CardEnum.WheatField: 1, CardEnum.Bakery: 1}
        state.Money = 3

        strat = StrategyFactory().cheese_factory_strategy()

        bot = Bot()
        bot.initialstate(state)
        bot.with_plan(strat)

        return bot

    def tearDown(self):
        pass

    def test_Init(self):
        #Arrange
        #performed by Setup
        #Act
        game = Game(self.basePlayers, self.engine,self.deck)
        #Assert
        self.assertIsNotNone(game)
        self.assertEqual(game._currentDeck, self.deck)
        self.assertEqual(game._playerCount, 2)
        self.assertEqual(self.basePlayers[0].get_currentstate(), self._initPlayerState)
        self.assertEqual(game._currentPlayer, 0)
        self.assertEqual(game._turn, 0)

    def test_Roll_1Die(self):
        #Arrange
        #performed by setup
        #Act
        roll = self.subject._roll(1)
        #Assert
        self.assertTrue(roll >= 1)
        self.assertTrue(roll <= 6)

    def test_Roll_2Dice(self):
        #Arrange
        #performed by setup
        #Act
        roll = self.subject._roll(2)
        #Assert
        self.assertTrue(roll >= 2)
        self.assertTrue(roll <= 12)

    def test_NextPlayerIndex(self):
        #Arrange
        #performed by setup
        #Act
        idx = self.subject._get_next_player()
        #Assert
        self.assertEqual(1, idx)

    def test_NextPlayerIndex_LoopsOnLastPlayer(self):
        #Arrange
        self.subject._currentPlayer = 1 #since there are 2 players
        #Act
        idx = self.subject._get_next_player()
        #Assert
        self.assertEqual(0, idx)

    def test_NextPlayerIndex_GivenIndex(self):
        #Arrange
        #Act
        idx = self.subject._get_next_player(1) # should loop since last player
        #Assert
        self.assertEqual(0, idx)

    def test_TakeMoney_RollNotOnARed(self):
        #Arrange
        self.basePlayers[0].initialstate(self._goodState())
        self.basePlayers[1].initialstate(self._badState())

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        #Act
        self.subject._take_money_if_necessary(2)

        #Assert
        #Confirms no money changed hands
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 10)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 1)

    def test_TakeMoney_RollOnARedButNoReds(self):
        #Arrange
        self.basePlayers[0].initialstate(self._goodState())
        self.basePlayers[1].initialstate(self._badState())

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        #Act
        self.subject._take_money_if_necessary(3) # a 3 would activate a cafe, if there was one.

        #Assert
        #Confirms no money changed hands
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 10)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 1)

    def test_TakeMoney_RollOnARed(self):
        #Arrange
        self.basePlayers[0].initialstate(self._goodState())
        redState = self._badState()
        redState.Deck[CardEnum.Cafe] = 1
        self.basePlayers[1].initialstate(redState)

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        #Act
        self.subject._take_money_if_necessary(3) # a 3 would activate a cafe, if there was one.

        #Assert
        #Confirms money changed hands
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 9)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 2)

    def test_AwardMoney_RollABlue(self):
        # Arrange
        self.basePlayers[0].initialstate(self._goodState())
        self.basePlayers[1].initialstate(self._badState())

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        # Act
        self.subject._award_money_if_necessary(1)

        # Assert
        # Confirms everyone gets something
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 11)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 2)

    def test_AwardMoney_RollABlueAndAGreen(self):
        # Arrange
        good = self._goodState()
        good.Deck[CardEnum.Ranch] = 1
        self.basePlayers[0].initialstate(good)
        bad = self._badState()
        bad.Deck[CardEnum.Ranch] = 1
        self.basePlayers[1].initialstate(bad)

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        # Act
        self.subject._award_money_if_necessary(2) # a 2 hits both ranch and bakery

        # Assert
        # Confirms everyone gets something, but Current gets more
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 12)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 2)

    def test_AwardMoney_RollEmpty(self):
        # Arrange
        self.basePlayers[0].initialstate(self._goodState())
        self.basePlayers[1].initialstate(self._badState())

        # Hacky hacky hacky!
        self.subject._players = self.basePlayers
        # Act
        self.subject._award_money_if_necessary(6)

        # Assert
        # Confirms nobody gets anything
        self.assertEqual(self.basePlayers[0].get_currentstate().Money, 10)
        self.assertEqual(self.basePlayers[1].get_currentstate().Money, 1)

    def test_ExecTurn_IncrementsNextPLayerButNotTurnIfNotLastPlayer(self):
        #Arrange
        players = [self._createSmartPlayer(), self._createSmartPlayer()]
        self.subject._players = players
        self.subject._init_game()

        #Act
        self.subject._execute_turn()

        # Assert
        self.assertEqual(self.subject._turn, 0)
        self.assertEqual(self.subject._currentPlayer, 1)

    def test_ExecTurn_IncrementsNextPLayerAndTurnIfLastPlayer(self):
        #Arrange
        players = [self._createSmartPlayer(), self._createSmartPlayer()]
        self.subject._players = players
        self.subject._init_game()

        self.subject._currentPlayer = 1

        #Act
        self.subject._execute_turn()

        # Assert
        self.assertEqual(self.subject._turn, 1)
        self.assertEqual(self.subject._currentPlayer, 0)
