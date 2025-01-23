from constants import *


class Game:
    player_colors = {"r": RED, "b": BLACK}

    def __init__(self):
        self.board = [["  " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.valid_moves = {}
        self.reset()

    def reset_board(self):
        for ri in range(0, 3):
            if ri % 2 == 0:
                for ci in range(1, COLUMNS, 2):
                    self.board[ri][ci] = "b "
            else:
                for ci in range(0, COLUMNS, 2):
                    self.board[ri][ci] = "b "

        for ri in range(5, ROWS):
            if ri % 2 == 0:
                for ci in range(1, COLUMNS, 2):
                    self.board[ri][ci] = "r "
            else:
                for ci in range(0, COLUMNS, 2):
                    self.board[ri][ci] = "r "

    def reset(self):
        self.reset_board()
        self.turn = "r"
        self.selected_piece = None
        self.set_valid_moves()
        # {(3, 4): {(4, 5): [], (4, 3): []}, (5, 5): {(7, 7): [(6, 6)]}}

    @property
    def black_pieces(self):
        result = []
        for ri, row in enumerate(self.board):
            for ci, square in enumerate(row):
                if square[0] == "b":
                    result.append((ri, ci))
        return result

    @property
    def red_pieces(self):
        result = []
        for ri, row in enumerate(self.board):
            for ci, square in enumerate(row):
                if square[0] == "r":
                    result.append((ri, ci))
        return result

    @property
    def direction(self):
        return -1 if self.turn == "r" else 1

    def get_piece(self, square):
        return self.board[square[0]][square[1]]

    def is_king(self, piece):
        return self.get_piece(piece)[1] == "k"

    def make_king(self, piece):
        if self.get_piece(piece) != "  ":
            self.board[piece[0]][piece[1]] = self.get_piece(piece)[:1] + "k"

    def _traverse_valid_moves(self, piece, original_piece=None):
        """Makes self.valid_moves[piece] a dictionary of all valid moves with the corresponding pieces to delete from
        the board.
        self.valid_moves is a dictionary of all pieces in board and their valid moves, dictionaries of all the squares
        and lists of pieces to jump over."""

        if self.is_king(piece):
            directions = [(self.direction, -1), (self.direction, 1), (-self.direction, -1), (-self.direction, 1)]
        else:
            directions = [(self.direction, -1), (self.direction, 1)]
        # Directions where pieces can move to, when they're kings or not.

        if -1 < piece[0] < ROWS and -1 < piece[1] < COLUMNS:
            # If the piece is inside the board,

            for direction in directions:
                # We look through each direction

                destination = (piece[0] + direction[0], piece[1] + direction[1])
                # and see the destination beside the piece.

                if -1 < destination[0] < ROWS and -1 < destination[1] < COLUMNS:
                    # If the destination is inside the board,

                    if original_piece:
                        # We check if we have already jumped over a piece.

                        if self.get_piece(destination)[0] != self.turn and \
                                self.get_piece(destination) != "  ":
                            # If we have, we check if the destination is filled with another piece we can jump over.

                            further_square = (destination[0] + direction[0], destination[1] + direction[1])

                            if -1 < further_square[0] < ROWS and -1 < further_square[1] < COLUMNS:

                                if self.get_piece(further_square) == "  ":

                                    self.valid_moves[original_piece][further_square] = [destination] + self.valid_moves[original_piece][piece]
                                    self._traverse_valid_moves(further_square, original_piece)
                                    # If there is, we check if the square behind it is empty and is in the board,
                                    # and if so, we add the blocked destination as a piece we can jump over and delete.
                                    # And set the further square as a valid move.
                    else:
                        # If we haven't jumped over pieces,
                        if self.get_piece(destination) == "  ":
                            # We check if the square right next to the piece is empty.

                            self.valid_moves[piece][destination] = []
                            # If it is, we add this square as a valid move, and add no pieces to delete.

                        elif self.get_piece(destination)[0] != self.turn and \
                                self.get_piece(destination) != "  ":
                            # If the square beside the piece is occupied by the opposite player,

                            further_square = (destination[0] + direction[0], destination[1] + direction[1])

                            if -1 < further_square[0] < ROWS and -1 < further_square[1] < COLUMNS:

                                if self.get_piece(further_square) == "  ":
                                    # We again check the further square to see if it's empty and in the board.

                                    self.valid_moves[piece][further_square] = [destination]
                                    self._traverse_valid_moves(further_square, piece)
                                    # If so, we add the further square as a valid move
                                    # and mark the piece we jumped over as a deleted piece, being the original piece.
                                    # We repeat the process from this piece, marking the original piece
                                    # was the original piece.

    def set_valid_moves(self):
        """Sets self.valid_moves to be a dictionary of
        all the pieces of the player that currently has the turn, which are dictionaries of all the valid moves
        that can be done on that piece."""
        self.valid_moves.clear()
        # {(3, 4): {(4, 5): [], (4, 3): []}, (5, 5): {(7, 7): [(6, 6)]}}

        for ri, row in enumerate(self.board):
            for ci, square in enumerate(row):
                # We iterate over each square.
                if square[0] == self.turn:
                    # If the square is occupied by a piece that belongs to the player who has a turn,
                    self.valid_moves[(ri, ci)] = {}
                    # We add the piece's dictionary to the dictionary
                    self._traverse_valid_moves((ri, ci))
                    # We check the valid moves of that piece.

    def delete(self, piece):
        """Deletes piece in board."""
        self.board[piece[0]][piece[1]] = "  "

    def move(self, destination):
        """Moves piece in board to destination (swaps piece with empty destination square).
        Makes piece king if it hits the edge of the screen before it swaps.
        Deletes all pieces we jumped over and resets information about turns, valid moves and selected piece."""
        print(destination)
        if destination[0] == 0 or destination[0] == ROWS - 1:
            self.make_king(self.selected_piece)
            # If we'll move a piece to an edge of the screen, it will be crowned.

        self.board[self.selected_piece[0]][self.selected_piece[1]], self.board[destination[0]][destination[1]] \
            = self.board[destination[0]][destination[1]], self.board[self.selected_piece[0]][self.selected_piece[1]]
        # We swap the piece for the empty space that it will occupy.

        for dp in self.valid_moves[self.selected_piece][destination]:
            self.delete(dp)
        # We delete all the pieces we jumped over.

        self.selected_piece = None
        # We moved, so we can't have a selected piece.
        self.turn = "r" if self.turn == "b" else "b"
        # We change the turn.
        self.set_valid_moves()
        # We check all valid moves for the new player.

    def select(self, piece):
        """Selects piece in the board."""
        self.selected_piece = piece

    def count(self, player):
        """returns how much pieces each player has in the board."""
        reds = 0
        blacks = 0

        for row in self.board:
            for square in row:
                # We iterate over each square and
                if square[0] == "r":
                    reds += 1
                elif square[0] == "b":
                    blacks += 1
                # Count the number of red and black squares.

        # If any of them are 0, the opposite player wins.
        return reds if player == "r" else blacks

    def get_winner(self):
        reds = self.count("r")
        blacks = self.count("b")
        # Count the number of red and black squares.

        # If any of them are 0, the opposite player wins.
        if reds == 0:
            return "b"
        elif blacks == 0:
            return "r"
        else:
            # If none of them are 0, a player can still win by making the opposite player not be able to move.
            for piece in self.valid_moves:
                if len(self.valid_moves[piece]) > 0:
                    return None
            # We iterate over each piece that belongs to the current player and it's valid moves.
            # If it's still possible for the player to move a piece, no player has won yet.

            return "r" if self.turn == "b" else "b"
            # If the player is stuck, we return the opposite player.

    def __copy__(self):
        game = Game()
        game.valid_moves = self.valid_moves
        game.selected_piece = self.selected_piece
        game.board = self.board
        game.turn = self.turn
        game.player_colors = self.player_colors

        return game

    def _traverse_ai_moves(self, depth, game=None, max_depth=3):
        # The ai would look in the second order in the valid_moves dictionary and
        # construct a list of all of the squares it can move.
        # For each of those moves, create a new Game instance to simulate what would happen when the ai moves
        # and then count all of the pieces again to bring up the minimax algorithm.
        # Ai would then decide which piece is best to move to which square, and pass that game to the next recursion.

        counts = []
        vms = game.valid_moves if game else self.valid_moves
        for piece in vms:
            for valid_move in vms[piece]:

                outcome = game.__copy__() if game else self.__copy__()

                counts += [(outcome.count("b") - outcome.count("r"), piece, valid_move, outcome)]

        counts.sort(key=lambda x: x[0])

        if depth == max_depth:
            return counts[1], counts[2]
        else:
            return self._traverse_ai_moves(depth + 1, counts[0][-1])

    def ai_move(self):
        result = self._traverse_ai_moves(0)
        self.select(result[0])
        self.move(result[1])

