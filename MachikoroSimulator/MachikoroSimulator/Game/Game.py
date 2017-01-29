import random
from ..CardEnum import *
from copy import deepcopy


class GameResult:
    def __init__(self,winner,turns):
        self.winner = winner
        self.turns = turns


class Game:
    def __init__(self, players, engine, deck, logger):
        random.seed()
        self.winner = None
        self.total_turns = 0
        self._logger = logger

        self._players = players
        self._playerCount = len(self._players)

        self._engine = engine
        self._initialDeck = deepcopy(deck)
        self._currentDeck = deck

        self._init_game()

    def _log(self, msg):
        self._logger.debug(msg)

    def _init_game(self):
        self._currentPlayer = 0
        self._turn = 0

        self.winner = None
        self.total_turns = 0

        init_state = self._engine.initialstate()

        for player in self._players:
            player.initialstate(deepcopy(init_state))

    def run(self):
        self._log("Starting a game.")

        game_finished = False
        while not game_finished:
            self._execute_turn()
            self._log("")
            game_finished = self._engine.winconditionmet(self._players)

        self.winner = self._engine.get_winner(self._players)
        self.total_turns = self._turn

    def _execute_turn(self):
        player = self._players[self._currentPlayer]

        self._log("\tTurn {0}, Player {1}".format(self._turn, player.name))
        # Ask current player for roll.
        dicecnt = player.get_number_toroll()
        # roll
        rollnum = self._roll(dicecnt)
        self._log("\t\tPlayer rolls {0} dice, and gets a {1}".format(dicecnt, rollnum))
        # use engine to determine earning.
        #  - Steal first
        self._take_money_if_necessary(rollnum)

        # - Then Earn
        self._award_money_if_necessary(rollnum)

        state = player.get_currentstate()
        self._log("\t\tAfter money has changed hands, the player now has:{0}".format(state.Money))

        # ask current player for purchase
        card = player.get_card_topurchase(self._currentDeck.get_availablecards())

        # make purchase
        if card is not CardEnum.NoCard:
            if player.get_currentstate().Money >= CardCosts[card]:
                player.deduct_money(CardCosts[card])
                self._currentDeck.request_card(card)
                player.award_card(card)
                self._log("\tThe player purchases {0}".format(card))

        # increment current player (increment turn if back to first player)
        self._currentPlayer = self._get_next_player()
        if self._currentPlayer == 0:
            self._turn += 1

    @staticmethod
    def _roll(dice):
        """Rolls the designated number of 6 sided dice. Returns sum of dice."""
        result = 0
        i = 0
        while i < dice:
            result += random.randint(1, 6)
            i += 1
        return result

    def _take_money_if_necessary(self, roll):
        """Iterates thru all other players to determine if money is owed by rolling player."""
        currentPlayer = self._players[self._currentPlayer]
        nextIdx = self._get_next_player()
        canContinue= True

        self._log("")
        while canContinue:
            # - Determine Cards activated on other players
            nextPlayer = self._players[nextIdx]
            owed = self._engine.steals_money(nextPlayer.get_currentstate(), roll)
            self._log("\t\tPlayer {0} owes {1} {2} money.".format(currentPlayer.name, nextPlayer.name, owed))
            # - Attempt to aware going around to next
            available = currentPlayer.deduct_money(owed)
            if available is None:
                self._log("\t\t\t But had no money left...")
                canContinue = False
                continue
            else:
                nextPlayer.award_money(available)
                if owed != available:
                    self._log("\t\t\t But could only pay {0}...".format(available))
                    canContinue = False
                    continue
            self._log("\t\t\t and paid in full.")

            nextIdx = self._get_next_player(nextIdx)
            if nextIdx == self._currentPlayer:
                canContinue = False

    def _get_next_player(self, cur_idx=None):
        idx = cur_idx
        if cur_idx is None:
            idx = self._currentPlayer

        return (idx + 1) % self._playerCount

    def _award_money_if_necessary(self, roll):
        """Iterates thru all players and awards money from bank as applicable."""
        # Iterate thru other players first

        self._log("")
        next_idx = self._get_next_player(self._currentPlayer)
        while next_idx != self._currentPlayer:
            player = self._players[next_idx]
            earned = self._engine.earns_money(player.get_currentstate(), roll, False)
            # False because it is not the players turn
            self._log("\t\t{0} earned {1} for their blues.".format(player.name, earned))
            player.award_money(earned)
            next_idx = self._get_next_player(next_idx)

        # Award money to current player
        player = self._players[self._currentPlayer]
        earned = self._engine.earns_money(player.get_currentstate(), roll, True)
        self._log("\t\t{0} earned {1} for their blues and greens.".format(player.name, earned))
        player.award_money(earned)

    def reset(self):
        self._currentDeck = deepcopy(self._initialDeck)
        self._init_game()
        self._randomize_first_player()

    def _randomize_first_player(self):
        self._currentPlayer = random.randint(0, self._playerCount-1)

    def get_players(self):
        result = []
        for player in self._players:
            result.append(player.name)

        return result

    def get_result(self):
        return GameResult(self.winner, self.total_turns)
