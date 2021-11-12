def row(start, finish):
    if start[1] < finish[1]:  # Right
        return list(range(start[1] + 1, finish[1]))
    else:  # Left
        return list(range(finish[1] + 1, start[1]))


def column(start, finish):
    if start[0] < finish[0]:  # Down
        return list(range(start[0] + 1, finish[0]))
    else:  # Up
        return list(range(finish[0] + 1, start[0]))


def diagonal(start, finish):
    tiles = [[start[0], start[1]]]
    if start[0] > finish[0] and start[1] > finish[1]:  # Top Left
        n = start[0] - finish[0]
        for i in range(1, n):
            tiles.append([tiles[-1][0] - 1, tiles[-1][1] - 1])
    if start[0] > finish[0] and start[1] < finish[1]:  # Top Right
        n = start[0] - finish[0]
        for i in range(1, n):
            tiles.append([tiles[-1][0] - 1, tiles[-1][1] + 1])
    if start[0] < finish[0] and start[1] > finish[1]:  # Bottom Left
        n = finish[0] - start[0]
        for i in range(1, n):
            tiles.append([tiles[-1][0] + 1, tiles[-1][1] - 1])
    if start[0] < finish[0] and start[1] < finish[1]:  # Bottom Right
        n = finish[0] - start[0]
        for i in range(1, n):
            tiles.append([tiles[-1][0] + 1, tiles[-1][1] + 1])
    return tiles


def knight_destinations(start):
    tiles = []
    if start[0] - 1 >= 0 and start[1] - 2 >= 0:  # LT
        tiles.append([start[0] - 1, start[1] - 2])
    if start[0] + 1 <= 7 and start[1] - 2 >= 0:  # LB
        tiles.append([start[0] + 1, start[1] - 2])
    if start[0] - 1 >= 0 and start[1] + 2 <= 7:  # RT
        tiles.append([start[0] - 1, start[1] + 2])
    if start[0] + 1 <= 7 and start[1] + 2 >= 0:  # RB
        tiles.append([start[0] + 1, start[1] + 2])
    if start[0] + 2 <= 7 and start[1] - 1 >= 0:  # BL
        tiles.append([start[0] + 2, start[1] - 1])
    if start[0] + 2 <= 7 and start[1] + 1 <= 7:  # BR
        tiles.append([start[0] + 2, start[1] + 1])
    if start[0] - 2 >= 0 and start[1] - 1 >= 0:  # TL
        tiles.append([start[0] - 2, start[1] - 1])
    if start[0] - 2 >= 0 and start[1] + 1 <= 7:  # TR
        tiles.append([start[0] - 2, start[1] + 1])
    return tiles


def pawn_destinations(start, color):
    tiles = []
    if color:  # White Pawn
        if start[0] - 1 >= 0 and start[1] - 1 >= 0:  # TL
            tiles.append([start[0] - 1, start[1] - 1])
        if start[0] - 1 >= 0 and start[1] + 1 <= 7:  # TR
            tiles.append([start[0] - 1, start[1] + 1])
    else:  # Black Pawn
        if start[0] + 1 <= 7 and start[1] - 1 >= 0:  # BL
            tiles.append([start[0] + 1, start[1] - 1])
        if start[0] + 1 <= 7 and start[1] + 1 <= 7:  # BR
            tiles.append([start[0] + 1, start[1] + 1])
    return tiles


def take_or_move(board, color, pos):
    piece = board[pos[0]][pos[1]]
    if piece is not None:  # Occupied Tile
        if piece.color != color:  # Enemy Piece
            if piece.is_king():  # Enemy King
                return False
            else:  # Can take piece
                return True
        else:  # Ally Piece
            if piece.name == "GP":
                return True
            else:
                return False
    else:  # Free Tile
        return True


def take(board, color, pos):
    piece = board[pos[0]][pos[1]]
    if piece is not None:  # Occupied Tile
        if piece.color != color:  # Enemy Piece
            if piece.is_king():  # Enemy King
                return False
            else:  # Can take piece
                return True
        else:  # Ally Piece
            return False
    else:  # Free Tile
        return False
