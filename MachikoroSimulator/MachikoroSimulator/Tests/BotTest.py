import unittest
from ..Bot import *
from ..Strategy import StrategyFactory
from ..CardEnum import CardEnum

class BotTest(unittest.TestCase):
    def setUp(self):
        self.subject = Bot()

        self.FullBot = Bot()
        state = BotState()
        state.Deck[CardEnum.WheatField] = 1
        state.Deck[CardEnum.Bakery] = 1
        state.Money = 3

        self.FullBot.initialstate(state)
        self.FullBot.with_plan(StrategyFactory().cheese_factory_strategy())

    def tearDown(self):
        pass

    def test_Init(self):
        #Arrange
        #Act
        bot = Bot()

        #Assert
        self.assertIsNone(bot._state)
        self.assertIsNone(bot._strategy)

    def test_WithPlan(self):
        #Arrange
        strat = StrategyFactory().default()
        #Act
        self.subject.with_plan(strat)
        #assert
        self.assertEqual(strat, self.subject._strategy)

    def test_InitialState(self):
        #Arrange
        state = BotState()
        state.Deck[CardEnum.WheatField] = 1
        state.Money = 1

        #Act
        self.subject.initialstate(state)

        #Assert
        self.assertEqual(self.subject._state, state)

    def test_CurrentState(self):
        # Arrange
        state = BotState()
        state.Deck[CardEnum.WheatField] = 1
        state.Money = 1

        self.subject.initialstate(state)

        #Act
        currState = self.subject.get_currentstate()

        #Assert
        self.assertEqual(state, currState)

    def test_Deduct_RemovesAmount(self):
        #Arrange

        #Act
        result = self.FullBot.deduct_money(2)

        #Assert
        state = self.FullBot.get_currentstate()
        self.assertEqual(state.Money,1)
        self.assertEqual(result, 2)

    def test_Deduct_RemovesMaximumAmountIfNotEnough(self):
        # Arrange

        # Act
        result = self.FullBot.deduct_money(4)

        # Assert
        state = self.FullBot.get_currentstate()
        self.assertEqual(state.Money, 0)
        self.assertEqual(result, 3)

    def test_Deduct_NegativeAmountRaisesException(self):
        #Arrange
        unreachableFlag = True
        #Act
        try:
            self.FullBot.deduct_money(-1)
            unreachableFlag = False
        except Exception:
            pass
        #Assert
        self.assertTrue(unreachableFlag)

    def test_Award_GivesAmount(self):
        #Arrange
        #Act
        self.FullBot.award_money(1)
        #Assert
        self.assertEqual(self.FullBot.get_currentstate().Money, 4)

    def test_Award_NegativeAmountThrowsException(self):
        # Arrange
        unreachableFlag = True
        # Act
        try:
            self.FullBot.award_money(-1)
            unreachableFlag = False
        except Exception:
            pass
        # Assert
        self.assertTrue(unreachableFlag)

    def test_AwardCard_AddsNewCardToPlayerDeck(self):
        #Arrange
        card = CardEnum.Forest
        #Act
        self.FullBot.award_card(card)
        #Assert
        state = self.FullBot.get_currentstate()
        self.assertTrue(card in state.Deck.keys())
        self.assertEqual(state.Deck[card], 1)

    def test_AwardCard_IncrementsCountOfExistingCards(self):
        #Arrange
        card = CardEnum.Bakery
        #Act
        self.FullBot.award_card(card)
        #Assert
        state = self.FullBot.get_currentstate()
        self.assertEqual(state.Deck[card], 2)