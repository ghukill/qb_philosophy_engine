"""

"""

import logging
from typing import Tuple, Union, Hashable

import pandas as pd

from core.exceptions import TileNotFound, TileLocOffBoard
from core.tiles import Tile, ProxyTile


class Board:
    def __init__(self):

        self.width = 3
        self.height = 3
        self.matrix = pd.DataFrame([[None for _row in range(self.height)] for _col in range(self.width)])

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return str(self.matrix)

    def __getitem__(self, loc: Tuple[int, int]):
        """
        return Tile by location
        """
        _tile = self.matrix.iloc[loc]
        if _tile is None:
            raise TileNotFound(f"tile not found at loc: {loc}")
        return _tile

    def place_tile(self, tile, loc):

        # add board tether to tile
        tile.board = self

        row, col = loc
        self.matrix[row][col] = tile

    def loc(self, tile) -> Tuple[Hashable, Hashable]:
        """
        return (row,col) of tile via id search
            - NOTE: this powers reflexive tile.loc()
        """
        if isinstance(tile, str):  # handle string id
            tile = ProxyTile(id=tile)
        for row_idx, row in self.matrix.iterrows():
            for col_idx, cell in row.items():
                if cell is not None and (cell.id == tile.id or cell.id.startswith(tile.id)):
                    return row_idx, col_idx
        raise TileNotFound(f"tile not found for id: '{tile.id}'")

    def move_tile(self, old_loc, new_loc):
        pass

    def perform_tile_actions(self, tile):

        """
        TODO: clone matrix for rollback
        TODO: move tiles (shift matrix) depending on tile.action()
        """

        # get target tile
        target_tile = tile.get_target_tile()

        # if no target, do nothing!
        if target_tile is None:
            return None

        logging.info(f"INTERACTION: {tile} --> {target_tile}")
