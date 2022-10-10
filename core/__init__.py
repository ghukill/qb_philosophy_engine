import logging

from core.board import Board
from core.tiles import Tile, PushTile, TileAngle
from core.game import Player

logging.getLogger().setLevel(logging.INFO)

# DEBUG ###############################################
p1 = Player("p1")
p2 = Player("p2")

b = Board()

b.place_tile(PushTile(player=p1, angle=TileAngle.S), (2, 0))
b.place_tile(PushTile(player=p2, angle=TileAngle.NW), (1, 1))
b.place_tile(PushTile(player=p1, angle=TileAngle.E), (0, 1))
b.place_tile(PushTile(player=p1, angle=TileAngle.SE), (2, 2))

print(b)

# get tile by loc
t = b[1, 0]

# get tile by loc, pass to loc by id, putting that loc back to board.... what is this relationship style?
t = b[b.loc(b[1, 0].id)]
print(t)
