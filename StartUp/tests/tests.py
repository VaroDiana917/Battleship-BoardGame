import unittest

from StartUp.Boardgame.board import Enemy_Board
from StartUp.Boardgame.cell import Cell
from StartUp.Functions.functionalities import surrounding_area, cleanup, get_int_from_letter, get_letter_from_int, \
    order_in_cells


class MyTestCase(unittest.TestCase):
    def test_surrounding_area(self):
        row, column = 5, 5
        surroundings = list(surrounding_area(row, column))
        self.assertEqual(surroundings, [[4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [6, 4], [6, 5], [6, 6]])

    def test_cleanup(self):
        list = [[-1, 0], [3, 7], [3, 7]]
        self.assertEqual(cleanup(list), [[3, 7]])

    def test_get_int_from_letter(self):
        letters = ["A", "b", "C", "D", "E", "f", "G", "H", "i", "J"]
        for i in range(0, len(letters)):
            self.assertEqual(get_int_from_letter(letters[i]), i)

        self.assertRaises(TypeError, lambda: get_int_from_letter("K"))

    def test_get_letter_from_int(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for i in range(0, len(letters)):
            self.assertEqual(get_letter_from_int(i), letters[i])

        self.assertRaises(TypeError, lambda: get_letter_from_int(10))

    def test_order_in_cells(self):
        cells = []

        cells.append(Cell(5, 5, False, False))
        cells.append(Cell(5, 5, True, True))
        cells.append(Cell(-5, 7, False, False))
        cells.append(Cell(-5, 7, True, True))
        cells.append(Cell(7, -5, False, False))
        cells.append(Cell(3, 7, True, True))

        self.assertEqual(order_in_cells(cells), [Cell(5, 5, False, False), Cell(3, 7, True, True)])

    def test_Enemy_Board(self):
        board = Enemy_Board(10, 10)
        ship_cells = 0
        for row in range(0, 10):
            for column in range(0, 10):
                if board.get_cell(row, column).ship == True:
                    ship_cells = ship_cells + 1
        self.assertEqual(ship_cells, 5 + 4 + 3 + 3 + 2)

    def tearDown(self):
        print("Torn Down")
