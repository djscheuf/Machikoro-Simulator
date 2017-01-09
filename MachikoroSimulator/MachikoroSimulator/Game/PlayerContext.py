from .Game import Game
from copy import deepcopy


class PlayerContext:
    maxPlayers = 4

    def __init__(self, first, second):
        self._players = []
        self._players.append(first)
        self._players.append(second)
        self._count = 2

    def and_(self, player):
        if self._count >= PlayerContext.maxPlayers:
            raise Exception("Too many players added.")

        context = deepcopy(self)
        context._players.append(player)
        context._count += 1

        return context

    def using(self, engine, deck):
        return Game(self._players, engine, deck)
