import traceback
from random import randint, choice

from StartUp.Boardgame.board import Enemy_Board
from StartUp.Boardgame.player_board import Player_Board
from StartUp.Functions.functionalities import surrounding_area, cleanup, get_int_from_letter, l_r_u_d_cells, \
    sunken_check, get_letter_from_int


class Gameplay:
    def __init__(self, player_board, enemy_board):
        self.__player_board = player_board
        self.__enemy_board = enemy_board
        self.__ships_left_p = 5
        self.__ships_left_c = 5
        # self.__p1 = p1
        # self.__p2 = p2

    def play(self):
        # while(self.__end==False)
        self.__player_move(0)

    def sunken_ship(self, list_of_cells, player, board, gm):
        for cell in list_of_cells:
            surr = list(surrounding_area(cell.row, cell.column))
            surr = cleanup(surr)
            for cell_index in surr:
                cell = player.get_cell(board, cell_index[0], cell_index[1])
                cell.checked = True

        print(player.__str__(board))
        if board == self.__player_board:
            print("Your ship has sunken!")
            self.__ships_left_p = self.__ships_left_p - 1
            if self.__ships_left_p != 0:
                return self.__player_move(0)

            print("\nYou lost the game!\nThe computer wins")
            return 0
        elif board == self.__enemy_board:
            print("You sunk the enemy's ship!")
            self.__ships_left_c = self.__ships_left_c - 1
            if self.__ships_left_c != 0:
                return self.__computer_move(gm)

            print("\nCongratulations!\nYou won the game!")
            return 0

    def __player_move(self, gm):
        try:

            print("\nYour turn!")
            print(Enemy_Board.__str__(self.__enemy_board))
            cell = input("Check cell: ")

            cell = list(cell)
            if len(cell) != 2:
                raise TypeError("Please insert a valid cell name (Example: 7J)")
            column = int(cell[0])
            row = get_int_from_letter(cell[1])
            if column > 9 or column < 0: raise TypeError("Please insert a valid cell name (Example: 7J)")

            cell = Enemy_Board.get_cell(self.__enemy_board, row, column)
            if cell.checked == True:
                raise TypeError("You already checked here!")

            cell.checked = True
            l, r, u, d = l_r_u_d_cells(cell, Enemy_Board, self.__enemy_board)

            if cell.ship == True:
                if l.ship == l.checked == True or r.checked == r.ship == True:
                    good_cells = sunken_check(cell, l, r, Enemy_Board, self.__enemy_board)
                    for cells in good_cells:
                        if cells.checked == False:
                            print("\nIt's a hit!")
                            return self.__player_move(gm)

                    return self.sunken_ship(good_cells, Enemy_Board, self.__enemy_board, gm)


                elif u.checked == u.ship == True or d.checked == d.ship == True:
                    good_cells = sunken_check(cell, u, d, Enemy_Board, self.__enemy_board)
                    for cells in good_cells:
                        if cells.checked == False:
                            print("\nIt's a hit!")
                            return self.__player_move(gm)

                    return self.sunken_ship(good_cells, Enemy_Board, self.__enemy_board, gm)

                else:
                    print("\nIt's a hit!")
                    return self.__player_move(gm)
            else:
                print(Enemy_Board.__str__(self.__enemy_board))
                print("\nIt's a miss!")
                return self.__computer_move(gm)  # End of round

        except Exception as ex:
            print(f"Error: {ex}")
            # traceback.print_exc()
            return self.__player_move(gm)  # Player can make another move - one that is valid

    def __computer_move(self, gm):
        if gm != 0: return self.__good_computer_move(gm)

        print("\nThe computer's turn!")
        row = randint(0, 9)
        column = randint(0, 9)

        cell = Player_Board.get_cell(self.__player_board, row, column)

        if cell.checked == True:
            return self.__computer_move(gm)

        print("Computer's choice of cell: " + str(column) + get_letter_from_int(row))
        cell.checked = True
        l, r, u, d = l_r_u_d_cells(cell, Player_Board, self.__player_board)

        if cell.ship == True:
            if l.ship == l.checked == True or r.checked == r.ship == True:
                good_cells = sunken_check(cell, l, r, Player_Board, self.__player_board)
                for cells in good_cells:
                    if cells.checked == False:
                        print(Player_Board.__str__(self.__player_board))
                        print("Your ship has been hit!\n")
                        gm = cell
                        return self.__good_computer_move(gm)

                return self.sunken_ship(good_cells, Player_Board, self.__player_board, gm)

            elif u.checked == u.ship == True or d.checked == d.ship == True:
                good_cells = sunken_check(cell, u, d, Player_Board, self.__player_board)
                for cells in good_cells:
                    if cells.checked == False:
                        print(Player_Board.__str__(self.__player_board))
                        print("Your ship has been hit!\n")
                        gm = cell
                        return self.__good_computer_move(gm)

                return self.sunken_ship(good_cells, Player_Board, self.__player_board, gm)

            else:
                print(Player_Board.__str__(self.__player_board))
                print("Your ship has been hit!\n")
                gm = cell
                return self.__good_computer_move(gm)
        else:
            print(Player_Board.__str__(self.__player_board))
            print("It's a miss!\n")
            return self.__player_move(gm)  # End of round

    def __good_computer_move(self, gm):
        """
        if we discovered l.ship or r.ship => check if sunken => if sunken return self.sunken
        if we discovered u.ship or d.ship => check if sunken => if sunken return self.sunken
        if we discovered one_way.ship==True =>
          if the_other_way.checked==True => hit one_way direction until sunken
          else: hit the_other_way direction (the_other_way.checked=True)
              if the_other_way.ship==True => gm=the_other_way (the whole cell);
                                              return self.__good_computer_move(gm)
              else: gm=one_way;
                    return self.__player_move(gm)
        elif x3 more times for all ways
        elif no info => random([l,r,u,d])
        """

        cell = gm
        l, r, u, d = l_r_u_d_cells(cell, Player_Board, self.__player_board)
        if l.ship == l.checked == True or r.ship == r.checked == True:
            all_the_current_ships_cells = sunken_check(cell, l, r, Player_Board, self.__player_board)
            number_of_cells = 0
            for cells in all_the_current_ships_cells:
                if cells.checked == True:
                    number_of_cells = number_of_cells + 1
            if number_of_cells == len(all_the_current_ships_cells):
                return self.sunken_ship(all_the_current_ships_cells, Player_Board, self.__player_board, gm)
        if u.ship == u.checked == True or d.ship == d.checked == True:
            all_the_current_ships_cells = sunken_check(cell, u, d, Player_Board, self.__player_board)
            number_of_cells = 0
            for cells in all_the_current_ships_cells:
                if cells.checked == True:
                    number_of_cells = number_of_cells + 1
            if number_of_cells == len(all_the_current_ships_cells):
                return self.sunken_ship(all_the_current_ships_cells, Player_Board, self.__player_board, gm)

        if l.ship == l.checked == True:
            if r.checked == True:
                for i in range(l.column - 1, -1, -1):  # hit left until sunken
                    hit_cell = Player_Board.get_cell(self.__player_board, cell.row, i)
                    hit_cell.checked = True
                    if hit_cell.ship == True:
                        print("Computer's choice of cell: " + str(hit_cell.column) + get_letter_from_int(hit_cell.row))
                        print(Player_Board.__str__(self.__player_board))
                        print("\nYour ship has been hit!")
                    else:
                        ships_cells = sunken_check(cell, l, r, Player_Board, self.__player_board)
                        return self.sunken_ship(ships_cells, Player_Board, self.__player_board, gm)
            else:
                print("Computer's choice of cell: " + str(r.column) + get_letter_from_int(r.row))
                r.checked = True
                if r.ship == True:
                    gm = r
                    print(Player_Board.__str__(self.__player_board))
                    print("\nYour ship has been hit!")
                    return self.__good_computer_move(gm)
                else:
                    gm = l
                    print(Player_Board.__str__(self.__player_board))
                    print("\nIt's a miss!")
                    return self.__player_move(gm)

        elif r.ship == r.checked == True:
            if l.checked == True:
                for i in range(r.column + 1, 10):
                    hit_cell = Player_Board.get_cell(self.__player_board, cell.row, i)
                    hit_cell.checked = True
                    if hit_cell.ship == True:
                        print("Computer's choice of cell: " + str(hit_cell.column) + get_letter_from_int(hit_cell.row))
                        print(Player_Board.__str__(self.__player_board))
                        print("\nYour ship has been hit!")
                    else:
                        ships_cells = sunken_check(cell, l, r, Player_Board, self.__player_board)
                        return self.sunken_ship(ships_cells, Player_Board, self.__player_board, gm)
            else:
                print("Computer's choice of cell: " + str(l.column) + get_letter_from_int(l.row))
                l.checked = True
                if l.ship == True:
                    gm = l
                    print(Player_Board.__str__(self.__player_board))
                    print("\nYour ship has been hit!")
                    return self.__good_computer_move(gm)
                else:
                    gm = r
                    print(Player_Board.__str__(self.__player_board))
                    print("\nIt's a miss!")
                    return self.__player_move(gm)

        elif u.ship == u.checked == True:
            if d.checked == True:
                for i in range(u.row - 1, -1, -1):
                    hit_cell = Player_Board.get_cell(self.__player_board, i, cell.column)
                    hit_cell.checked = True
                    if hit_cell.ship == True:
                        print("Computer's choice of cell: " + str(hit_cell.column) + get_letter_from_int(hit_cell.row))
                        print(Player_Board.__str__(self.__player_board))
                        print("\nYour ship has been hit!")
                    else:
                        ships_cells = sunken_check(cell, u, d, Player_Board, self.__player_board)
                        return self.sunken_ship(ships_cells, Player_Board, self.__player_board, gm)
            else:
                print("Computer's choice of cell: " + str(d.column) + get_letter_from_int(d.row))
                d.checked = True
                if d.ship == True:
                    gm = d
                    print(Player_Board.__str__(self.__player_board))
                    print("\nYour ship has been hit!")
                    return self.__good_computer_move(gm)
                else:
                    gm = u
                    print(Player_Board.__str__(self.__player_board))
                    print("\nIt's a miss!")
                    return self.__player_move(gm)

        elif d.ship == d.checked == True:
            if u.checked == True:
                for i in range(d.row + 1, 10):
                    hit_cell = Player_Board.get_cell(self.__player_board, i, cell.column)
                    hit_cell.checked = True
                    if hit_cell.ship == True:
                        print("Computer's choice of cell: " + str(hit_cell.column) + get_letter_from_int(hit_cell.row))
                        print(Player_Board.__str__(self.__player_board))
                        print("\nYour ship has been hit!")
                    else:
                        ships_cells = sunken_check(cell, u, d, Player_Board, self.__player_board)
                        return self.sunken_ship(ships_cells, Player_Board, self.__player_board, gm)
            else:
                print("Computer's choice of cell: " + str(u.column) + get_letter_from_int(u.row))
                u.checked = True
                if u.ship == True:
                    gm = u
                    print(Player_Board.__str__(self.__player_board))
                    print("\nYour ship has been hit!")
                    return self.__good_computer_move(gm)
                else:
                    gm = d
                    print(Player_Board.__str__(self.__player_board))
                    print("\nIt's a miss!")
                    return self.__player_move(gm)

        else:
            random_hit = choice([l, r, u, d])
            if random_hit.checked == True:
                return self.__good_computer_move(gm)  # If the random hit is outside the ocean case
            random_hit.checked = True
            print("Computer's choice of cell: " + str(random_hit.column) + get_letter_from_int(random_hit.row))

            if random_hit.ship == True:
                gm = random_hit
                print(Player_Board.__str__(self.__player_board))
                print("\nYour ship has been hit!")
                return self.__good_computer_move(gm)
            else:
                print(Player_Board.__str__(self.__player_board))
                print("\nIt's a miss!")
                return self.__player_move(gm)
