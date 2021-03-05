import MapGeneration as MapGen

# go i need to return grid or no
# benton need to code for case of flag
def reveal_coord(grid, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    # if coord already revealed or out of bounds try again (needed for 0 rule)
    if MapGen.isValid(grid, coordinates) == False:
        return None
    # show whats square value is
    grid[x][y].revealed = "yes"
    # if square was a mine add 1 to bomb count
    if grid[x][y].status == "mine":
        print("you blew up, keep trying")
        return 1
    # if square was 0 reveal all neighbors
    if grid[x][y].status == 0:
        neighbors = MapGen.get_neighbors(grid, coordinates)
        for i in neighbors:
            if grid[i.coordinates[0]][i.coordinates[1]].revealed != "yes":
                reveal_coord(grid, i.coordinates)
    return 0


def pick_coord(grid):
    gridlength = len(grid)
    try:
        x, y = input("\nCan I take your coords sir? In the form 'x y': ").split()
        coordinates = (int(x) - 1, int(y) - 1)
        while MapGen.isValid(grid, coordinates) == False:
            if int(x) >= gridlength or int(x) < 0 or int(y) >= gridlength or int(y) < 0:
                x, y = input(
                    "out of bounds: \nbounds are: "
                    + str(gridlength)
                    + " by "
                    + str(gridlength)
                    + " try again: "
                ).split()
            else:
                x, y = input("already revealed, try another coordinate: ").split()
            coordinates = (int(x) - 1, int(y) - 1)
    except ValueError:
        print("please use the format of 'x y'")
        return pick_coord(grid)

    return coordinates


# returns false if the game is not solved and true if it is
def win_condition(grid):
    gridlen = len(grid)
    for i in range(gridlen):
        for j in range(gridlen):
            # if a number and not revealed
            if grid[i][j].status != "mine" and grid[i][j].revealed != "yes":
                return False
    return True
