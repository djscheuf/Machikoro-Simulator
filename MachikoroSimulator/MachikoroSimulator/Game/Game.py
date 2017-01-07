import random
from ..CardEnum import *
from copy import deepcopy

class Game():
    def __init__(self, players, engine, deck):
        self._players = players

        self._playerCount = len(self._players)

        self._engine = engine
        self._initialDeck = deepcopy(deck)
        self._currentDeck = deck

        self._initializeGame()

    def _initializeGame(self):
        random.seed()
        initState = self._engine.initialstate()

        for player in self._players:
            player.initialstate(deepcopy(initState))

        self._currentPlayer = 0
        self._turn = 0

    def Run(self):
        print("Starting a game.")

        gameFinished = False
        while not gameFinished:
            self._executeTurn()
            print()
            gameFinished = self._engine.winconditionmet(self._players)

        self.winner = self._engine.get_winner(self._players)
        self.total_turns = self._turn

    def _executeTurn(self):
        player = self._players[self._currentPlayer]

        print("\tTurn {0}, Player {1}".format(self._turn, player.name))
        # Ask current player for roll.
        dicecnt = player.get_number_toroll()
        # roll
        rollnum = self._roll(dicecnt)
        print("\tPlayer rolls {0} dice, and gets a {1}".format(dicecnt, rollnum))
        # use engine to determine earning.
        #  - Steal first
        self._TakeMoneyIfNecessary(rollnum)

        # - Then Earn
        self._AwardMoneyIfNecessary(rollnum)

        state = player.get_currentstate()
        print("\tAfter money has changed hands, the player now has:{0}".format(state.Money))

        # ask current player for purchase
        card = player.get_card_topurchase(self._currentDeck.get_availablecards())

        # make purchase
        if card is not CardEnum.NoCard:
            if player.get_currentstate().Money >= CardCosts[card]:
                player.deduct_money(CardCosts[card])
                self._currentDeck.request_card(card)
                player.award_card(card)
                print("\tThe player purchases {0}".format(card))

        # increment current player (increment turn if back to first player)
        self._currentPlayer = self._getNextPlayerIndex()
        if self._currentPlayer == 0:
            self._turn += 1

    def _roll(self, dice):
        """Rolls the designated number of 6 sided dice. Returns sum of dice."""
        result = 0
        i = 0
        while i < dice:
            result += random.randint(1, 6)
            i += 1
        return result

    def _TakeMoneyIfNecessary(self,rollnum):
        """Iterates thru all other players to determine if money is owed by rolling player."""
        currentPlayer = self._players[self._currentPlayer]
        nextIdx = self._getNextPlayerIndex()
        canContinue= True

        while canContinue:
            # - Determine Cards activated on other players
            nextPlayer = self._players[nextIdx]
            owed = self._engine.steals_money(nextPlayer.get_currentstate(), rollnum)

            # - Attempt to aware going around to next
            available = currentPlayer.deduct_money(owed)
            if available is None:
                canContinue = False
                continue
            else:
                nextPlayer.award_money(available)
                if owed != available:
                    canContinue = False
                    continue

            nextIdx = self._getNextPlayerIndex(nextIdx)
            if nextIdx == self._currentPlayer:
                canContinue = False

    def _getNextPlayerIndex(self, curIdx = None):
        idx = curIdx
        if curIdx is None:
            idx = self._currentPlayer

        return (idx + 1) % self._playerCount

    def _AwardMoneyIfNecessary(self, rollnum):
        """Iterates thru all players and awards money from bank as applicable."""
        # Iterate thru other players first
        nextIdx = self._getNextPlayerIndex(self._currentPlayer)
        while nextIdx != self._currentPlayer:
            player = self._players[nextIdx]
            earned = self._engine.earns_money(player.get_currentstate(), rollnum, False)
            # False because it is not the players turn
            player.award_money(earned)
            nextIdx = self._getNextPlayerIndex(nextIdx)

        # Award money to current player
        player = self._players[self._currentPlayer]
        earned = self._engine.earns_money(player.get_currentstate(), rollnum, True)
        player.award_money(earned)

    def Reset(self):
        self._currentDeck = deepcopy(self._initialDeck)
        self._initializeGame()
