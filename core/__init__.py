import logging
import random

from core.board import Board
from core.tiles import Tile, PushTile, TileAngle
from core.game import Player

logging.getLogger().setLevel(logging.INFO)

# DEBUG ###############################################
p1 = Player("p1")
p2 = Player("p2")

b = Board()

b.place_tile(PushTile(player=p1, angle=TileAngle.S), (0, 2))
b.place_tile(PushTile(player=p1, angle=TileAngle.E), (1, 0))
b.place_tile(PushTile(player=p2, angle=TileAngle.NW), (1, 1))
b.place_tile(PushTile(player=p2, angle=TileAngle.W), (1, 2))
b.place_tile(PushTile(player=p1, angle=TileAngle.SE), (2, 1))

print(b)

# get tile by loc
t = b[1, 0]


def random_board(n=5):
    b2 = Board(width=n, height=n)

    locs = []
    for x in range(n):
        if x % 2 == 0:
            p = p1
        else:
            p = p2
        loc = random.randint(0, n - 1), random.randint(0, n - 1)
        if loc in locs:
            continue
        tile = PushTile(player=p, angle=list(TileAngle)[random.randint(0, 7)])
        b2.place_tile(tile, loc)
    print(b2)
    return b2
