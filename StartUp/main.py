from texttable import Texttable

from StartUp.Boardgame.board import Enemy_Board
from StartUp.Boardgame.player_board import Player_Board
from StartUp.gameplay.gameplay import Gameplay


if __name__ == '__main__':
    table = Texttable()
    table.set_cols_align(["l", "r", "c"])
    table.set_cols_valign(["t", "m", "b"])
    table.add_rows([["Name", "Age", "Nickname"],
                    ["Mr\nXavier\nHuon", 32, "Xav'"],
                    ["Mr\nBaptiste\nClement", 1, "Baby"],
                    ["Mme\nLouise\nBourgeau", 28, "Lou\n\nLoue"]])
    #print(table.draw() + "\n")
    print("\nWelcome to battleship!\n"
          "The rules are simple: Each player hides ships on a grid containing vertical and horizontal space coordinates.\n"
          "Players take turns calling out row and column coordinates on the other player's grid in an attempt to identify a square that contains a ship.\n"
          "The first player to sink all five of their opponent's ships wins the game!")

    enemy_board = Enemy_Board(10, 10)
    player_board = Player_Board(10, 10)
    game=Gameplay(player_board,enemy_board)

    game.play()


