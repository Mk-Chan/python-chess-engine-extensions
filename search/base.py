from abc import ABC

import chess


class BaseSearch(ABC):
    def __init__(self, board: chess.Board):
        if board is None:
            raise ValueError('board must be defined')
        self.board = board
