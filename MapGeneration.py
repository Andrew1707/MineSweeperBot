import random


class GridUnit:
    def __init__(self, status, revealed):
        self.status = status  # mine, number
        self.revealed = revealed  # yes, no, flag


# coordinates is a tuple (x,y) for easier to read code
class Node:
    def __init__(self, coordinates):
        self.coordinates = coordinates


# returns list of coordinates
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


def isValid(grid, coordinates):
    # is it out of bounds?
    gridlength = len(grid)
    if (
        coordinates[0] >= gridlength
        or coordinates[0] < 0
        or coordinates[1] >= gridlength
        or coordinates[1] < 0
    ):
        return False
    return True


def makeMap(gridlength, mines):
    if mines > gridlength * gridlength:
        print("Too many mines to fit in grid error")
        return None

    grid = [
        [GridUnit(None, "no") for j in range(gridlength)] for i in range(gridlength)
    ]

    while mines > 0:
        mines -= 1
        x = random.randint(0, len(grid) - 1)
        y = random.randint(0, len(grid) - 1)
        if grid[x][y].status == None:
            grid[x][y].status = "mine"
        else:
            mines += 1

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


# prints grid out of easy to read O (open) and X (closed) characters
def gridPrint(grid):
    gridlength = len(grid)
    for i in range(gridlength):
        print()
        for j in range(gridlength):
            if grid[i][j].revealed == "yes":
                if grid[i][j].status == "mine":
                    print("💣", end=" ")
                else:
                    emoji = str(grid[i][j].status) + "\uFE0F\u20E3"
                    print(emoji, end="  ")
            elif grid[i][j].revealed == "no":
                print("⬛", end=" ")
            else:
                print("🚩", end=" ")


def reveal_all(grid):
    gridlength = len(grid)
    for i in range(gridlength):
        for j in range(gridlength):
            grid[i][j].revealed = "yes"
    return grid
