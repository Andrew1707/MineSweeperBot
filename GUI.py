def GUI(grid):
    def toggle():
        """
        use
        t_btn.config('text')[-1]
        to get the present state of the toggle button
        """
        if flag_btn.config("text")[-1] == "On":
            flag_btn.config(text="Off")
        else:
            flag_btn.config(text="On")

    def clicked(x, y):
        if flag_btn.config("text")[-1] == "On":
            grid[x][y].revealed = "flag"
            b.config(text="🚩")
        else:
            grid[x][y].revealed = "yes"
            b.config(text=str(grid[x][y].status))

    top = tkinter.Tk()
    right = tkinter.Frame(top)
    right.pack(side="right")

    f = tkinter.Frame(right, width=30, height=30)
    flag_btn = tkinter.Button(f, text=str("Off"), width=12, command=toggle)
    f.rowconfigure(0, weight=1)
    f.columnconfigure(0, weight=1)
    f.grid_propagate(0)

    f.grid(row=len(grid) + 1, column=0)
    flag_btn.grid(sticky="NWSE")
    for i in range(len(grid)):
        for j in range(len(grid)):
            f = tkinter.Frame(right, width=30, height=30)
            if grid[i][j].revealed == "yes":
                if grid[i][j].status == "mine":
                    b = tkinter.Button(f, text=str("💣"), command=lambda: clicked(i, j))
                else:
                    b = tkinter.Button(
                        f, text=str(grid[i][j].status), command=lambda: clicked(i, j)
                    )
            elif grid[i][j].revealed == "no":
                b = tkinter.Button(
                    f, text=str(""), bg="green", command=lambda: clicked(i, j)
                )
            else:
                b = tkinter.Button(f, text=str("🚩"), command=lambda: clicked(i, j))

            f.rowconfigure(0, weight=1)
            f.columnconfigure(0, weight=1)
            f.grid_propagate(0)

            f.grid(row=i, column=j)
            b.grid(sticky="NWSE")

    top.mainloop()


grid = makeMap(10, 10)
gridPrint(grid)
GUI(grid)
grid = reveal_all(grid)
gridPrint(grid)
GUI(grid)