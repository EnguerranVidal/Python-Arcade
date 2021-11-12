from classes.checks import*


class Piece:
    def __init__(self, color=True):
        self.color = color
        self.name = ""

    def is_king(self):
        return False

    def is_valid_move(self, board, start, to):
        pass

    def is_white(self):
        return self.color

    def __str__(self):
        if self.color:
            return self.name
        else:
            return '\033[94m' + self.name + '\033[0m'


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "R"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        if start[0] == to[0]:  # SAME LINE
            tiles = row(start, to)
            for i in tiles:
                if board[start[0]][i] is not None:
                    return False
            return take_or_move(board, piece.color, to)
        elif start[1] == to[1]:  # SAME COLUMN
            tiles = column(start, to)
            for i in tiles:
                if board[i][start[1]] is not None:
                    return False
            return take_or_move(board, piece.color, to)
        else:
            return False


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "N"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        tiles = knight_destinations(start)
        if [to[0], to[1]] in tiles:
            return take_or_move(board, piece.color, to)
        else:
            return False


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "B"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        if abs(start[0] - to[0]) == abs(start[1] - to[1]):
            tiles = diagonal(start, to)
            tiles.pop(0)
            for i in tiles:
                if board[i[0]][i[1]] is not None:
                    if board[i[0]][i[1]].name != "GP":
                        return False
            return take_or_move(board, piece.color, to)
        else:
            return False


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "P"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        if piece.color:  # White pawn
            if start[1] == to[1] and start[0] - to[0] == 1:  # Going Forward +1
                if board[to[0]][to[1]] is None:
                    return True
                else:
                    return False
            elif start[1] == to[1] and start[0] - to[0] == 2 and start[0] == 6:  # Going Forward +2
                tiles = column(start, to)
                for i in tiles:
                    if board[i][start[1]] is not None:
                        return False
                if board[to[0]][to[1]] is None:
                    return True
                else:
                    return False
            elif abs(start[0] - to[0]) == abs(start[1] - to[1]):  # Taking on sides
                tiles = pawn_destinations(start, piece.color)
                if [to[0], to[1]] in tiles:
                    return take(board, piece.color, to)
                else:
                    return False
            else:
                return False
        else:  # Black Pawn
            if start[1] == to[1] and to[0] - start[0] == 1:  # Going Backward -1
                if board[to[0]][to[1]] is None:
                    return True
                else:
                    return False
            elif start[1] == to[1] and to[0] - start[0] == 2 and start[0] == 1:  # Going Backward -2
                tiles = column(start, to)
                for i in tiles:
                    if board[i][start[1]] is not None:
                        return False
                if board[to[0]][to[1]] is None:
                    return True
                else:
                    return False
            elif abs(start[0] - to[0]) == abs(start[1] - to[1]):  # Taking on sides
                tiles = pawn_destinations(start, piece.color)
                if [to[0], to[1]] in tiles:
                    return take(board, piece.color, to)
                else:
                    return False
            else:
                return False


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "Q"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        if start[0] == to[0]:  # SAME LINE
            tiles = row(start, to)
            for i in tiles:
                if board[start[0]][i] is not None:
                    if board[start[0]][i].name != "GP":
                        return False
            return take_or_move(board, piece.color, to)
        elif start[1] == to[1]:  # SAME COLUMN
            tiles = column(start, to)
            for i in tiles:
                if board[i][start[1]] is not None:
                    if board[i][start[1]].name != "GP":
                        return False
            return take_or_move(board, piece.color, to)
        elif abs(start[0] - to[0]) == abs(start[1] - to[1]):
            tiles = diagonal(start, to)
            tiles.pop(0)
            for i in tiles:
                if board[i[0]][i[1]] is not None:
                    if board[i[0]][i[1]].name != "GP":
                        return False
            return take_or_move(board, piece.color, to)
        else:
            return False


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "K"

    def is_valid_move(self, board, start, to):
        piece = board[start[0]][start[1]]
        if start[0] == to[0] and abs(start[1] - to[1]) == 1:  # LEFT OR RIGHT
            return take_or_move(board, piece.color, to)
        elif start[1] == to[1] and abs(start[0] - to[0]) == 1:  # UP OR DOWN
            return take_or_move(board, piece.color, to)
        elif abs(start[0] - to[0]) == abs(start[1] - to[1]) and abs(start[0] - to[0]) == 1:
            return take_or_move(board, piece.color, to)  # DIAGONALS
        else:
            return False

    def is_king(self):
        return True


class Ghost_Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = "GP"

    def is_valid_move(self, board, start, to):
        return False
