import MineSweeper as MineSweep
import MapGeneration as MapGen
import random
import sys


x = 2500
# max grid size is x/x
# 2500 means max grid size is 50 by 50
# this is needed because of the special 0 rule is implemented with recursion
sys.setrecursionlimit(x)


class Equation:
    def __init__(self, loc_set, mines_left):
        self.loc_set = loc_set
        self.mines_left = mines_left

    def __eq__(self, other):
        condition1 = other.loc_set.symmetric_difference(self.loc_set) == set()
        condition2 = other.mines_left == self.mines_left
        return condition1 and condition2


def database_print(database):
    print("database: [", end="")
    for x in database:
        print(x.loc_set, f" = {x.mines_left}", end="; ")
    print("]")


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


# try and make a smart guess bases on highest possibility
def smart_random_move(grid, clues_to_check):
    best_probability = 0
    best_coords = set()
    all_prob_coords = set()
    for c in clues_to_check:
        neighbors = MapGen.get_neighbors(grid, (c[0], c[1]))
        unrevealed = set()
        num_bombs = 0
        # count unrevealed and mines
        for n in neighbors:
            if n.revealed == "no":
                unrevealed.add(n.coordinates)
                all_prob_coords.add(n.coordinates)
            elif n.revealed == "flag" or n.status == "mine":
                num_bombs += 1
        # prob one of the unrevealed is not a mine
        bombs_left = grid[c[0]][c[1]].status - num_bombs
        prob = (len(unrevealed) - bombs_left) / len(unrevealed)

        # only store the best prob
        if prob > best_probability:
            best_probability = prob
            best_coords = unrevealed
    # if the best probability is too low pick unknown area
    if best_probability >= 2 / 3:
        return random.choice(tuple(best_coords)), best_probability

    # get all unrevealed coords and subtract all too low prob coords from before
    total_unrevealed_coords = set()
    gridlen = len(grid)
    for x in range(gridlen):
        for y in range(gridlen):
            if grid[x][y].revealed == "no":
                total_unrevealed_coords.add(grid[x][y].coordinates)
    remainder = total_unrevealed_coords - all_prob_coords

    # if there are any remainders use them
    if len(remainder) != 0:
        return random.choice(tuple(remainder)), "<2/3"
    # else use the best prob from before
    return random.choice(tuple(best_coords)), best_probability


# returns list of coordinates that still have un-flagged and unrevealed neighbors
def dumb_needed_clues(grid):
    clues_to_check = set()
    gridlen = len(grid)
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


# performs the same function as dumb_needed_clues, but also adds equations to database
# for each clue_to_check coordinate
def smart_needed_clues(grid, database):
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

                if len(eq_locs) != 0:  # there are hidden neighbors
                    clues_to_check.add((x, y))

                    # update database with new eq
                    temp = Equation(eq_locs, grid[x][y].status - flags_mines)
                    if not in_database(temp, database):
                        database.append(temp)
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


# update database equations when flag or safe space is identified
def database_update(space, database, mode="safe"):
    i = 0
    l = len(database)
    while i < l:
        if space in database[i].loc_set:
            # if flag square is the only tuple in equation
            if len(database[i].loc_set) == 1:
                database.remove(database[i])
                i -= 1
                l -= 1
            # else remove square tuple from eqs & subtract 1 from mines total
            else:
                new_eq = Equation(database[i].loc_set.copy(), database[i].mines_left)
                if mode == "flag":
                    new_eq.mines_left -= 1
                new_eq.loc_set.remove(space)

                if not in_database(new_eq, database):
                    database[i].loc_set.remove(space)
                    if mode == "flag":
                        database[i].mines_left -= 1
                # unless new eq already exists in database, in that case just delete
                else:
                    database.remove(database[i])
                    i -= 1
                    l -= 1
        i += 1


