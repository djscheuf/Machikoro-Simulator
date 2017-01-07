from .Game import Game


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

        self._players.add(player)
        self._count += 1

    def using(self, engine, deck):
        return Game(self._players, engine, deck)
