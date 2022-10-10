"""

"""


import pandas as pd

from core.tiles import Tile


class Board:
    def __init__(self):

        self.width = 3
        self.height = 3
        self.matrix = pd.DataFrame([[None for y in range(self.height)] for x in range(self.width)])

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return str(self.matrix)

    def __getitem__(self, index):
        x, y = index
        return self.matrix[x][y]

    def __getitem__(self, key):
        return self.matrix.iloc[key]

    def place_tile(self, tile, x, y):
        self.matrix[x][y] = tile

    def get_tile(self, x, y):
        return self.matrix[x][y]
