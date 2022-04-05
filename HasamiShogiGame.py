# Matt Chalabian
# CS 162
# November 25, 2021
# A program containing a classes that allow a user(s) to make moves and play a game of
# Hasami Shogi.  It consists of a HasamiShogiGame class and Board class.  The HasamiShogiGame class
# contains methods for playing a game of Hasami Shogi, and the Board class contains methods for
# setting up a new board and resetting the board, accessing spaces on the board, and displaying
# the board.

class HasamiShogiGame:
    """class that creates new hasami shogi game objects and has methods for carrying out moves, keeping
    track of player turn, and keeping track of game state"""

    def __init__(self):
        """creates a new game object with a new board, turn set to the black player, and game state
        set to unfinished"""
        self._board = Board()
        self._active_player = "BLACK"  # can be set to "BLACK" or "RED"
        self._game_state = "UNFINISHED"  # can be set to "UNFINISHED", "RED_WON", or "BLACK_WON"

    def get_game_state(self):
        """returns the current game state of the current shogi game"""
        return self._game_state

    def set_game_state(self, state):
        """takes a string argument and sets the current game state of the current shogi game"""
        self._game_state = state

    def get_active_player(self):
        """returns current player, used for figuring out turn and winner"""
        return self._active_player

    def set_active_player(self, player):
        """takes a string argument and sets the active player to that"""
        self._active_player = player

    def get_num_captured_pieces(self, player):
        """takes a string argument for player and returns number of pieces that player
        has captured"""
        total = 9  # starting piece amount
        tally = 0  # remaining pieces

        # figure out which remaining pieces to count
        if player == "BLACK":
            piece = "R"
        else:
            piece = "B"

        # tally remaining pieces
        for row in range(9):
            for column in range(9):
                if piece == self._board.get_board()[row + 1][column + 1]:
                    tally += 1

        # calculates and returns pieces captured
        return total - tally

    def get_square_occupant_str(self, location):
        """takes a two-character location string argument and returns the content held
        at that position in the form of a string"""
        # convert string location entry to row and column index values
        row_num = self.letter_converter(location)
        column_num = int(location[1])

        # return location contents
        return self._board.get_space_content(row_num, column_num)

    def get_square_occupant(self, location):
        """method that takes a two-character string argument and returns an all-caps string describing
        the contents of the location referred to by the argument"""
        if self.get_square_occupant_str(location) == ".":
            return "NONE"
        if self.get_square_occupant_str(location) == "B":
            return "BLACK"
        if self.get_square_occupant_str(location) == "R":
            return "RED"

    def set_square_occupant(self, location, content):
        """takes a two-character location string argument and a content argument and sets
        the specified location's occupancy to the content argument"""
        # convert string location entry to row and column index values
        row_num = self.letter_converter(location)
        column_num = int(location[1])

        # set location contents
        self._board.set_space_contents(row_num, column_num, content)

    def letter_converter(self, string):
        """converts first part of position string from letter to corresponding index value"""
        # finds corresponding number to letter input
        for num in range(9):
            if string[0] == self._board.get_letter_list()[num]:
                return num + 1

        # entered letter not within bounds
        return False

    def check_bounds(self, location):
        """input validation method that checks location string is 2 characters long and each character is within
        permitted bounds for the board.  returns True if all conditions are met, and False if any one condition
        is broken"""
        # check string length is correct
        if len(location) != 2:
            return False

        # check letter part is within bounds
        if not self.letter_converter(location):
            return False

        # check number part is within bounds
        if int(location[1]) < 1 or int(location[1]) > 9:
            return False

        # input is a space on the board
        return True

    def check_direction(self, location_1, location_2):
        """takes two location strings and returns True if the direction between them is horizontal or vertical, and
        returns False otherwise"""
        # set up variables as row and column index values
        loc1_row_num = self.letter_converter(location_1)
        loc1_column_num = int(location_1[1])
        loc2_row_num = self.letter_converter(location_2)
        loc2_column_num = int(location_2[1])

        # check if movement is horizontal or vertical, return true if so
        if ((loc1_column_num == loc2_column_num and loc1_row_num == loc2_row_num) or
                (loc1_column_num != loc2_column_num and loc1_row_num != loc2_row_num)):
            return False
        else:
            return True

    def check_obstacles(self, location_1, location_2):
        """takes two location strings and returns True if the direction between them is horizontal or vertical, and
        returns False otherwise"""
        # set up variables as row and column index values
        loc1_row_num = self.letter_converter(location_1)
        loc1_column_num = int(location_1[1])
        loc2_row_num = self.letter_converter(location_2)
        loc2_column_num = int(location_2[1])

        # call check middle spaces with variables passed in depending on conditions
        if loc1_row_num == loc2_row_num:
            return self.check_middle_spaces(loc1_column_num, loc2_column_num, loc1_row_num, "column")

        if loc1_column_num == loc2_column_num:
            return self.check_middle_spaces(loc1_row_num, loc2_row_num, loc1_column_num, "row")

    def check_middle_spaces(self, num_1, num_2, static_num, row_or_column):
        """method used by check obstacles that takes 3 int values and a string value as arguments to
        figure out which indices to iterate through and check the contents of those indices.  if '.' is
        returned for all indices, True is returned, otherwise, False is returned."""
        # set up values
        if num_1 > num_2:
            higher_val = num_1
            lower_val = num_2
        else:
            higher_val = num_2
            lower_val = num_1

        # check middle spaces if they are in a row
        if row_or_column == "row":
            for position in range(lower_val + 1, higher_val):
                if self._board.get_space_content(position, static_num) != ".":
                    return False

        # check middle spaces if they are in a column
        if row_or_column == "column":
            for position in range(lower_val + 1, higher_val):
                if self._board.get_space_content(static_num, position) != ".":
                    return False

        # no obstacles found in middle spaces
        return True

    def check_move_legality(self, space_from, space_to):
        """method that carries out a number of tests to make sure the inputs for a move are legal.
        takes two two-character string arguments and passes them through a number of tests. if all
        are passed, returns True, if one or more aren't passed, returns False"""
        # check game state
        if self.get_game_state() != "UNFINISHED":
            return False

        # check input validation
        if not (self.check_bounds(space_from) and self.check_bounds(space_to)):
            return False

        # check square_from has valid piece depending on player turn
        if self.get_active_player() == "BLACK" and self.get_square_occupant_str(space_from) != "B":
            return False
        if self.get_active_player() == "RED" and self.get_square_occupant_str(space_from) != "R":
            return False

        # check square_to is empty
        if self.get_square_occupant_str(space_to) != ".":
            return False

        # check move direction is horizontal or vertical only
        if not self.check_direction(space_from, space_to):
            return False

        # check that there are no obstacles in movement path
        if not self.check_obstacles(space_from, space_to):
            return False

        # all checks passed
        return True

    def check_captures(self, location):
        """method that takes a two-character string as an argument and adjusts the board to account"""
        # set up variables as row and column index values
        row_num = self.letter_converter(location)
        column_num = int(location[1])

        # check above captures
        self.check_capture_directions(row_num, column_num, -1, 0, 1)

        # check below captures
        self.check_capture_directions(row_num, column_num, 1, 0, 9)

        # check left captures
        self.check_capture_directions(row_num, column_num, 0, -1, 1)

        # check right captures
        self.check_capture_directions(row_num, column_num, 0, 1, 9)

        # check top right corner captures
        self.check_capture_corners(location, "a9", "a8", "b9")

        # check top left corner captures
        self.check_capture_corners(location, "a1", "a2", "b1")

        # check bottom right corner captures
        self.check_capture_corners(location, "i9", "i8", "h9")

        # check bottom left corner captures
        self.check_capture_corners(location, "i1", "i2", "h1")

    def check_capture_directions(self, row, column, x_mod, y_mod, boundary):
        """method that takes five integers as arguments. the first two are row and column arguments,
        the third and fourth are modifiers that adjust the row and column values. one of these arguments
        must always be 0 while the other must always be -1 or 1.  the final variable represents the edge
        position of the board"""

        # set up board tile content variables
        if self.get_active_player() == "BLACK":
            enemy = "R"
            player = "B"
        else:
            enemy = "B"
            player = "R"

        # set up sandwich condition
        sandwich = False

        # set variables for checking
        if y_mod == 0:  # checking above or below
            mod_val = row
            first_pos = row
        else:           # checking left or right
            mod_val = column
            first_pos = column

        # check spaces on board in single direction (up, down, left, right) according to variables
        while mod_val != boundary:

            # empty tile encountered, break loop
            if self._board.get_space_content(row + x_mod, column + y_mod) == ".":
                break

            # enemy piece encountered, adjust variables and continue loop
            elif self._board.get_space_content(row + x_mod, column + y_mod) == enemy:
                row += x_mod
                column += y_mod
                mod_val = mod_val + x_mod + y_mod

            # player piece encountered, sandwich occurs, adjust variables, and break loop
            elif self._board.get_space_content(row + x_mod, column + y_mod) == player:
                sandwich = True
                row += x_mod
                column += y_mod
                mod_val = mod_val + x_mod + y_mod
                break

        # if a sandwich occurs, clear appropriate tiles
        if sandwich:

            # set up variables for range of tiles on board needing content adjusted
            if first_pos < mod_val:
                second_pos = mod_val
            else:
                second_pos = first_pos
                first_pos = mod_val

            # iterate through range of tiles
            for index in range(first_pos + 1, second_pos):
                if y_mod == 0:  # horizontally
                    self._board.set_space_contents(index, column, ".")
                else:           # vertically
                    self._board.set_space_contents(row, index, ".")

    def check_capture_corners(self, space_to, corner, edge_1, edge_2):
        """method that takes four string arguments, space_to being the space the player-picked piece
        is moved to, corner being the corner being checked, and edge_1 and edge_2 being the two neighboring
        spaces to that corner.  captures and removes the corner piece if conditions are met"""
        # checks if the space_to tile matches one of the possible corner-adjacent tiles
        if space_to == edge_1 or space_to == edge_2:

            # checks if the corner tile holds an enemy tile and both adjacent tiles hold ally tiles
            if (self.get_active_player() == "BLACK" and self.get_square_occupant_str(edge_1) == "B"
                    and self.get_square_occupant_str(edge_2) == "B" and self.get_square_occupant_str(corner) == "R"):
                self.set_square_occupant(corner, ".")

            if (self.get_active_player() == "RED" and self.get_square_occupant_str(edge_1) == "R"
                    and self.get_square_occupant_str(edge_2) == "R" and self.get_square_occupant_str(corner) == "B"):
                self.set_square_occupant(corner, ".")

    def make_move(self, space_from, space_to):
        """method used by both players to make moves. takes two two-character string arguments
        and checks the move legality, carries out legal moves, handles captures, and sets game
        and player turn states.  returns False and makes no changes if move is illegal.  returns
        True is move is legal and carried out."""
        # check move legality
        if not self.check_move_legality(space_from, space_to):
            return False

        # move piece by setting space_to contents to space_from contents
        # set space_from contents to "." to mark it as an empty space
        self.set_square_occupant(space_to, self.get_square_occupant_str(space_from))
        self.set_square_occupant(space_from, ".")

        # check and carry out captures
        self.check_captures(space_to)

        # check if a player won with the move and set game_state if so
        if self.get_num_captured_pieces(self.get_active_player()) > 7:
            if self.get_active_player() == "BLACK":
                self.set_game_state("BLACK_WON")
            else:
                self.set_game_state("RED_WON")

        # pass player turn if game is still going
        if self.get_game_state() == "UNFINISHED":
            if self.get_active_player() == "BLACK":
                self.set_active_player("RED")
            else:
                self.set_active_player("BLACK")

        # turn complete
        return True


