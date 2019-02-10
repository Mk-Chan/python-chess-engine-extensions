import chess

from definitions import INFINITE, MAX_PLY, MATE
from search.base import BaseSearch


def is_drawn(board: chess.Board):
    return board.is_fivefold_repetition() \
           or board.is_stalemate() \
           or board.is_seventyfive_moves() \
           or board.is_insufficient_material()


class MinimaxMixin(BaseSearch):
    def search(self, depth, ply=0):
        """
        Search `self.board` with the `self.evaluate` using the
        minimax algorithm.

        The implementation is in a Negamax arrangement.
        -> Here, we try to avoid repeating code for the min and max nodes by
           fixing a positive score for White and negative score for Black.
        -> Consider the root node as a max-node.
        -> When searching a min-node, we can simply maximize the negative score
           to achieve the same effect as minimizing the score.
        -> The score returned to the parent then needs to be negated to retrieve
           the actual value.

        :param depth: Remaining depth to search.
        :param ply: Depth of the current node.

        :return: (score, pv)
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

        best_value = -INFINITE
        pv = []
        for move in self.board.legal_moves:
            self.board.push(move)
            search_value, child_pv = self.search(depth - 1, ply + 1)
            search_value = -search_value
            self.board.pop()

            if search_value > best_value:
                best_value = search_value
                pv = [move] + child_pv

        return best_value, pv
