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


import datetime as dt
import random

import chess

from controller.time_controller import TimeControllerMixin
from definitions import INFINITE, MAX_PLY, MATE, MIN_MATE_SCORE
from evaluation.mixins import PieceSquareMixin, PieceValueMixin
from search.alphabeta import AlphaBetaMixin
from search.minimax import MinimaxMixin


class BadEngine(TimeControllerMixin, MinimaxMixin, PieceValueMixin):
    pass


class GoodEngine(TimeControllerMixin, AlphaBetaMixin, PieceValueMixin, PieceSquareMixin):
    pass


def main():
    # Start with initial position
    board = chess.Board()

    # Choose which side gets the good engine
    good_engine_side = random.sample([chess.WHITE, chess.BLACK], 1)[0]

    # Run a game playout and print status updates
    while not board.is_game_over():
        print(board)

        # Fixed time match
        movetime = 2000

        if board.turn == good_engine_side:
            engine = GoodEngine(board)
        else:
            engine = BadEngine(board)

        engine.start_signal(movetime=movetime)  # Begin the internal timer
        for depth in range(1, MAX_PLY):
            if isinstance(engine, GoodEngine):
                score, _pv = engine.search(-INFINITE, +INFINITE, depth)
            else:
                score, _pv = engine.search(depth)
            if engine.stop_signal():
                break
            pv = _pv
            print(f'info score', end=" ")
            if score >= MIN_MATE_SCORE:
                mate_dist = int((MATE - score + 1) / 2)
                print(f'mate {mate_dist}', end=" ")
            elif score <= -MIN_MATE_SCORE:
                mate_dist = -int((score + MATE + 1) / 2)
                print(f'mate {mate_dist}', end=" ")
            else:
                print(f'cp {score}', end=" ")
            print(f'depth {depth}', end=" ")
            print(f'time {int((dt.datetime.now().timestamp() - engine.start_time) * 1000)}', end=" ")
            print("moves", " ".join(map(str, pv)))

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
