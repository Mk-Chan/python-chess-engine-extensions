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

from definitions import INFINITE, MAX_PLY, MATE
from evaluation.piece_values import PIECE_VALUES
from search.base import BaseSearch


def move_sorting_policy(board: chess.Board, m: chess.Move):
    """
    Simple policy that uses the MVV-LVA technique to sort captures
    and ensure captures are placed before quiet moves.

    :param board: The current position.
    :param m: The move to sort.
    :return: The score of the move.
             Higher scores are placed earlier in the list.
    """
    moving_piece = board.piece_at(m.from_square)
    attacked_piece = board.piece_at(m.to_square)
    order = 0
    if attacked_piece:
        # Using the fact that piece types have values:
        # P=1, N=2, B=3, R=4, Q=5, K=6,
        order = PIECE_VALUES[attacked_piece.piece_type] - moving_piece.piece_type
    return order


def is_drawn(board: chess.Board):
    return board.is_fivefold_repetition() \
        or board.is_stalemate() \
        or board.is_seventyfive_moves() \
        or board.is_insufficient_material()


class AlphaBetaMixin(BaseSearch):
    def search(self, alpha, beta, depth, ply=0):
        """
        Search `self.board` with the `self.evaluate` using the
        Alpha-Beta Pruning algorithm.

        The implementation is in a Negamax arrangement.
        -> Here, we try to avoid repeating code for the min and max nodes by
           fixing a positive score for White and negative score for Black.
        -> Consider the root node as a max-node.
        -> When searching a min-node, we can simply maximize the negative score
           to achieve the same effect as minimizing the score.
        -> The score returned to the parent then needs to be negated to retrieve
           the actual value.
        -> Since we are maximizing the negative score of a child and negating the
           return value, our (alpha, beta) bounds become (-beta, -alpha) instead.

        * Note: Alpha-cutoffs become beta-cutoffs since we have normalized all
                nodes to max-nodes.

        :param alpha: Lower limit of the score.
        :param beta: Upper limit of the score.
        :param depth: Remaining depth to search.
        :param ply: Depth of the current node.
                    Default: 0 - for the root node.

        :return: (score, pv).
        """
        if depth <= 0:
            # This is a leaf node. So use plain evaluation or quiescence search.
            return self.evaluate(), []

        if ply >= MAX_PLY:
            # Hard stop on search depth.
            return self.evaluate(), []

        if self.board.is_checkmate():
            # Board is in checkmate, return a distance from mate score.
            return -MATE + ply, []

        if is_drawn(self.board):
            # Five-fold repetition is a draw.
            return 0, []

        if self.stop_signal():
            # We met a stop condition, abort and return.
            return 0, []

        # Sort moves according to a given policy to maximize beta-cutoffs.
        legal_moves = sorted(self.board.legal_moves, reverse=True,
                             key=lambda m: move_sorting_policy(self.board, m))

        best_score = -INFINITE
        pv = []
        for move in legal_moves:
            self.board.push(move)

            # The bounds are inverted and negated due to Negamax.
            child_score, child_pv = self.search(-beta, -alpha, depth - 1, ply + 1)
            # The return value is negated due to Negamax.
            child_score = -child_score

            self.board.pop()

            if child_score >= beta:
                # Beta-cutoff. This was a CUT-node.
                return beta, []

            if child_score > best_score:
                # The best move till now, but PV is not updated since it
                # does not necessarily beat alpha.
                best_score = child_score

                if best_score > alpha:
                    # The move beats (and therefore raises) alpha. PV
                    # can be updated.
                    alpha = best_score
                    pv = [move] + child_pv

        # If alpha was raised (and did not cause a beta-cutoff), then the node
        # is considered a PV-node. Otherwise it is an ALL-node.
        return alpha, pv
