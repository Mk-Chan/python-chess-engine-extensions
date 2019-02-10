import chess


class BaseEvaluation(object):
    def __init__(self, board: chess.Board):
        if board is None:
            raise ValueError('board must be defined')
        self.board = board

    def evaluate(self):
        return 0
