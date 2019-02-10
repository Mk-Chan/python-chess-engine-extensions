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


import random

import chess

from definitions import INFINITE
from evaluation.piece_square_table import PieceSquareMixin
from evaluation.piece_values import PieceValueMixin
from search.alphabeta import AlphaBetaMixin


class BadEngine(AlphaBetaMixin, PieceValueMixin):
    pass


class GoodEngine(AlphaBetaMixin, PieceValueMixin, PieceSquareMixin):
    pass


def main():
    # Start with initial position
    board = chess.Board()

    # Choose which side gets the good engine
    good_engine_side = random.sample([chess.WHITE, chess.BLACK], 1)[0]

    # Run a game playout and print status updates
    while not board.is_game_over():
        print(board)

        # Randomize depth for fun
        depth = random.randint(3, 4)

        # Generate a move depending on the side
        if board.turn == good_engine_side:
            score, pv = GoodEngine(board).search(-INFINITE, +INFINITE, depth)
        else:
            score, pv = BadEngine(board).search(-INFINITE, +INFINITE, depth)

        print(chess.COLOR_NAMES[board.turn], score, " ".join(map(str, pv)))

        # Update the current position and continue playing
        best_move = pv[0]
        board.push(best_move)

    # Print the final position and game over reason
    print(board)
    if board.is_checkmate():
        print('Checkmate!')
    elif board.is_insufficient_material():
        print('Draw by insufficient material!')
    elif board.is_stalemate():
        print('Dray by stalemate!')
    elif board.is_seventyfive_moves():
        print('Dray by 75-move rule!')
    elif board.is_fivefold_repetition():
        print('Dray by 5-fold repetition!')
    else:
        print('Unexpected game over!?')


if __name__ == '__main__':
    main()