# checks for locations in database that have been auto-revealed and updates appropriately
def catch_auto_reveals(grid, database):
    new_reveals = set()
    for eq in database:
        for square in eq.loc_set:
            x = square[0]
            y = square[1]
            if grid[x][y].revealed == "yes" and grid[x][y].status != "mine":
                new_reveals.add(square)
    for square in new_reveals:
        database_update(square, database, "safe")


# Recognize clear & mine spots via equation subtraction (look for eqs that are subsets of other eqs)
# returns solvable (safe/mine) values from database equations
def infer(database):
    safe_coords = set()
    mine_coords = set()
    # This outer loop will still hit eqs added to database
    for eq1 in database:
        # Look if database[i] is subset of other database eqs
        generator = (eq2 for eq2 in database if eq2 != eq1)
        for eq2 in generator:
            if eq1.loc_set.issubset(eq2.loc_set):
                tentative_eq = Equation(
                    eq2.loc_set - eq1.loc_set, eq2.mines_left - eq1.mines_left
                )

                if not in_database(tentative_eq, database):
                    # if tentative equation is a conclusion (a square is a mine/clear)
                    if len(tentative_eq.loc_set) == 1:
                        if tentative_eq.mines_left == 0:
                            safe_coords = safe_coords | tentative_eq.loc_set
                        elif tentative_eq.mines_left == 1:
                            mine_coords = mine_coords | tentative_eq.loc_set

                    # all squares in equation are clear
                    elif tentative_eq.mines_left == 0:
                        safe_coords = safe_coords | tentative_eq.loc_set

                    # no explicit conclusion, add new equation to database
                    else:
                        database.append(tentative_eq)

    return safe_coords, mine_coords


# Base AI algorithm specified by Dr. Cowan's instructions
def dumbAI(grid):

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
        unchecked = dumb_needed_clues(grid)
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


# general AI procedure: check for obvious flags and safe spaces, infer using database, then guess
def smartAI(grid):

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
        # list (clue) squares with hidden neighbors
        unchecked = smart_needed_clues(grid, database)
        print("\nunchecked", unchecked)  #!rem

        # if set to flag and click are empty tryand fill them
        if len(flag_these) == 0 and len(safe_spaces) == 0:
            flag_these = bomb_coord_set(grid, unchecked)
            safe_spaces = safe_coord_set(grid, unchecked)

            catch_auto_reveals(grid, database)
            inferred_safes, inferred_flags = infer(database)
            safe_spaces = safe_spaces | inferred_safes
            flag_these = flag_these | inferred_flags
            print("\ninferred flags", inferred_flags)  #!rem
            print("inferred safes", inferred_safes)  #!rem
        print("\nflags", flag_these)  #!rem
        print("safes", safe_spaces)  #!rem

        # time to make a move
        # if you can flag spend the move to flag
        if len(flag_these) != 0:
            print("flag move")  #!rem
            flag_coords = flag_these.pop()
            grid[flag_coords[0]][flag_coords[1]].revealed = "flag"
            database_update(flag_coords, database, "flag")
        # if there is a safe space then click it
        elif len(safe_spaces) != 0:
            print("safe move")  #!rem
            safe_coords = safe_spaces.pop()
            # for case when a safe coord is a zero and that zero reveals a coord in safe coords
            if grid[safe_coords[0]][safe_coords[1]].revealed == "no":
                mines_detonated += MineSweep.reveal_coord(grid, safe_coords)
            database_update(safe_coords, database, "safe")
        # if you have no useful info do a random move
        else:
            print("\n\nsmart random move")  #!rem
            random_coords, prob = smart_random_move(grid, unchecked)
            print(random_coords[0] + 1, random_coords[1] + 1, prob)  #! rem
            mines_detonated += MineSweep.reveal_coord(grid, random_coords)

    MapGen.reveal_all(grid)
    MapGen.gridPrint(grid)
    print("\nyou blew up ", mines_detonated, " mines. Lets play again")


mines = 4
gridlen = 5
grid = MapGen.makeMap(gridlen, mines)
gridlen = len(grid)
smartAI(grid)
