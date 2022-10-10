"""

"""

from typing import Tuple

import pandas as pd

from core.tiles import Tile


class Board:
    def __init__(self):

        self.width = 3
        self.height = 3
        self.matrix = pd.DataFrame([[None for _row in range(self.height)] for _col in range(self.width)])

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return str(self.matrix)

    def __getitem__(self, index):
        row, col = index
        return self.matrix[row][col]

    def __getitem__(self, key) -> Tile:
        return self.matrix.iloc[key]

    def place_tile(self, tile, loc):
        row, col = loc
        self.matrix[row][col] = tile

    def get_tile(self, loc):
        row, col = loc
        return self.matrix[row][col]

    def tile_get_target(self, loc):
        row, col = loc

        # get tile
        t: Tile = self[row][col]

        # if None, exit
        if t is None:
            raise Exception("tile not found")  # TODO: use explicit exception

        d_row, d_col = t.target_vector
        t_row, t_col = row + d_row, col + d_col
        if t_row < 0 or t_col < 0:
            return Exception("target tile is off board")  # TODO: use explicit exception
        target = self[t_row][t_col]

        return target, (t_row, t_col)

    def do_tile_actions(self, row, col):

        # get tile and target
        target = self.tile_get_target(row, col)
