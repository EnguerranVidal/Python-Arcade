##################### IMPORTS #####################

# Python files imports
import classes.board as board
import classes.pieces as pieces
import classes.sprites as sprites

# Libraries imports
import pygame
import pygame_gui
import os


class ChessGame:
    def __init__(self):
        # Initializing main window
        pygame.init()
        pygame.display.set_caption('CHESS')
        self.window_surface = pygame.display.set_mode((800, 580))

        # Important paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.current_dir, "images")
        self.pieces_path = os.path.join(self.images_path, "pieces")
        self.board_path = os.path.join(self.images_path, "boards")

        # Window Icon
        self.Icon = pygame.image.load(os.path.join(self.pieces_path, "white_king.png"))
        pygame.display.set_icon(self.Icon)

        # Board Image and background setting
        self.board_image = pygame.transform.scale(pygame.image.load(os.path.join(self.board_path, "green.png")),
                                                  (520, 520))
        self.empty_surface = pygame.Surface((65, 65))
        self.window_surface.blit(self.board_image, (30, 30))
        self.board = board.Board()
        self.board.empty()

        # UI Manager
        self.manager = pygame_gui.UIManager((800, 580), "theme.json")

        # New Game Button
        self.new_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((580, 30), (100, 50)),
                                                       text='New Game', manager=self.manager)

        # Other Variables
        self.pieces_labels = ["R", "N", "B", "Q", "K", "P"]
        self.pieces_names = ["rook", "knight", "bishop", "queen", "king", "pawn"]

        self.clock = None
        self.turn = True
        self.castle = False

        # Selection
        self.selected = False
        self.selected_piece = None
        self.selected_position = None
        selected_path = os.path.join(self.board_path, "move_tile.png")
        move_path = os.path.join(self.board_path, "move_tile.png")
        self.move_image = pygame.transform.scale(pygame.image.load(move_path), (65, 65))
        # Check image
        check_path = os.path.join(self.board_path, "check_tile.png")
        self.check_image = pygame.transform.scale(pygame.image.load(check_path), (65, 65))
        # Available Moves
        self.available_moves = []
        available_path = os.path.join(self.board_path, "move_tile.png")
        self.available_image = pygame.transform.scale(pygame.image.load(selected_path), (65, 65))
        # Player Times
        self.whites_time = 0.
        self.blacks_time = 0.
        # Previous Turn
        self.previous_move = [[None, None]] * 2

    def run(self):
        continuing = True
        self.clock = pygame.time.Clock()
        while continuing:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuing = False
                if event.type == pygame.MOUSEBUTTONUP:  # Clicking
                    pos = pygame.mouse.get_pos()
                    if 30 < pos[0] < 550 and 30 < pos[1] < 550:
                        tile_x = (pos[0] - 30) // 65
                        tile_y = (pos[1] - 30) // 65
                        piece = self.board.board[tile_y][tile_x]
                        if piece is not None and piece.name in self.pieces_labels:
                            if piece.color == self.turn:  # Piece from the current player
                                self.select_piece((tile_y, tile_x))
                            else:
                                if self.selected and (tile_y, tile_x) in self.available_moves:
                                    self.move(self.selected_position, (tile_y, tile_x))
                                else:
                                    self.unselect_piece()
                        else:
                            if self.selected and (tile_y, tile_x) in self.available_moves:
                                self.move(self.selected_position, (tile_y, tile_x))
                            else:
                                self.unselect_piece()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.new_button:
                            self.new_game()
                self.manager.process_events(event)
            self.manager.draw_ui(self.window_surface)
            self.manager.update(time_delta)
            pygame.display.flip()
        pygame.quit()

    def new_game(self):
        self.board.reinitialize()
        self.clear_promotion()
        self.selected = False
        self.turn = True
        self.display_board()
        self.board.situation_check(True)

    def select_piece(self, pos):
        self.selected = True
        self.selected_piece = self.board.board[pos[0]][pos[1]]
        self.selected_position = pos
        # Finding available moves positions
        self.available_moves = self.board.available_moves(self.turn, pos)
        # Adding castle if king is selected
        if self.selected_piece.name == "K" and not self.selected_piece.moved:
            if self.turn:
                if self.board.can_king_castle(self.turn):
                    self.available_moves.append((7, 6))
                    self.castle = True
                if self.board.can_queen_castle(self.turn):
                    self.available_moves.append((7, 2))
                    self.castle = True
            else:
                if self.board.can_king_castle(self.turn):
                    self.available_moves.append((0, 6))
                    self.castle = True
                if self.board.can_queen_castle(self.turn):
                    self.available_moves.append((0, 2))
                    self.castle = True
        self.display_board()

    def unselect_piece(self):
        self.selected = False
        self.selected_piece = None
        self.available_moves = []
        # need to add clearing of movable tiles
        self.display_board()

    def move(self, start, finish):
        if self.turn and start == (7, 4):  # WHITE KING
            if self.selected_piece.name == "K" and self.castle:
                if finish == (7, 6):
                    self.board.move_piece([7, 7], [7, 5])
                if finish == (7, 2):
                    self.board.move_piece([7, 0], [7, 3])
        if not self.turn and start == (0, 4):  # BLACK KING
            if self.selected_piece.name == "K" and self.castle:
                if finish == (0, 6):
                    self.board.move_piece([0, 7], [0, 5])
                if finish == (0, 2):
                    self.board.move_piece([0, 0], [0, 3])
        self.board.move_piece(start, finish)
        self.unselect_piece()
        self.display_board()
        self.castle = False
        if self.board.check_promotion(self.turn):
            self.display_promotion()
            promotion = True
            while promotion:
                time_delta = self.clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        continuing = False
                    if event.type == pygame.MOUSEBUTTONUP:  # Clicking
                        pos = pygame.mouse.get_pos()
                        if 580 < pos[0] < 645 and 160 < pos[1] < 420:
                            piece = (pos[1] - 160) // 65
                            self.board.promote(self.turn, piece)
                            promotion = False
                            self.clear_promotion()
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.new_button:
                                self.new_game()
                    self.manager.process_events(event)
                self.manager.draw_ui(self.window_surface)
                self.manager.update(time_delta)
                pygame.display.flip()
        # Changing Turn
        self.turn = not self.turn
        self.board.clean_ghost_pawn(self.turn)
        self.display_board()
        print(self.board.evaluate())

    def display_board(self):
        self.window_surface.blit(self.board_image, (30, 30))
        if self.selected:
            pos_x = 30 + self.selected_position[1] * 65
            pos_y = 30 + self.selected_position[0] * 65
            self.window_surface.blit(self.move_image, (pos_x, pos_y))
            for i in self.available_moves:
                pos_x = 30 + i[1] * 65
                pos_y = 30 + i[0] * 65
                self.window_surface.blit(self.move_image, (pos_x, pos_y))
        if self.board.situation_check(self.turn):
            king = self.board.find_king(self.turn)
            pos_x = 30 + king[1] * 65
            pos_y = 30 + king[0] * 65
            self.window_surface.blit(self.check_image, (pos_x, pos_y))
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece is not None and piece.name in self.pieces_labels:  # Piece is present
                    number = self.pieces_labels.index(piece.name)
                    if piece.color:  # White Piece
                        path = os.path.join(self.pieces_path, "white_" + self.pieces_names[number] + ".png")
                        piece_image = pygame.transform.scale(pygame.image.load(path), (65, 65))
                        pos_x = 30 + j * 65
                        pos_y = 30 + i * 65
                        self.window_surface.blit(piece_image, (pos_x, pos_y))
                    else:  # Black Piece
                        path = os.path.join(self.pieces_path, "black_" + self.pieces_names[number] + ".png")
                        piece_image = pygame.transform.scale(pygame.image.load(path), (65, 65))
                        pos_x = 30 + j * 65
                        pos_y = 30 + i * 65
                        self.window_surface.blit(piece_image, (pos_x, pos_y))

    def display_promotion(self):
        promotion_pieces = ["queen", "rook", "bishop", "knight"]
        path = os.path.join(self.board_path, "white_tile.png")
        tile = pygame.transform.scale(pygame.image.load(path), (65, 65))
        for i in range(4):
            pos_x = 580
            pos_y = 160 + i * 65
            self.window_surface.blit(tile, (pos_x, pos_y))
            if self.turn:
                path = os.path.join(self.pieces_path, "white_" + promotion_pieces[i] + ".png")
                piece_image = pygame.transform.scale(pygame.image.load(path), (65, 65))
            else:
                path = os.path.join(self.pieces_path, "black_" + promotion_pieces[i] + ".png")
                piece_image = pygame.transform.scale(pygame.image.load(path), (65, 65))
            self.window_surface.blit(piece_image, (pos_x, pos_y))

    def clear_promotion(self):
        path = os.path.join(self.board_path, "cover_up.png")
        cover = pygame.transform.scale(pygame.image.load(path), (65, 65))
        for i in range(4):
            pos_x = 580
            pos_y = 160 + i * 65
            self.window_surface.blit(cover, (pos_x, pos_y))



if __name__ == '__main__':
    ChessGame().run()
