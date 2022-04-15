from StartUp.Boardgame.board import Enemy_Board
from StartUp.Boardgame.cell import Cell
from StartUp.Functions.functionalities import get_int_from_letter, surrounding_area, cleanup, get_letter_from_int


class Player_Board:
    def __init__(self, rows, columns):
        self.__rows = rows
        self.__columns = columns

        self.__cells = self.__initialize_player_board()
        self.choice_for_ships()

    def choice_for_ships(self):
        """
        Player has the choice to place the ships themselves or have the program place them randomly on the map
        """

        choice = input("\nIt's your turn to place your ships on the board!\n"
                       "You can choose for your ships to be randomly placed\n"
                       "What will your choice be?\n\n"
                       "1. I want them randomized!\n"
                       "2. I want to place them myself!\n"
                       "Your choice: ")
        try:
            if int(choice) == 1:
                self.__ships = Enemy_Board.initialize_ships_randomly(self, self.__cells)
                print(self.__str__())
            elif int(choice) == 2:
                print(self.__str__())
                self.__ships = self.__initialize_ships()
            else:
                raise TypeError("Please insert a number between 1 or 2")
            return True
        except Exception as ex:
            print(f"Please insert a valid command: {ex}")
            return self.choice_for_ships()

    def __initialize_player_board(self):
        cells = []
        for row in range(0, self.__rows):
            values = []
            for column in range(0, self.__columns):
                values.append(Cell(row, column, False, False))
            cells.append(values)

        return cells

    def __initialize_ships(self):

        print("\nInput method is '<int><letter>-<int><letter>' (For example: 4B-4F)")

        no_go_zone = []

        def input_string(string):
            if string.find("-") == -1:
                raise TypeError("Please insert a valid command! (For example: 4B-4F)")
            else:
                start, finnish = string.split("-")

                number, letter = list(start)
                row1 = get_int_from_letter(letter)
                column1 = int(number)

                number, letter = list(finnish)
                row2 = get_int_from_letter(letter)
                column2 = int(number)
                if column1 < 0 or column1 > 9:
                    raise TypeError("Please insert a valid command! (For example: 4B-4F)")

                if column2 < 0 or column2 > 9:
                    raise TypeError("Please insert a valid command! (For example: 4B-4F)")
            return row1, column1, row2, column2

        def carrier():
            string = input("Where will your Carrier ship be? (Size of 5 squares):\n")
            try:
                row1, column1, row2, column2 = input_string(string)
            except TypeError as te:
                print(te)
                return carrier()

            if row1 == row2:
                if column2 - column1 + 1 != 5:
                    print("Please insert a valid command! (For example: 4B-4F)")
                    return carrier()
                else:
                    for i in range(column1, column2 + 1):
                        self.__cells[row1][i].ship = True
                        no_go_zone.append([row1, i])
                        for value in surrounding_area(row1, i):
                            no_go_zone.append(value)
            elif column1 == column2:
                if row2 - row1 + 1 != 5:
                    print("Please insert a valid command! (For example: 4B-4F)")
                    return carrier()
                else:
                    for i in range(row1, row2 + 1):
                        self.__cells[i][column1].ship = True
                        no_go_zone.append([i, column1])
                        for value in surrounding_area(i, column1):
                            no_go_zone.append(value)
            else:
                print("Please insert a valid command! (For example: 4B-4F)")
                return carrier()

        def battleship():
            string = input("Where will your Battleship ship be? (Size of 4 squares):\n")
            try:
                row1, column1, row2, column2 = input_string(string)
            except TypeError as te:
                print(te)
                return battleship()

            if row1 == row2:
                if column2 - column1 + 1 != 4:
                    print("Please insert a valid command! (For example: 8E-8H)")
                    return battleship()
                else:
                    for i in range(column1, column2 + 1):
                        for list in no_go_zone:
                            if [row1, i] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return battleship()
                    for i in range(column1, column2 + 1):
                        self.__cells[row1][i].ship = True
                        no_go_zone.append([row1, i])
                        for value in surrounding_area(row1, i):
                            no_go_zone.append(value)
                    return True
            elif column1 == column2:
                if row2 - row1 + 1 != 4:
                    print("Please insert a valid command! (For example: 8E-8H)")
                    return battleship()
                else:
                    for i in range(row1, row2 + 1):
                        for list in no_go_zone:
                            if [i, column1] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return battleship()
                    for i in range(row1, row2 + 1):
                        self.__cells[i][column1].ship = True
                        no_go_zone.append([i, column1])
                        for value in surrounding_area(i, column1):
                            no_go_zone.append(value)
                    return True
            else:
                print("Please insert a valid command! (For example: 8E-8H)")
                return battleship()

        def destroyer_and_submarine():
            string = input()
            try:
                row1, column1, row2, column2 = input_string(string)
            except TypeError as te:
                print(te)
                return destroyer_and_submarine()

            if row1 == row2:
                if column2 - column1 + 1 != 3:
                    print("Please insert a valid command! (For example: 3G-5G)")
                    return destroyer_and_submarine()
                else:
                    for i in range(column1, column2 + 1):
                        for list in no_go_zone:
                            if [row1, i] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return destroyer_and_submarine()
                    for i in range(column1, column2 + 1):
                        self.__cells[row1][i].ship = True
                        no_go_zone.append([row1, i])
                        for value in surrounding_area(row1, i):
                            no_go_zone.append(value)
                    return True
            elif column1 == column2:
                if row2 - row1 + 1 != 3:
                    print("Please insert a valid command! (For example: 3G-5G)")
                    return destroyer_and_submarine()
                else:
                    for i in range(row1, row2 + 1):
                        for list in no_go_zone:
                            if [i, column1] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return destroyer_and_submarine()
                    for i in range(row1, row2 + 1):
                        self.__cells[i][column1].ship = True
                        no_go_zone.append([i, column1])
                        for value in surrounding_area(i, column1):
                            no_go_zone.append(value)
                    return True
            else:
                print("Please insert a valid command! (For example: 3G-5G)")
                return destroyer_and_submarine()

        def patrol_boat():
            string = input("Where will your Patrol Boat ship be? (Size of 2 squares):\n")
            try:
                row1, column1, row2, column2 = input_string(string)
            except TypeError as te:
                print(te)
                return patrol_boat()

            if row1 == row2:
                if column2 - column1 + 1 != 2:
                    print("Please insert a valid command! (For example: 6E-6F)")
                    return patrol_boat()
                else:
                    for i in range(column1, column2 + 1):
                        for list in no_go_zone:
                            if [row1, i] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return patrol_boat()

                    for i in range(column1, column2 + 1):
                        self.__cells[row1][i].ship = True
                        no_go_zone.append([row1, i])
                        for value in surrounding_area(row1, i):
                            no_go_zone.append(value)
                    return True
            elif column1 == column2:
                if row2 - row1 + 1 != 2:
                    print("Please insert a valid command! (For example: 6E-6F)")
                    return patrol_boat()

                else:
                    for i in range(row1, row2 + 1):
                        for list in no_go_zone:
                            if [i, column1] == list:
                                print("Your ships cant overlap! Please leave one square between your ships")
                                return patrol_boat()
                    for i in range(row1, row2 + 1):
                        self.__cells[i][column1].ship = True
                        no_go_zone.append([i, column1])
                        for value in surrounding_area(i, column1):
                            no_go_zone.append(value)
                    return True
            else:
                print("Please insert a valid command! (For example: 6E-6F)")
                return patrol_boat()

        carrier()
        print(self.__str__())
        cleanup(no_go_zone)

        battleship()
        print(self.__str__())
        cleanup(no_go_zone)

        print("Where will your Destroyer ship be? (Size of 3 squares):\n")
        destroyer_and_submarine()
        print(self.__str__())
        cleanup(no_go_zone)

        print("Where will your Submarine ship be? (Size of 3 squares):\n")
        destroyer_and_submarine()
        print(self.__str__())
        cleanup(no_go_zone)

        patrol_boat()
        print(self.__str__())
        cleanup(no_go_zone)

    def get_cell(self, row, column):
        return self.__cells[row][column]

    def __str__(self):
        board = "\nPlayer's board:\n"
        board += "  "
        row_numbers = [" ⓿ ", " ❶ ", " ❷ ", " ❸ ", " ❹ ", " ❺ ", " ❻ ", " ❼ ", " ❽ ", " ❾ "]
        for row in range(0, self.__rows):
            # board += " " + str(row) + " "
            board += row_numbers[row]
        board += "\n"
        board += "  "
        for row in range(0, self.__rows * 2):
            board += "―"
        board += "\n"
        j = 0

        for row in range(0, self.__rows):
            board += get_letter_from_int(j) + "│"
            for column in range(0, self.__columns):
                cell = self.__cells[row][column]

                if cell.ship == True:
                    if cell.checked == True:
                        # board += " ❎ "
                        board += " ☒ "
                    else:
                        board += " ■ "
                elif cell.checked == True:
                    board += " ✕ "

                else:
                    board += " ◦ "

            board += "\n"
            j = j + 1
        return board


# Measure
"""

" ◦ "
" ■ "
" ✕ "
" ☒ "
" ― "

" ⓿ "
❶❷❸❹❺❻❼❽❾
①②③④⑤⑥⑦⑧⑨
" ❎ "


"""
