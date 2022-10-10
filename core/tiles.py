"""

Tile Types:
    - Push
        - moves target 1 away
    - Corner Push
        - moves target 1 diagonal away
    - Slide Left
        - moves target 1 left
    - Slide Right
        - moves target 1 right
    - Pull Left
        - moves target left and towards (1 diagonal)
    - Pull Right
        - moves target right and towards (1 diagonal)
    - Long Shot
        - targets 2 spaces away, moves target 1 away
    - Corner Long Shot
        - targets 2 spaces away, moves target 1 diagonal away
    - Decision
        - moves target 1 left OR right [decision]
    - Rephrase
        - rotate target X degrees
        - can target your own tiles
    - Toss
        - moves target one space behind self
    - Persuade
        - moves target and self 1 backwards
"""

import abc
from enum import IntEnum
from typing import Optional, Tuple, Union
import uuid

from aenum import MultiValueEnum

from core.game import Player
from core.exceptions import TileNotFound, TileLocOffBoard


class TileAngle(MultiValueEnum):
    N = 0, "↑", (-1, 0)
    NE = 45, "↗", (-1, 1)
    E = 90, "→", (0, 1)
    SE = 135, "↘", (1, 1)
    S = 180, "↓", (1, 0)
    SW = 225, "↙", (1, -1)
    W = 270, "←", (0, -1)
    NW = 315, "↖", (-1, -1)


class Tile(abc.ABC):
    def __init__(self, *, player: Player = None, angle: Union[TileAngle, int] = None, id=None):
        self.id = id or str(uuid.uuid4())
        self.player = player
        if isinstance(angle, int):
            self.angle = TileAngle(angle)
        else:
            self.angle = angle

        # NOTE: connection to board
        self.board = None

    def __repr__(self):
        return f"<{self.__class__.__name__}:'{self.id[:6]}',({self.player},{self.angle.name}{self.angle.values[1]},{self.loc})>"

    @abc.abstractmethod
    def action(self, target_tile):
        pass

    @property
    def target_vector(self):
        v = self.angle.values[2]
        # TODO: handle "long" targeting tiles by bumping +1 where appropriate
        return v

    @property
    def loc(self):
        if self.board is None:
            return (None, None)
        return self.board.loc(self.id)

    def get_target_tile(self):

        row, col = self.loc

        # targeting vector
        d_row, d_col = self.target_vector

        # calc target loc
        t_row, t_col = row + d_row, col + d_col
        if t_row < 0 or t_row >= self.board.width or t_col < 0 or t_col >= self.board.height:
            raise TileLocOffBoard(f"target loc off board: {(t_row, t_col)}")

        return self.board[t_row][t_col]


class ProxyTile(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action(self, t_loc):
        pass


class PushTile(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action(self, t_loc):
        return t_loc[0] + 0, t_loc[1] + 1
