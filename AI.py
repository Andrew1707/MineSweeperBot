import MineSweeper as MineSweep
import MapGeneration as MapGen
import random

# when in doubt make any move
def random_move(grid):
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)
    if MapGen.isValid(grid, (x, y)) == False:
        random_move(grid)
    return (x, y)


# returns list of coordinates that still have un-flagged and unrevealed neighbors
def needed_clues(grid):
    clues_to_check = {}
    for x in range(gridlen):
        for y in range(gridlen):
            # if revealed and not a mine
            if grid[x][y].revealed == "yes" and grid[x][y].status != "mine":
                neighbors = MapGen.get_neighbors(grid, (x, y))
                for n in neighbors:
                    if n.revealed == "no":
                        clues_to_check += n.coordinates
                        break  # has unrevealed neighbor no need to check for more
    return clues_to_check


# if square has number equal to number of unrevealed they are all bombs and return bomb coords
def clue_equal_bombs(grid, clues_to_check):
    flag_these = {}
    for c in clues_to_check:
        x = c[0]
        y = c[1]
        neighbors = MapGen.get_neighbors(grid, (x, y))
        unrevealed = 0
        potential_threats = {}
        # count number of unrevealed neighbors
        for n in neighbors:
            if n.revealed != "yes":
                potential_threats += n.coordinates
                unrevealed += 1
        if unrevealed == grid[x][y].status:
            flag_these += potential_threats

    return flag_these


# if square has number equal to num flags/mines around it , the rest are safe and return safe coords
def bombs_found(grid, clues_to_check):
    safe_coords = {}
    for c in clues_to_check:
        x = c[0]
        y = c[1]
        neighbors = MapGen.get_neighbors(grid, (x, y))
        mines = 0
        # mine_coords = {}
        safe_neighbors = {}
        # if neighbor is a flag or revealed mine add it up
        for n in neighbors:
            if n.revealed == "flag":
                # mine_coords += n.coordinates
                mines += 1
            elif n.revealed == "yes" and n.status == "mine":
                # mine_coords += n.coordinates
                mines += 1
            else:
                safe_neighbors += n.coordinates
        if grid.status == mines:
            safe_coords += safe_neighbors

    return safe_coords


def AI(grid):
    mines_detonated = 0

    MapGen.gridPrint(grid)
    first_move = random_move(grid)
    mines_detonated += MineSweep.reveal_coord(grid, first_move)

    while MineSweep.win_condition(grid) == False:
        MapGen.gridPrint(grid)
        coordinates = MineSweep.pick_coord(grid)
        mines_detonated += MineSweep.reveal_coord(grid, coordinates)
    MapGen.reveal_all(grid)
    MapGen.gridPrint(grid)
    print("\nyou blew up ", mines_detonated, " mines. Lets play again")


mines = 2
gridlen = 5
grid = MapGen.makeMap(gridlen, mines)
gridlen = len(grid)
AI(grid)
