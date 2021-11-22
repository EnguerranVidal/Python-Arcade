import classes.pieces as pieces
import classes.checks as checks
import copy


class Board:
    def __init__(self):
        self.board = []
        self.pieces_labels = ["R", "N", "B", "Q", "K", "P"]
        for i in range(8):
            self.board.append([None] * 8)
        # Adding White Pieces in last two rows
        self.board[7][0] = pieces.Rook(True)
        self.board[7][1] = pieces.Knight(True)
        self.board[7][2] = pieces.Bishop(True)
        self.board[7][3] = pieces.Queen(True)
        self.board[7][4] = pieces.King(True)
        self.board[7][5] = pieces.Bishop(True)
        self.board[7][6] = pieces.Knight(True)
        self.board[7][7] = pieces.Rook(True)

        for i in range(8):
            self.board[6][i] = pieces.Pawn(True)

        # Adding Black Pieces in first two rows
        self.board[0][0] = pieces.Rook(False)
        self.board[0][1] = pieces.Knight(False)
        self.board[0][2] = pieces.Bishop(False)
        self.board[0][3] = pieces.Queen(False)
        self.board[0][4] = pieces.King(False)
        self.board[0][5] = pieces.Bishop(False)
        self.board[0][6] = pieces.Knight(False)
        self.board[0][7] = pieces.Rook(False)

        for i in range(8):
            self.board[1][i] = pieces.Pawn(False)

    def print_board(self):
        print(33 * "*")
        for i in range(8):
            buffer = "|"
            for j in range(8):
                if self.board[i][j] is None:
                    buffer = buffer + '   |'
                else:
                    buffer = buffer + ' ' + str(self.board[i][j]) + ' |'
            print(buffer)
        print(33 * "*")

    def empty(self):
        self.board = []
        for i in range(8):
            self.board.append([None] * 8)

    def reinitialize(self):
        self.empty()
        self.board = []
        for i in range(8):
            self.board.append([None] * 8)
        # Adding White Pieces in last two rows
        self.board[7][0] = pieces.Rook(True)
        self.board[7][1] = pieces.Knight(True)
        self.board[7][2] = pieces.Bishop(True)
        self.board[7][3] = pieces.Queen(True)
        self.board[7][4] = pieces.King(True)
        self.board[7][5] = pieces.Bishop(True)
        self.board[7][6] = pieces.Knight(True)
        self.board[7][7] = pieces.Rook(True)

        for i in range(8):
            self.board[6][i] = pieces.Pawn(True)

        # Adding Black Pieces in first two rows
        self.board[0][0] = pieces.Rook(False)
        self.board[0][1] = pieces.Knight(False)
        self.board[0][2] = pieces.Bishop(False)
        self.board[0][3] = pieces.Queen(False)
        self.board[0][4] = pieces.King(False)
        self.board[0][5] = pieces.Bishop(False)
        self.board[0][6] = pieces.Knight(False)
        self.board[0][7] = pieces.Rook(False)

        for i in range(8):
            self.board[1][i] = pieces.Pawn(False)

    def move_piece(self, start: list, finish: list):
        piece = self.board[start[0]][start[1]]
        taken = self.board[finish[0]][finish[1]]
        # Adding possible ghost pawns
        if piece.name == "P":
            if piece.color:
                if start[0] == 6 and finish[0] == 4:
                    self.board[5][start[1]] = pieces.Ghost_Pawn(True)
            else:
                if start[0] == 1 and finish[0] == 3:
                    self.board[2][start[1]] = pieces.Ghost_Pawn(False)
            if taken is not None and taken.name == "GP":
                if taken.color:
                    self.board[4][finish[1]] = None
                else:
                    self.board[3][finish[1]] = None
        # Moving piece across board
        self.board[finish[0]][finish[1]] = piece
        self.board[start[0]][start[1]] = None
        self.board[finish[0]][finish[1]].moved = True

    def available_moves(self, turn, pos):
        moves = []
        piece = self.board[pos[0]][pos[1]]
        for i in range(8):
            for j in range(8):
                if piece.is_valid_move(self.board, pos, (i, j)):
                    if not self.situation_turn_check(turn, pos, (i, j)):
                        moves.append((i, j))
        return moves

    def check_promotion(self, turn):
        if turn:
            for i in range(8):
                piece = self.board[0][i]
                if piece is not None:
                    if piece.color and piece.name == "P":
                        return True
            return False
        else:
            for i in range(8):
                piece = self.board[7][i]
                if piece is not None:
                    if piece.color is False and piece.name == "P":
                        return True
            return False

    def clean_ghost_pawn(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    if piece.name == "GP" and piece.color == color:
                        self.board[i][j] = None

    def find_king(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    if piece.name == "K" and piece.color == color:
                        king = (i, j)
        return king

    def situation_turn_check(self, turn, start, finish):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        new_board.move_piece(start, finish)
        check = new_board.situation_check(turn)
        del new_board
        return check

    def situation_check(self, turn):
        # Finding our King piece in the board
        king = self.find_king(turn)
        # Select columns and rows
        [left, right] = checks.left_right_row(self.board, king)
        [up, down] = checks.up_down_column(self.board, king)
        # Select diagonals
        [up_left, up_right] = checks.up_diagonals(self.board, king)
        [down_left, down_right] = checks.down_diagonals(self.board, king)
        knights = checks.knights(self.board, king)
        # Checking threats on given tiles
        for piece in knights:
            if piece is not None:
                if piece.name == "K" and piece.color != turn:
                    return True
        for i in range(len(up)):
            piece = up[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "R" and piece.color != turn:
                    return True
                elif piece.name == "Q" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(down)):
            piece = down[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "R" and piece.color != turn:
                    return True
                elif piece.name == "Q" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(left)):
            piece = left[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "R" and piece.color != turn:
                    return True
                elif piece.name == "Q" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(right)):
            piece = right[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "R" and piece.color != turn:
                    return True
                elif piece.name == "Q" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(up_left)):
            piece = up_left[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if turn:
                        if piece.name == "P" and piece.color != turn:
                            return True
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "Q" and piece.color != turn:
                    return True
                elif piece.name == "B" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(up_right)):
            piece = up_right[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if turn:
                        if piece.name == "P" and piece.color != turn:
                            return True
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "Q" and piece.color != turn:
                    return True
                elif piece.name == "B" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(down_left)):
            piece = down_left[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if not turn:
                        if piece.name == "P" and piece.color != turn:
                            return True
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "Q" and piece.color != turn:
                    return True
                elif piece.name == "B" and piece.color != turn:
                    return True
                else:
                    break
        for i in range(len(down_right)):
            piece = down_right[i]
            if piece is not None and piece.name != "GP":
                if i == 0:
                    if not turn:
                        if piece.name == "P" and piece.color != turn:
                            return True
                    if piece.name == "K" and piece.color != turn:
                        return True
                if piece.name == "Q" and piece.color != turn:
                    return True
                elif piece.name == "B" and piece.color != turn:
                    return True
                else:
                    break
        return False

    def situation_mat(self, turn):
        if self.situation_pat(turn) and self.situation_check(turn):
            return True
        else:
            return False

    def situation_pat(self, turn):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    if piece.name in self.pieces_labels and piece.color == turn:
                        if len(self.available_moves(turn, (i, j))) != 0:
                            return False
        return True

    def can_king_castle(self, turn):
        if turn:
            king_position = self.board[7][4]
            bishop_position = self.board[7][5]
            knight_position = self.board[7][6]
            rook_position = self.board[7][7]
            if king_position is None or king_position.moved:
                return False
            if rook_position is None or rook_position.moved:
                return False
            if bishop_position is not None or knight_position is not None:
                return False
            # Checking threats to movement
            if self.situation_turn_check(turn, start=(7, 4), finish=(7, 5)):
                return False
            if self.situation_turn_check(turn, start=(7, 4), finish=(7, 6)):
                return False
            # All conditions checked
            return True
        else:
            king_position = self.board[0][4]
            bishop_position = self.board[0][5]
            knight_position = self.board[0][6]
            rook_position = self.board[0][7]
            if king_position is None or king_position.moved:
                return False
            if rook_position is None or rook_position.moved:
                return False
            if bishop_position is not None or knight_position is not None:
                return False
            # Checking threats to movement
            if self.situation_turn_check(turn, start=(0, 4), finish=(0, 5)):
                return False
            if self.situation_turn_check(turn, start=(0, 4), finish=(0, 6)):
                return False
            # All conditions checked
            return True

    def can_queen_castle(self, turn):
        if turn:
            king_position = self.board[7][4]
            queen_position = self.board[7][3]
            bishop_position = self.board[7][2]
            knight_position = self.board[7][1]
            rook_position = self.board[7][0]
            if king_position is None or king_position.moved:
                return False
            if rook_position is None or rook_position.moved:
                return False
            if bishop_position is not None or knight_position is not None or queen_position is not None:
                return False
            # Checking threats to movement
            if self.situation_turn_check(turn, start=(7, 4), finish=(7, 3)):
                return False
            if self.situation_turn_check(turn, start=(7, 4), finish=(7, 2)):
                return False
            # All conditions checked
            return True
        else:
            king_position = self.board[0][4]
            queen_position = self.board[0][3]
            bishop_position = self.board[0][2]
            knight_position = self.board[0][1]
            rook_position = self.board[0][0]
            if king_position is None or king_position.moved:
                return False
            if rook_position is None or rook_position.moved:
                return False
            if bishop_position is not None or knight_position is not None or queen_position is not None:
                return False
            # Checking threats to movement
            if self.situation_turn_check(turn, start=(0, 4), finish=(0, 3)):
                return False
            if self.situation_turn_check(turn, start=(0, 4), finish=(0, 2)):
                return False
            # All conditions checked
            return True

    def promote(self, turn, number):
        number = int(number)
        if turn:
            for i in range(8):
                piece = self.board[0][i]
                if piece is not None and piece.name == "P":
                    if piece.color:
                        if number == 0:
                            self.board[0][i] = pieces.Queen(True)
                        if number == 1:
                            self.board[0][i] = pieces.Rook(True)
                        if number == 2:
                            self.board[0][i] = pieces.Bishop(True)
                        if number == 3:
                            self.board[0][i] = pieces.Knight(True)
        else:
            for i in range(8):
                piece = self.board[7][i]
                if piece is not None and piece.name == "P":
                    if not piece.color:
                        if number == 0:
                            self.board[7][i] = pieces.Queen(False)
                        if number == 1:
                            self.board[7][i] = pieces.Rook(False)
                        if number == 2:
                            self.board[7][i] = pieces.Bishop(False)
                        if number == 3:
                            self.board[7][i] = pieces.Knight(False)

    def evaluate(self):
        white = 0
        black = 0
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None and piece.name != "GP":
                    if piece.name != "K" and piece.color:
                        if piece.name == "Q":
                            white = white + 9
                        if piece.name == "R":
                            white = white + 5
                        if piece.name == "B":
                            white = white + 3
                        if piece.name == "K":
                            white = white + 3
                        if piece.name == "P":
                            white = white + 1
                    if piece.name != "K" and not piece.color:
                        if piece.name == "Q":
                            black = black + 9
                        if piece.name == "R":
                            black = black + 5
                        if piece.name == "B":
                            black = black + 3
                        if piece.name == "K":
                            black = black + 3
                        if piece.name == "P":
                            black = black + 1
        return white - black
