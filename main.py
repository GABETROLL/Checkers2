import pygame
from constants import *
from game import Game


class Play:

    PIECE_RADIUS = 29
    PIECE_OUTLINE = 2
    CROWN = pygame.image.load("assets/crown.png")

    def __init__(self):
        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.clock = pygame.time.Clock()
        self.running = True

        self.previous_click = False

        self.game = Game()

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_board()
            self.check_for_turns()

            pygame.display.update()

        pygame.quit()

    def check_for_turns(self):
        if self.game.turn == "r":
            if pygame.mouse.get_pressed(3)[0] and not self.previous_click:
                self.previous_click = True

                mouse_pos = pygame.mouse.get_pos()
                square = (mouse_pos[1] // BLOCK_WIDTH, mouse_pos[0] // BLOCK_WIDTH)

                if not self.game.selected_piece:
                    if self.game.get_piece(square)[0] == "r":
                        self.game.select(square)

                else:
                    # If we have already selected a piece (that belongs to us!!)
                    if square in self.game.valid_moves[self.game.selected_piece]:
                        self.game.move(square)

                        if self.game.get_winner():
                            self.running = False
                    else:
                        # If we have selected a piece, but we clicked somewhere that isn't a valid move,
                        self.game.selected_piece = None
                        # We assume the player changed their mind, and deselect the piece.
            elif not pygame.mouse.get_pressed(3)[0]:
                self.previous_click = False
        else:
            self.game.ai_move()

    def draw_tiles(self):
        for row in range(ROWS):
            if row % 2 == 0:
                for column in range(0, COLUMNS, 2):
                    pygame.draw.rect(self.WINDOW, RED,
                                     pygame.Rect(column * BLOCK_WIDTH, row * BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH))
            else:
                for column in range(1, COLUMNS, 2):
                    pygame.draw.rect(self.WINDOW, RED,
                                     pygame.Rect(column * BLOCK_WIDTH, row * BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH))

        if self.game.selected_piece:
            # If we have selected a piece,
            pygame.draw.rect(self.WINDOW, LIGHT_YELLOW, pygame.Rect(self.game.selected_piece[1] * BLOCK_WIDTH,
                                                                    self.game.selected_piece[0] * BLOCK_WIDTH,
                                                                    BLOCK_WIDTH,
                                                                    BLOCK_WIDTH))
            # we light up the square behind it.

    def draw_valid_moves(self):
        # {(3, 4): {(4, 5): [], (4, 3): []}, (5, 5): {(7, 7): [(6, 6)]}}
        selected_valid_moves = self.game.valid_moves.get(self.game.selected_piece)
        # We try to get the selected piece's valid move dictionary from the valid moves dictionary.
        if selected_valid_moves:
            # If we found the selected piece in the dictionary,
            for valid_move in selected_valid_moves:
                # We iterate over all the piece's valid moves
                pygame.draw.rect(self.WINDOW, LIGHT_BLUE, pygame.Rect(BLOCK_WIDTH * valid_move[1],
                                                                      BLOCK_WIDTH * valid_move[0],
                                                                      BLOCK_WIDTH,
                                                                      BLOCK_WIDTH))
                # And display them with a nice light blue square.

    def draw_pieces(self):
        for ri, row in enumerate(self.game.board):
            for ci, piece in enumerate(row):
                if piece != "  ":
                    # We iterate over each square.
                    # If the square is not empty,
                    pygame.draw.circle(self.WINDOW,
                                       GREY,
                                       (ci * BLOCK_WIDTH + BLOCK_WIDTH // 2, ri * BLOCK_WIDTH + BLOCK_WIDTH // 2),
                                       Play.PIECE_RADIUS + Play.PIECE_OUTLINE)
                    # We draw a grey outline to distinguish the piece from the background
                    pygame.draw.circle(self.WINDOW,
                                        Game.player_colors[piece[0]],
                                        (ci * BLOCK_WIDTH + BLOCK_WIDTH // 2, ri * BLOCK_WIDTH + BLOCK_WIDTH // 2),
                                        Play.PIECE_RADIUS)
                    # And the actual piece.
                    if piece[1] == "k":
                        # If the piece is a king,
                        self.WINDOW.blit(Play.CROWN, (ci * BLOCK_WIDTH + BLOCK_WIDTH // 2 - Play.CROWN.get_width() // 2,
                                                      ri * BLOCK_WIDTH + BLOCK_WIDTH // 2 - Play.CROWN.get_height() // 2))
                        # We draw a little crown over it.

    def draw_board(self):
        self.WINDOW.fill(BLACK)

        self.draw_tiles()
        self.draw_valid_moves() if self.game.selected_piece else None
        self.draw_pieces()


Play()
