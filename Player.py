import MineSweeper as MineSweep
import MapGeneration as MapGen


def play(grid):
    mines_detonated = 0
    while MineSweep.win_condition(grid) == False:
        MapGen.gridPrint(grid)
        coordinates = MineSweep.pick_coord(grid)
        mines_detonated += MineSweep.reveal_coord(grid, coordinates)
    MapGen.reveal_all(grid)
    MapGen.gridPrint(grid)
    print("\nyou blew up ", mines_detonated, " mines. Lets play again")


# errors, not finnishing game and not doing specail 0 rule
mines = 2
gridlen = 5
grid = MapGen.makeMap(gridlen, mines)
gridlen = len(grid)
play(grid)