class Board:
    """class that stores the board data and has methods for resetting and editing the board"""

    def __init__(self):
        """creates a new board object with all pieces in starting position"""
        self._board = []
        self._letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  # used for various conversions
        self.fill_board()  # fills empty _board data member

    def get_space_content(self, row, column):
        """takes a row index position (int), a column index position (int), and returns contents the
        of that space (string)"""
        return self._board[row][column]

    def set_space_contents(self, row, column, contents):
        """takes a row index position (int), a column index position (int), and contents (string)
        argument, and sets the space to the passed-in contents"""
        self._board[row][column] = contents

    def get_board(self):
        """returns current stored board"""
        return self._board

    def get_letter_list(self):
        """returns board letter list"""
        return self._letter_list

    def fill_board(self):
        """clears and fills the board data member with a freshly set board for a new game of Hasami Shogi"""
        self._board.clear()
        for row in range(10):
            self._board.append([])

            for column in range(10):

                # places top left corner empty string
                if row == 0 and column == 0:
                    self._board[row].append(" ")

                # place row and column markers
                elif row == 0 and column > 0:
                    self._board[row].append(str(column))
                elif column == 0 and row > 0:
                    for index in range(9):
                        if row == index + 1:
                            self._board[row].append(self._letter_list[index])

                # place black and red pieces in starting positions
                elif row == 1 and column > 0:
                    self._board[row].append("R")
                elif row == 9 and column > 0:  # calculates and returns pieces captured
                    self._board[row].append("B")

                # place empty spaces marked by periods
                else:
                    self._board[row].append(".")

    def display_board(self):
        """prints the current board state"""
        for row in range(10):
            for column in range(10):
                print(self._board[row][column], end=" ")
            print()


shog = HasamiShogiGame()
shog._board.display_board()
shog.make_move("i8", "h8")
shog._board.display_board()
shog.make_move("a9", "h9")
shog._board.display_board()
shog.make_move("h8", "h7")
shog._board.display_board()
shog.make_move("a8", "i8")
shog._board.display_board()

