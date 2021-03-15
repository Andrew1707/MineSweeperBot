import MineSweeper as MineSweep
import MapGeneration as MapGen
import random


class Equation:
    def __init__(self, loc_set, mines_left):
        self.loc_set = loc_set
        self.mines_left = mines_left

    def __eq__(self, other):
        condition1 = (other.loc_set.symmetric_difference(self.loc_set) == set())
        condition2 = other.mines_left == self.mines_left
        return condition1 and condition2


def database_print(database):
    print('database: [', end='')
    for x in database:
        print(x.loc_set, f' = {x.mines_left}', end='; ')
    print(']')


# checks if an equation object is in database
def in_database(eq, database):
    for x in database:
        if eq == x:
            return True
    return False


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
def needed_clues(grid, database):
    clues_to_check = set()
    for x in range(gridlen):
        for y in range(gridlen):
            # if revealed and not a mine
            if grid[x][y].revealed == "yes" and grid[x][y].status != "mine":
                neighbors = MapGen.get_neighbors(grid, (x, y))
                
                # count surrounding mines & unrevealed squares
                eq_locs = set()
                flags_mines = 0
                for n in neighbors:
                    if n.revealed == "no":
                        eq_locs.add(n.coordinates)
                    elif n.revealed == "flag" or n.status == "mine":
                        flags_mines += 1

                if len(eq_locs) != 0: # there are hidden neighbors 
                    clues_to_check.add((x, y))
                    
                    # update database with new eq
                    temp = Equation(eq_locs, grid[x][y].status - flags_mines)
                    if not in_database(temp, database):
                        database.append(temp)
    return clues_to_check

# if square has number equal to number of unrevealed they are all bombs and return bomb coords
def bomb_coord_set(grid, clues_to_check, database):
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

    # update database equations
    for f in flag_these:
        i = 0
        l = len(database)
        while i < l:
            if f in database[i].loc_set:
                # if flag square is the only tuple in equation
                if len(database[i].loc_set) == 1:
                    database.remove(database[i])
                    i -= 1
                    l -= 1
                # else remove square tuple from eqs & subtract 1 from mines total
                else:
                    new_eq = Equation(database[i].loc_set.copy(), database[i].mines_left - 1)
                    new_eq.loc_set.remove(f)
                    if not in_database(new_eq, database):
                        database[i].loc_set.remove(f)
                        database[i].mines_left -= 1
                    # unless new eq already exists in database, in that case just delete
                    else:
                        database.remove(database[i])
                        i -= 1
                        l -= 1
            i += 1

    return flag_these


# if square has number equal to num flags/mines around it , the rest are safe and return safe coords
def safe_coord_set(grid, clues_to_check, database):
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

    # update database equations
    for s in safe_coords:
        i = 0
        l = len(database)
        while i < l:
            if s in database[i].loc_set:
                # if flag square is the only tuple in equation
                if len(database[i].loc_set) == 1:
                    database.remove(database[i])
                    i -= 1
                    l -= 1
                # else remove square tuple from eqs & subtract 1 from mines total
                else:
                    new_eq = Equation(database[i].loc_set.copy(), database[i].mines_left)
                    new_eq.loc_set.remove(s)
                    if not in_database(new_eq, database):
                        database[i].loc_set.remove(s)
                    # unless new eq already exists in database, in that case just delete
                    else:
                        database.remove(database[i])
                        i -= 1
                        l -= 1
            i += 1
                    
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
#! I don't think agent is supposed to have access to total # of bombs in grid :(
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


# returns solvable (safe/mine) values from database equations
def infer(grid, database):
    safe_coords = set()
    mine_coords = set()
    # 1. Set up equations related to clues_to_check (this is being implemented in other methods)
    # 2. Recognize clear & mine spots via equation subtraction (look for eqs that are subsets of other eqs)
    for d in database:
        # Look if d is subset of other database eqs
        generator = (e for e in database if e != d)
        for e in generator:
            1 #! This is filler, checking for subsets here -Benton
    # 3. Guess and check, see if mine/clear states are possible with curr knowledge


# function which is the brain of the AI
def AI(grid):

    mines_detonated = 0
    MapGen.gridPrint(grid)
    print()
    first_move = random_move(grid)
    mines_detonated += MineSweep.reveal_coord(grid, first_move)
    
    flag_these = set()
    safe_spaces = set()
    database = []

    while MineSweep.win_condition(grid) == False:
        MapGen.gridPrint(grid)
        # pick coord
        unchecked = needed_clues(grid, database)
        print("\nunchecked", unchecked)

        # if set to flag and click are empty tryand fill them
        if len(flag_these) == 0 and len(safe_spaces) == 0:
            flag_these = bomb_coord_set(grid, unchecked, database)
            safe_spaces = safe_coord_set(grid, unchecked, database)
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


mines = 2
gridlen = 5
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
