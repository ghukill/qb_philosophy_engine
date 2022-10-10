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


class TileAngle(MultiValueEnum):
    N = 0, "↑"
    NE = 45, "↗"
    E = 90, "→"
    SE = 135, "↘"
    S = 180, "↓"
    SW = 225, "↙"
    W = 270, "←"
    NW = 315, "↖"


class Tile(abc.ABC):
    def __init__(
        self,
        *,
        player: Player = None,
        angle: Union[TileAngle, int] = None,
        tile_uuid: uuid.UUID = str(uuid.uuid4()),
    ):
        self.tile_uuid = tile_uuid
        self.player = player
        if isinstance(angle, int):
            self.angle = TileAngle(angle)
        else:
            self.angle = angle

    def __repr__(self):
        return f"<{self.__class__.__name__}:({self.player},{self.angle.name}{self.angle.values[1]})>"

    @abc.abstractmethod
    def action(self):
        pass


class PushTile(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action(self, target_tile):
        pass
