from StartUp.Boardgame.cell import Cell


def surrounding_area(row, column):
    """
    :param row:
    :param column:
    :return: Program returns all the cells' indexes surrounding the given cell's row and column
    """
    return [row - 1, column - 1], [row - 1, column], [row - 1, column + 1], \
           [row, column - 1], [row, column], [row, column + 1], \
           [row + 1, column - 1], [row + 1, column], [row + 1, column + 1]


def cleanup(no_go_zone):
    """
    :param no_go_zone: A list of indexes
    :return: Program gets rid of duplicates and indexes that don't exist on the board and returns that list
    """
    s = []
    for list in no_go_zone:
        if list not in s:
            if 0 <= list[0] <= 9 and 0 <= list[1] <= 9:
                s.append(list)

    return s

def get_int_from_letter(letter):
    """
    :param letter:
    :return: Program returns the letter's index
    """
    if letter.upper() == "A": return 0
    if letter.upper() == "B": return 1
    if letter.upper() == "C": return 2
    if letter.upper() == "D": return 3
    if letter.upper() == "E": return 4
    if letter.upper() == "F": return 5
    if letter.upper() == "G": return 6
    if letter.upper() == "H": return 7
    if letter.upper() == "I": return 8
    if letter.upper() == "J": return 9
    raise TypeError(f"{letter} is outside the ocean! (Valid letters are between A and J - including both)")


def get_letter_from_int(x):
    """
    :param x:
    :return: Program returns the letter of that index
    """
    if x == 0: return "A"
    if x == 1: return "B"
    if x == 2: return "C"
    if x == 3: return "D"
    if x == 4: return "E"
    if x == 5: return "F"
    if x == 6: return "G"
    if x == 7: return "H"
    if x == 8: return "I"
    if x == 9: return "J"
    raise TypeError(f"{x} is outside the ocean! (Valid numbers are between 0 and 9 - including both)")

def order_in_cells(list):
    """
    :param list: A list of cells
    :return: Returns a list of cells similar to the first one but without their duplicates and without the cells
    that are "out of the ocean"
    """
    # s = []
    # for cell in list:
    #     if cell not in s:
    #         if 0 <= cell.row <= 9 and 0 <= cell.column <= 9:
    #             s.append(cell)

    l = list[:]
    for i in range (0,len(list)):
        for j in range(i+1, len(list)):
            if list[i].row==list[j].row and list[i].column==list[j].column:
                try:
                    l.remove(list[j])
                except ValueError:
                    pass
            if list[j].row<0 or list[j].row>9 or list[j].column<0 or list[j].column>9:
               try:
                    l.remove(list[j])
               except ValueError:
                   pass
    return l


def sunken_check(cell, one_way, another_way, player, board):
    """
    Program goes along the row/column and checks all the cells for cell.ship==True until it finds a
    cell that has no ship on it (cell.ship=False) - when the program stops going that way.
    Every cell that is a "good cell" (meaning cell.ship=True) is appended in a list "good_cells".

    :param cell:
    :param one_way: parameter will either be the "l" cell (for left) or "u" cell (for up)
    :param another_way: parameter will either be "r" cell (for right) or "d" cell (for down)
    :param player: either human or computer
    :param board: either human's board or computer's board
    :return: A list of all the cells that are part of the ship
    """
    good_cells = []
    if one_way.checked == one_way.ship == True: good_cells.append(one_way)
    if another_way.checked == another_way.ship == True: good_cells.append(another_way)
    if one_way.row == another_way.row:
        for i in range(one_way.column + 1, 10):
            current_cell = player.get_cell(board, cell.row, i)
            if current_cell.ship == False:
                break
            else:
                good_cells.append(current_cell)
        for j in range(another_way.column - 1, -1, -1):
            current_cell = player.get_cell(board, cell.row, j)
            if current_cell.ship == False:
                break
            else:
                good_cells.append(current_cell)
    else:
        for i in range(one_way.row + 1, 10):
            current_cell = player.get_cell(board, i, cell.column)
            if current_cell.ship == False:
                break
            else:
                good_cells.append(current_cell)
        for j in range(another_way.row - 1, -1, -1):
            current_cell = player.get_cell(board, j, cell.column)
            if current_cell.ship == False:
                break
            else:
                good_cells.append(current_cell)
    good_cells = order_in_cells(good_cells)
    # print(good_cells)
    return good_cells


def l_r_u_d_cells(cell, player, board):
    """
    :param cell:
    :param player:
    :param board:
    :return: Function returns the cell to the left, right, up and down (in that order) of the give cell parameter
    """
    if cell.column != 0:
        l_cell = player.get_cell(board, cell.row, cell.column - 1)
    else:
        l_cell = Cell(cell.row, cell.column, False, True)
    if cell.column != 9:
        r_cell = player.get_cell(board, cell.row, cell.column + 1)
    else:
        r_cell = Cell(cell.row, cell.column, False, True)
    if cell.row != 0:
        u_cell = player.get_cell(board, cell.row - 1, cell.column)
    else:
        u_cell = Cell(cell.row, cell.column, False, True)
    if cell.row != 9:
        d_cell = player.get_cell(board, cell.row + 1, cell.column)
    else:
        d_cell = Cell(cell.row, cell.column, False, True)
    return l_cell, r_cell, u_cell, d_cell
