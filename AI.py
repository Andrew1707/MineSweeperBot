import MineSweeper as MineSweep
import MapGeneration as MapGen
import random

# when in doubt make any move but not on a flag
def random_move(grid):
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)
    # keep getting coords if they are bad or coords hit a flag

    while (grid[x][y].revealed != "no") or MapGen.isValid(grid, (x, y)) == False:
        x = random.randint(0, gridlen - 1)
        y = random.randint(0, gridlen - 1)
    return (x, y)


# returns list of coordinates that still have un-flagged and unrevealed neighbors
def needed_clues(grid):
    clues_to_check = set()
    gridlen = len(grid)  # benton work without this line ??????
    for x in range(gridlen):
        for y in range(gridlen):
            # if revealed and not a mine
            if grid[x][y].revealed == "yes" and grid[x][y].status != "mine":
                neighbors = MapGen.get_neighbors(grid, (x, y))
                for n in neighbors:
                    if n.revealed == "no":
                        clues_to_check.add((x, y))
                        break  # has unrevealed neighbor no need to check for more
    return clues_to_check


# if square has number equal to number of unrevealed they are all bombs and return bomb coords
def bomb_coord_set(grid, clues_to_check):
    flag_these = set()
    for c in clues_to_check:
        x = c[0]
        y = c[1]
        neighbors = MapGen.get_neighbors(grid, (x, y))
        unrevealed = 0
        actual_threats = 0
        potential_threats = set()
        # count number of unrevealed neighbors and bombs
        for n in neighbors:
            # if unrevealed its a possible threat so add them to counter

            if n.revealed == "no":
                potential_threats.add(n.coordinates)
                unrevealed += 1
            # subtract the already found threats
            elif n.revealed == "flag":
                actual_threats += 1
            elif n.status == "mine":
                actual_threats += 1
        # benton should this be greater than???
        # if all bombs found leave
        if actual_threats != grid[x][y].status:
            # if unrevealed bombs = clue - found bombs, then unrevealed are bombs and flag them
            if unrevealed == grid[x][y].status - actual_threats:
                flag_these = flag_these | potential_threats
    return flag_these


# if square has number equal to num flags/mines around it , the rest are safe and return safe coords
def safe_coord_set(grid, clues_to_check):
    safe_coords = set()
    for c in clues_to_check:
        x = c[0]
        y = c[1]
        neighbors = MapGen.get_neighbors(grid, (x, y))
        mines = 0
        # mine_coords = {}
        safe_neighbors = set()
        # if neighbor is a flag or revealed mine add it up
        for n in neighbors:
            if n.revealed == "flag":
                # mine_coords += n.coordinates
                mines += 1
            elif n.revealed == "yes" and n.status == "mine":
                # mine_coords += n.coordinates
                mines += 1
            elif n.revealed == "no":
                safe_neighbors.add(n.coordinates)
        if grid[x][y].status == mines:
            safe_coords = safe_coords | safe_neighbors
    return safe_coords


# send DEEP COPY of POSSIBLE grid configs and return if possible or not
def impossible(grid):
    gridlen = len(grid)
    for x in range(gridlen):
        for y in range(gridlen):
            neighbors = MapGen.get_neighbors(grid, (x, y))
            bomb_neighbors = 0
            if grid[x][y].revealed == "yes" and grid[x][y].status != "mine":
                for n in neighbors:
                    if n.revealed == "flag" or (
                        n.revealed == "yes" and n.status == "mine"
                    ):
                        bomb_neighbors += 1
                if grid[x][y].status != bomb_neighbors:
                    return False
    return True


# returns the number of bombs found so if you know total bombs you get remainder
def bombs_found(grid):
    gridlen = len(grid)
    bombs = 0
    for x in range(gridlen):
        for y in range(gridlen):
            if grid[x][y].revealed == "flag" or (
                grid[x][y].revealed == "yes" and grid[x][y].status == "mine"
            ):
                bombs += 1
    return bombs


# function which is the brain of the AI
def AI(grid):

    mines_detonated = 0
    MapGen.gridPrint(grid)
    print()
    first_move = random_move(grid)
    mines_detonated += MineSweep.reveal_coord(grid, first_move)
    flag_these = set()
    safe_spaces = set()
    while MineSweep.win_condition(grid) == False:
        MapGen.gridPrint(grid)
        # pick coord
        unchecked = needed_clues(grid)
        print("\nunchecked", unchecked)
        # if set to flag and click are empty tryand fill them
        if len(flag_these) == 0 and len(safe_spaces) == 0:
            flag_these = bomb_coord_set(grid, unchecked)
            safe_spaces = safe_coord_set(grid, unchecked)
        print("\nflags", flag_these)
        print("\nsafes", safe_spaces)
        # time to make a move
        # if you can flag spend the move to flag
        if len(flag_these) != 0:
            print("flag move")
            flag_coords = flag_these.pop()
            grid[flag_coords[0]][flag_coords[1]].revealed = "flag"
        # if there is a safe space then click it
        elif len(safe_spaces) != 0:
            print("safe move")
            safe_coords = safe_spaces.pop()
            if grid[safe_coords[0]][safe_coords[1]].revealed == "no":
                mines_detonated += MineSweep.reveal_coord(grid, safe_coords)
        # if you have no useful info do a random move
        else:
            print("\n\nrandom move")
            random_coords = random_move(grid)
            print(random_coords[0] + 1, random_coords[1] + 1)
            mines_detonated += MineSweep.reveal_coord(grid, random_coords)

    MapGen.reveal_all(grid)
    MapGen.gridPrint(grid)
    print("\nyou blew up ", mines_detonated, " mines. Lets play again")


mines = 20
gridlen = 10
grid = MapGen.makeMap(gridlen, mines)
gridlen = len(grid)
AI(grid)

# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 0 0 0
# 1 1 1 1 1
# ? ? ? ? ?
# in x legal states, if this coord is always a bomb or is always safe do something about it
# should know middle ? is safe
