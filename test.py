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


import unittest

import chess

from evaluation.mixins import PieceValueMixin, PieceSquareMixin
from evaluation.piece_square_tables import PIECE_SQUARE_TABLES
from evaluation.piece_values import PIECE_VALUES


class EvaluationTest(unittest.TestCase):
    def run_test(self, eval_cls, fen, evaluation):
        self.assertEqual(evaluation, eval_cls(chess.Board(fen)).evaluate())

    def test_piece_value_eval(self):
        self.run_test(PieceValueMixin, chess.STARTING_FEN,
                      0)
        self.run_test(PieceValueMixin, "8/8/8/8/8/8/1P6/8 w - - 0 1",
                      PIECE_VALUES[chess.PAWN])
        self.run_test(PieceValueMixin, "8/5p2/8/8/8/8/8/8 w - - 0 1",
                      -PIECE_VALUES[chess.PAWN])
        self.run_test(PieceValueMixin, "8/5pr1/8/8/8/8/8/8 w - - 0 1",
                      -PIECE_VALUES[chess.PAWN] - PIECE_VALUES[chess.ROOK])
        self.run_test(PieceValueMixin, "8/5pr1/8/8/8/8/8/8 b - - 0 1",
                      PIECE_VALUES[chess.PAWN] + PIECE_VALUES[chess.ROOK])

    def test_piece_square_table_eval(self):
        self.run_test(PieceSquareMixin, chess.STARTING_FEN,
                      0)
        self.run_test(PieceSquareMixin, "8/8/8/8/8/8/1P6/8 w - - 0 1",
                      PIECE_SQUARE_TABLES[chess.PAWN][chess.B2])
        self.run_test(PieceSquareMixin, "8/5P2/8/8/8/8/8/8 w - - 0 1",
                      PIECE_SQUARE_TABLES[chess.PAWN][chess.G7])
        self.run_test(PieceSquareMixin, "8/5p2/8/8/8/8/r7/8 w - - 0 1",
                      -PIECE_SQUARE_TABLES[chess.PAWN][chess.G2]
                      - PIECE_SQUARE_TABLES[chess.ROOK][chess.A7])
        self.run_test(PieceSquareMixin, "8/5p2/8/8/8/8/r7/8 b - - 0 1",
                      PIECE_SQUARE_TABLES[chess.PAWN][chess.G2]
                      + PIECE_SQUARE_TABLES[chess.ROOK][chess.A7])


if __name__ == "__main__":
    unittest.main()
