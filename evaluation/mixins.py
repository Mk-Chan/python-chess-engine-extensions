# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-engine-extensions library.
# Copyright (C) 2019 Manik Charan <mkchan2951@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import chess

from evaluation.piece_square_tables import PIECE_SQUARE_TABLES
from evaluation.piece_values import PIECE_VALUES


class BaseEvaluation(object):
    def __init__(self, board: chess.Board):
        if board is None:
            raise ValueError('board must be defined')
        self.board = board

    def evaluate(self):
        return 0


class PieceValueMixin(BaseEvaluation):
    def evaluate(self):
        parent_score = super(PieceValueMixin, self).evaluate()
        score = 0
        for piece_type in chess.PIECE_TYPES:
            pieces_mask = self.board.pieces_mask(piece_type, chess.WHITE)
            score += chess.popcount(pieces_mask) * PIECE_VALUES[piece_type]
        for piece_type in chess.PIECE_TYPES:
            pieces_mask = self.board.pieces_mask(piece_type, chess.BLACK)
            score -= chess.popcount(pieces_mask) * PIECE_VALUES[piece_type]

        if self.board.turn == chess.BLACK:
            score = -score
        return score + parent_score


class PieceSquareMixin(BaseEvaluation):
    def evaluate(self):
        parent_score = super(PieceSquareMixin, self).evaluate()
        score = 0
        for piece_type in chess.PIECE_TYPES:
            for square in self.board.pieces(piece_type, chess.WHITE):
                score += PIECE_SQUARE_TABLES[piece_type][square]
            for square in self.board.pieces(piece_type, chess.BLACK):
                score -= PIECE_SQUARE_TABLES[piece_type][square ^ 56]

        if self.board.turn == chess.BLACK:
            score = -score
        return score + parent_score
