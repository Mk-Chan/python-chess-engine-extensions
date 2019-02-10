import chess

from evaluation.base import BaseEvaluation

PIECE_VALUES = [None, 100, 300, 300, 500, 900, 0]


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
