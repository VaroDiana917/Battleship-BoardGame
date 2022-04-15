from dataclasses import dataclass
from random import choice, randint

from StartUp.Boardgame.cell import Cell
from StartUp.Functions.functionalities import surrounding_area, cleanup, get_letter_from_int


class Enemy_Board:
    def __init__(self, rows, columns):
        self.__rows = rows
        self.__columns = columns

        self.cells = self.__initialize_board_enemy()
        self.__ships = self.initialize_ships_randomly(self.cells)

    def __initialize_board_enemy(self):
        """
        :return: A 10x10 matrix of cells where the cell.ship and cell.checked are both False - meaning,
         there are no ships on the board and none of the cells have been checked yet
        """
        cells = []
        for row in range(0, self.__rows):
            values = []
            for column in range(0, self.__columns):
                values.append(Cell(row, column, False, False))
            cells.append(values)
        return cells


    def initialize_ships_randomly(self,board_cells):
        no_go_zone = []

        # Carrier - size 5
        def carrier():
            """
            Subprogram randomly places a size 5 ship on the board - 5 cells will have cell.ship become True.
            Subprogram will also remember those 5 cells along with all the surrounding cells as indexes in
            a no_go_zone list, meaning the following subprograms are not allowed to places ships on those indexes.
            """
            r_or_c_placement = choice(["row", "column"])
            start = randint(0, 5)
            if r_or_c_placement == "row":
                row = randint(0, 9)
                for i in range(start, start + 5):
                    board_cells[row][i].ship = True

                    no_go_zone.append([row, i])
                    for value in surrounding_area(row, i):
                        no_go_zone.append(value)

            elif r_or_c_placement == "column":
                column = randint(0, 9)
                for i in range(start, start + 5):
                    board_cells[i][column].ship = True
                    no_go_zone.append([i, column])
                    for value in surrounding_area(i, column):
                        no_go_zone.append(value)

        # Battleship - size 4
        def battleship():
            """
            Subprogram randomly places a size 4 ship on the board - 4 cells will have cell.ship become True.
            Subprogram will also remember those 4 cells along with all the surrounding cells as indexes in
            a no_go_zone list, meaning the following subprograms are not allowed to places ships on those indexes.
            """
            r_or_c_placement = choice(["row", "column"])
            start = randint(0, 6)
            if r_or_c_placement == "row":
                row = randint(0, 9)
                for i in range(start, start + 4):
                    for list in no_go_zone:
                        if [row, i] == list:
                            return battleship()

                for i in range(start, start + 4):
                    board_cells[row][i].ship = True

                    no_go_zone.append([row, i])
                    for value in surrounding_area(row, i):
                        no_go_zone.append(value)
                return True

            elif r_or_c_placement == "column":
                column = randint(0, 9)
                for i in range(start, start + 4):
                    for list in no_go_zone:
                        if [i, column] == list:
                            return battleship()

                for i in range(start, start + 4):
                    board_cells[i][column].ship = True

                    no_go_zone.append([i, column])
                    for value in surrounding_area(i, column):
                        no_go_zone.append(value)
                return True

        # Destroyer and submarine - size 3
        def destroyer_and_submarine():
            """
            Subprogram randomly places a size 3 ship on the board - 3 cells will have cell.ship become True.
            Subprogram will also remember those 3 cells along with all the surrounding cells as indexes in
            a no_go_zone list, meaning the following subprograms are not allowed to places ships on those indexes
            """
            r_or_c_placement = choice(["row", "column"])
            start = randint(0, 7)
            if r_or_c_placement == "row":
                row = randint(0, 9)
                for i in range(start, start + 3):
                    for list in no_go_zone:
                        if [row, i] == list:
                            return destroyer_and_submarine()

                for i in range(start, start + 3):
                    board_cells[row][i].ship = True

                    no_go_zone.append([row, i])
                    for value in surrounding_area(row, i):
                        no_go_zone.append(value)
                return True

            elif r_or_c_placement == "column":
                column = randint(0, 9)
                for i in range(start, start + 3):
                    for list in no_go_zone:
                        if [i, column] == list:
                            return destroyer_and_submarine()

                for i in range(start, start + 3):
                    board_cells[i][column].ship = True

                    no_go_zone.append([i, column])
                    for value in surrounding_area(i, column):
                        no_go_zone.append(value)
                return True

        # Patrol Boat - size 2
        def patrol_boat():
            """
            Subprogram randomly places a size 2 ship on the board - 2 cells will have cell.ship become True.
            """
            r_or_c_placement = choice(["row", "column"])
            start = randint(0, 8)
            if r_or_c_placement == "row":
                row = randint(0, 9)
                for i in range(start, start + 2):
                    for list in no_go_zone:
                        if [row, i] == list:
                            return patrol_boat()

                for i in range(start, start + 2):
                    board_cells[row][i].ship = True
                    #
                    # no_go_zone.append([row, i])
                    # for value in surrounding_area(row, i):
                    #     no_go_zone.append(value)
                return True

            elif r_or_c_placement == "column":
                column = randint(0, 9)
                for i in range(start, start + 2):
                    for list in no_go_zone:
                        if [i, column] == list:
                            return patrol_boat()

                for i in range(start, start + 2):
                    board_cells[i][column].ship = True
                    #
                    # no_go_zone.append([i, column])
                    # for value in surrounding_area(i, column):
                    #     no_go_zone.append(value)
                return True

        carrier()
        no_go_zone = cleanup(no_go_zone)

        battleship()
        no_go_zone = cleanup(no_go_zone)

        for i in range(0, 2): destroyer_and_submarine()
        no_go_zone = cleanup(no_go_zone)

        patrol_boat()
        no_go_zone = cleanup(no_go_zone)


    def get_cell(self, row, column):
        return self.cells[row][column]

    def __str__(self):
        board = "\nEnemy's board:\n"
        board += "  "
        row_numbers=[" ⓿ ", " ❶ ", " ❷ ", " ❸ ", " ❹ ", " ❺ ", " ❻ ", " ❼ ", " ❽ ", " ❾ "]
        for row in range(0, self.__rows):
            # board += " " + str(row) + " "
            board+=row_numbers[row]
        board += "\n"
        board += "  "
        for row in range(0, self.__rows * 2):
            board += "―"
        board += "\n"
        j = 0

        for row in range(0, self.__rows):
            board += get_letter_from_int(j) + "│"
            for column in range(0, self.__columns):
                cell = self.cells[row][column]
                if cell.checked == True:
                    if cell.ship==True:
                        board += " ■ "
                    else:
                        board += " ✕ "
                # elif cell.ship == True:
                #     board += " ❎ "
                else:
                    board += " ◦ "

                # if cell.checked == True:
                #     if cell.ship == True:
                #         board += " █ "
                #     else:
                #         board += " X "
                # # elif cell.ship == True:
                # #     board += " / "
                # else:
                #     board += " • "

            board += "\n"
            j = j + 1
        return board



