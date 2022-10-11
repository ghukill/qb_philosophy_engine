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
from typing import Union
import uuid

from aenum import MultiValueEnum

from core.game import Player


class TileAngle(MultiValueEnum):
    N = 0, "↑", (-1, 0)
    # NE = 45, "↗", (-1, 1) # NOTE: removed diagnoal angle positions
    E = 90, "→", (0, 1)
    # SE = 135, "↘", (1, 1) # NOTE: removed diagnoal angle positions
    S = 180, "↓", (1, 0)
    # SW = 225, "↙", (1, -1) # NOTE: removed diagnoal angle positions
    W = 270, "←", (0, -1)
    # NW = 315, "↖", (-1, -1) # NOTE: removed diagnoal angle positions


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

    def __hash__(self):
        return hash(self.id)

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

        r, c = self.loc

        # get targeting vector and calc loc
        delta_r, delta_c = self.target_vector
        target_r, target_c = r + delta_r, c + delta_c

        # return tile/None from loc
        return self.board[target_r, target_c]


class ProxyTile(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action(self, t_loc):
        pass


class PushTile(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action(self, target_tile):

        """
        Push tile one space away
        """

        # shift tiles
        delta = self.angle.values[2]
        self.board.shift_tiles(target_tile, delta)
