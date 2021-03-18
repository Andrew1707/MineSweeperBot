import random


class GridUnit:
    def __init__(self, status, revealed, coordinates):
        self.status = status  # mine, number
        self.revealed = revealed  # yes, no, flag
        self.coordinates = coordinates  # tuples (x,y)


# makes sure the coordinate is within the grid
def isValid(grid, coordinates):
    # is it out of bounds?
    x = coordinates[0]
    y = coordinates[1]
    gridlength = len(grid)
    if x >= gridlength or x < 0 or y >= gridlength or y < 0:
        return False
    # has it already been revealed
    # if grid[x][y].revealed == "yes":
    #     return False
    return True


# returns list of neighbors that surround corrdinate
def get_neighbors(grid, coordinates):
    neighbors = []
    x = coordinates[0]
    y = coordinates[1]
    i = x - 1
    j = y - 1
    while i <= x + 1:
        while j <= y + 1:

            if isValid(grid, (i, j)) and not (i == x and j == y):
                neighbors.append(grid[i][j])
            j += 1
        j = y - 1
        i += 1
    return neighbors


# makes and returns a grid for minesweeper
def makeMap(gridlength, mines):
    # makes sure you can fit all the bombs in grid
    if mines > gridlength * gridlength:
        print("Too many mines to fit in grid error")
        return None

    grid = [
        [GridUnit(None, "no", (i, j)) for j in range(gridlength)]
        for i in range(gridlength)
    ]

    # adds mines in random locations and does not overlap
    while mines > 0:
        mines -= 1
        x = random.randint(0, len(grid) - 1)
        y = random.randint(0, len(grid) - 1)
        if grid[x][y].status == None:
            grid[x][y].status = "mine"
        else:
            mines += 1

    # adds number values to each non mine to represent clues
    for i in range(gridlength):
        for j in range(gridlength):
            if grid[i][j].status != "mine":
                neighbors = get_neighbors(grid, (i, j))
                closeMines = 0
                for k in neighbors:
                    if k.status == "mine":
                        closeMines += 1
                grid[i][j].status = closeMines
    return grid


# prints grid out of easy to read emojis
def gridPrint(grid):
    gridlength = len(grid)
    for i in range(gridlength):
        print()
        for j in range(gridlength):
            if grid[i][j].revealed == "yes":
                if grid[i][j].status == "mine":
                    print("💣", end=" ")
                else:
                    if grid[i][j].status == 0:
                        print("🟦", end=" ")
                    # turn clue number into emoji using unicode
                    else:
                        emoji = str(grid[i][j].status) + "\uFE0F\u20E3"
                        print(emoji, end="  ")
            elif grid[i][j].revealed == "no":
                print("⬛", end=" ")
            else:
                print("🚩", end=" ")


# shows status of all units
def reveal_all(grid):
    gridlength = len(grid)
    for i in range(gridlength):
        for j in range(gridlength):
            grid[i][j].revealed = "yes"
    return grid
