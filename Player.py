import MineSweeper as MineSweep
import MapGeneration as MapGen
import sys

x = 2500
# max size is x/x
# 2500 means max grid size is 50 by 50
sys.setrecursionlimit(x)


def play(grid):
    mines_detonated = 0
    while MineSweep.win_condition(grid) == False:
        MapGen.gridPrint(grid)
        coordinates = MineSweep.pick_coord(grid)
        mines_detonated += MineSweep.reveal_coord(grid, coordinates)
    MapGen.reveal_all(grid)
    MapGen.gridPrint(grid)
    print("\nyou blew up ", mines_detonated, " mines. Lets play again")


mines = 4
gridlen = 5
grid = MapGen.makeMap(gridlen, mines)
gridlen = len(grid)
play(grid)
