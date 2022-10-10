from core.board import Board
from core.tiles import Tile, PushTile, TileAngle
from core.game import Player

# DEBUG ###############################################
p1 = Player("p1")
p2 = Player("p2")

b = Board()

b.place_tile(PushTile(player=p1, angle=TileAngle.S), 2, 0)
b.place_tile(PushTile(player=p2, angle=TileAngle.N), 1, 1)
b.place_tile(PushTile(player=p1, angle=TileAngle.E), 0, 1)
