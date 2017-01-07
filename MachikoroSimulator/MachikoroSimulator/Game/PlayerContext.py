from .Game import Game


class PlayerContext:
    maxPlayers = 4

    def __init__(self, first, second):
        self._players = []
        self._players.append(first)
        self._players.append(second)
        self._count = 2

    def and_(self, player):
        #TODO May want to get the fluent decorator for these...
        if self._count >= PlayerContext.maxPlayers:
            raise Exception("Too many players added.")

        from copy import deepcopy
        context = deepcopy(self)

        context._players.append(player)
        context._count += 1

        return context

    def using(self, engine, deck):
        return Game(self._players, engine, deck)
