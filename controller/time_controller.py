import datetime as dt
from abc import ABC

import chess


class TimeControllerMixin(ABC):
    start_time = None
    end_time = None
    board = None  # Needs to be defined by a search-based mixin

    def start_signal(self, *, movetime=None, wtime=None, btime=None, winc=0,
                     binc=0, movestogo=35, buffer=0):
        self.start_time = dt.datetime.now().timestamp()

        if movetime is None:
            if self.board.turn == chess.WHITE:
                timetogo = wtime
                increment = winc
            else:
                timetogo = btime
                increment = binc
            movetime = (timetogo + (increment * (movestogo - 1))) / movestogo

        self.end_time = self.start_time + (movetime - buffer) / 1000.0

    def stop_signal(self):
        return dt.datetime.now().timestamp() > self.end_time
