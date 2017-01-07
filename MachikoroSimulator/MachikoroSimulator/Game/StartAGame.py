from .PlayerContext import PlayerContext


class StartAGame:
    @staticmethod
    def with_(first, second):
        return PlayerContext(first, second)
