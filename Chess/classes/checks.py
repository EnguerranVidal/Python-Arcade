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
    if start[0] + 1 <= 7 and start[1] + 2 <= 7:  # RB
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


def up_diagonals(board, pos):
    left = [[pos[0], pos[1]]]
    right = [[pos[0], pos[1]]]
    while left[-1][0] > 0 and left[-1][1] > 0:
        left.append([left[-1][0] - 1, left[-1][1] - 1])
    while right[-1][0] > 0 and right[-1][1] < 7:
        right.append([right[-1][0] - 1, right[-1][1] + 1])
    left.pop(0)
    right.pop(0)
    pieces_left = []
    pieces_right = []
    for i in range(len(left)):
        pieces_left.append(board[left[i][0]][left[i][1]])
    for i in range(len(right)):
        pieces_right.append(board[right[i][0]][right[i][1]])
    return pieces_left, pieces_right


def down_diagonals(board, pos):
    left = [[pos[0], pos[1]]]
    right = [[pos[0], pos[1]]]
    while left[-1][0] < 7 and left[-1][1] > 0:
        left.append([left[-1][0] + 1, left[-1][1] - 1])
    while right[-1][0] < 7 and right[-1][1] < 7:
        right.append([right[-1][0] + 1, right[-1][1] + 1])
    left.pop(0)
    right.pop(0)
    pieces_left = []
    pieces_right = []
    for i in range(len(left)):
        pieces_left.append(board[left[i][0]][left[i][1]])
    for i in range(len(right)):
        pieces_right.append(board[right[i][0]][right[i][1]])
    return pieces_left, pieces_right


def left_right_row(board, pos):
    left = [[pos[0], pos[1]]]
    right = [[pos[0], pos[1]]]
    while left[-1][1] > 0:
        left.append([left[-1][0], left[-1][1] - 1])
    while right[-1][1] < 7:
        right.append([right[-1][0], right[-1][1] + 1])
    left.pop(0)
    right.pop(0)
    pieces_left = []
    pieces_right = []
    for i in range(len(left)):
        pieces_left.append(board[left[i][0]][left[i][1]])
    for i in range(len(right)):
        pieces_right.append(board[right[i][0]][right[i][1]])
    return pieces_left, pieces_right


def up_down_column(board, pos):
    up = [[pos[0], pos[1]]]
    down = [[pos[0], pos[1]]]
    while up[-1][0] > 0:
        up.append([up[-1][0] - 1, up[-1][1]])
    while down[-1][0] < 7:
        down.append([down[-1][0] + 1, down[-1][1]])
    up.pop(0)
    down.pop(0)
    pieces_up = []
    pieces_down = []
    for i in range(len(up)):
        pieces_up.append(board[up[i][0]][up[i][1]])
    for i in range(len(down)):
        pieces_down.append(board[down[i][0]][down[i][1]])
    return pieces_up, pieces_down


def knights(board, pos):
    destinations = knight_destinations(pos)
    pieces = []
    for i in range(len(destinations)):
        pieces.append(board[destinations[i][0]][destinations[i][1]])
    return pieces
