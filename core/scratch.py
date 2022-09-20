"""
Scratch
"""

from enum import Enum

from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace, compare as rdflib_compare

QB_NS = Namespace("http://qualitybeast.com/ld/")


class QBItem(Enum):
    board = QB_NS.board
    board_square = QB_NS.board_square
    tile = QB_NS.tile
    on_square = QB_NS.on_square


class QBBoard(Enum):
    row = QB_NS.row
    column = QB_NS.column
    dir_n = QB_NS.dir_n
    dir_ne = QB_NS.dir_ne
    dir_e = QB_NS.dir_e
    dir_se = QB_NS.dir_se
    dir_s = QB_NS.dir_s
    dir_sw = QB_NS.dir_sw
    dir_w = QB_NS.dir_w
    dir_nw = QB_NS.dir_nw


def init_graph():
    g = Graph()
    g.bind(prefix="QB", namespace=QB_NS)
    return g


def init_game_board(g, size=3):

    # build board node
    b1 = Literal("b1")
    g.add((b1, RDFS.label, Literal(f"Board: {b1}")))
    g.add((b1, RDF.type, QBItem.board.value))

    squares = []
    for x in range(size):
        for y in range(size):

            # create square node
            s = Literal(f"s{(x * size) + y}")
            squares.append(s)
            g.add((s, RDF.type, QBItem.board_square.value))
            g.add((s, RDFS.label, Literal(f"Board Square: {s}")))

            # add columns and rows
            g.add((s, QBBoard.row.value, Literal(x)))
            g.add((s, QBBoard.column.value, Literal(y)))

            # add directional pointers
            target_squares = {
                QBBoard.dir_n.value: ((x * size) + (y + 1)),
                QBBoard.dir_ne.value: (((x + 1) * size) + (y + 1)),
                QBBoard.dir_e.value: (((x + 1) * size) + y),
                QBBoard.dir_se.value: (((x + 1) * size) + (y - 1)),
                QBBoard.dir_s.value: ((x * size) + (y - 1)),
                QBBoard.dir_sw.value: (((x - 1) * size) + (y - 1)),
                QBBoard.dir_w.value: (((x - 1) * size) + y),
                QBBoard.dir_nw.value: (((x - 1) * size) + (y + 1)),
            }
            for k, v in target_squares.items():
                if v >= 0 and v < size**2:
                    g.add((s, k, Literal(f"s{v}")))


def get_square(g, row, column):

    q = """
        PREFIX 
            qb: <%(qb_ns)s>
        SELECT ?p ?r
        WHERE {
            ?p rdf:type qb:board_square .
            ?p qb:row %(row)d .
            ?p qb:column %(column)d .
        }
    """ % {
        "qb_ns": QB_NS,
        "row": row,
        "column": column,
    }
    print(q)
    for r in g.query(q):
        print(r)


board_graph = init_graph()
init_game_board(board_graph)

# turn 1
turn1_graph = init_graph()
t0 = Literal("t0")
turn1_graph.add((t0, RDF.type, QBItem.tile.value))
turn1_graph.add((t0, RDFS.label, Literal(f"Tile: {t0}")))
turn1_graph.add((t0, QBItem.on_square.value, Literal("s4")))

turn2_graph = init_graph()
t0 = Literal("t0")
turn2_graph.add((t0, RDF.type, QBItem.tile.value))
turn2_graph.add((t0, RDFS.label, Literal(f"Tile: {t0}")))
turn2_graph.add((t0, QBItem.on_square.value, Literal("s1")))


def get_tile_coords(tile):
    q = """
        PREFIX 
            qb: <%(qb_ns)s>
        SELECT ?square_row ?square_column
        WHERE {
            "%(tile)s" qb:on_square ?s .
            ?s qb:row ?square_row .
            ?s qb:row ?square_column .        
        }
    """ % {
        "qb_ns": QB_NS,
        "tile": tile,
    }
    tcoords = list((board_graph + turn1_graph).query(q))[0]
    return tcoords[0].value, tcoords[1].value


b, f, s = rdflib_compare.graph_diff(turn1_graph, turn2_graph)
turn3_graph = board_graph + b + s
