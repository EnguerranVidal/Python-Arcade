import classes.pieces as pieces


class Board:
    def __init__(self):
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
