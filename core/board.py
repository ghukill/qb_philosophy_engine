"""

"""

import logging
from typing import Tuple, Union, Hashable

import pandas as pd

from core.exceptions import TileNotFound, TileLocOffBoard
from core.tiles import Tile, ProxyTile


class Board:
    def __init__(self, width=3, height=3):

        self.width = width
        self.height = height
        self.matrix = pd.DataFrame([[None for _row in range(self.height)] for _col in range(self.width)])

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return str(self.matrix)

    def __getitem__(self, loc: Tuple[int, int]):
        r, c = loc
        if r < 0 or r >= self.width or c < 0 or c >= self.height:  # TODO: refactor
            raise TileLocOffBoard(f"loc off board: {(r, c)}")
        return self.matrix.iloc[loc]

    def __setitem__(self, loc, value):
        r, c = loc
        if r < 0 or r >= self.width or c < 0 or c >= self.height:  # TODO: refactor
            raise TileLocOffBoard(f"loc off board: {(r, c)}")
        self.matrix.iloc[loc] = value

    @property
    def tiles(self):
        for r_idx, r in self.matrix.iterrows():
            for c_idx, cell in r.items():
                if isinstance(cell, Tile):
                    yield cell

    def place_tile(self, tile, loc):
        tile.board = self
        r, c = loc
        self[r, c] = tile

    def remove_tile(self, tile: Tile):
        r, c = tile.loc
        tile.board = None
        tile.player.tiles_in_hand.add(tile)
        self[r, c] = None

    def loc(self, tile) -> Tuple[Hashable, Hashable]:
        """
        return (row,col) of tile via id search
        - NOTE: this powers reflexive tile.loc()
        """
        if isinstance(tile, str):  # handle string id
            tile = ProxyTile(id=tile)
        for r_idx, r in self.matrix.iterrows():
            for c_idx, cell in r.items():
                if cell is not None and (cell.id == tile.id or cell.id.startswith(tile.id)):
                    return r_idx, c_idx
        raise TileNotFound(f"tile not found for id: '{tile.id}'")

    def move_tile(self, tile, new_loc):

        # copy old loc
        old_r, old_c = tile.loc

        # check if tile in new loc (allow move onto self)
        new_r, new_c = new_loc
        if isinstance(self[new_r, new_c], Tile) and self[new_r, new_c] != tile:
            raise Exception(f"cannot move tile here, tile {self[new_r, new_c]} here already")

        # handle tile moving off board
        if new_r < 0 or new_r >= self.width or new_c < 0 or new_c >= self.height:  # TODO: refactor
            logging.info(f"move puts tile off board, removing tile: {tile}")
            self.remove_tile(tile)
            return

        # move tile
        self[new_r, new_c] = tile
        self[old_r, old_c] = None
        return

    def shift_tiles(self, tile: Tile, delta: Tuple[int, int]):

        """
        Shift tiles
        """

        logging.info(f"SHIFTING TILE: {tile} via {delta}")

        r, c = tile.loc
        nr, nc = r + delta[0], c + delta[1]
        # check target and recurse if necessary
        try:
            _tile = self[nr, nc]
            if isinstance(_tile, Tile):
                self.shift_tiles(_tile, delta)
        except TileLocOffBoard:
            logging.info("shift moves tile off board, removing...")
            self.remove_tile(tile)
            return

        # move tile
        self.move_tile(tile, (nr, nc))

    def perform_tile_actions(self, tile):

        """
        TODO: clone matrix for rollback
        TODO: move tiles (shift matrix) depending on tile.action()
        """

        # get target tile
        target_tile = tile.get_target_tile()

        # if no target, do nothing
        if target_tile is None:
            return None

        logging.info(f"INTERACTION: {tile} --> {target_tile}")

        # perform action
        tile.action(target_tile)
