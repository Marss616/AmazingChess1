class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 'white'
        self.king_moved = {'white': False, 'black': False}
        self.rook_moved = {'white': [False, False], 'black': [False, False]}
        self.kings_position = {'white': (0, 4), 'black': (7, 4)}

    def create_board(self):
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]


    def print_board(self):
        print("\n\n\n")
        print("---- \nBlack side \n----")
        print("  0 1 2 3 4 5 6 7")
        print("-------------------")
        for i, row in enumerate(self.board):
            print(f"{i}|{' '.join(row)}")
        print("---- \nWhite side \n----")

    def in_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def is_path_clear(self, sx, sy, ex, ey):
        dx = ex - sx
        dy = ey - sy
        step_x = (dx > 0) - (dx < 0)
        step_y = (dy > 0) - (dy < 0)

        x, y = sx + step_x, sy + step_y
        while (x, y) != (ex, ey):
            if self.board[x][y] != ".":
                return False
            x += step_x
            y += step_y
        return True

    def is_opponent_piece(self, piece, target):
        return (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())

    def is_valid_pawn(self, sx, sy, ex, ey, piece):
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        target = self.board[ex][ey]

        # Forward move
        if sy == ey:
            if self.board[ex][ey] == ".":
                if ex - sx == direction:
                    return True
                if sx == start_row and ex - sx == 2 * direction and self.board[sx + direction][sy] == ".":
                    return True
        # Diagonal capture
        elif abs(ey - sy) == 1 and ex - sx == direction:
            if target != "." and self.is_opponent_piece(piece, target):
                return True

        return False

    def is_valid_rook(self, sx, sy, ex, ey):
        return (sx == ex or sy == ey) and self.is_path_clear(sx, sy, ex, ey)

    def is_valid_bishop(self, sx, sy, ex, ey):
        return abs(sx - ex) == abs(sy - ey) and self.is_path_clear(sx, sy, ex, ey)

    def is_valid_knight(self, sx, sy, ex, ey):
        dx, dy = abs(ex - sx), abs(ey - sy)
        return (dx, dy) in [(2, 1), (1, 2)]

    def is_valid_queen(self, sx, sy, ex, ey):
        return self.is_valid_rook(sx, sy, ex, ey) or self.is_valid_bishop(sx, sy, ex, ey)

    def is_valid_king(self, sx, sy, ex, ey, color):
        if max(abs(sx - ex), abs(sy - ey)) == 1:
            return True
        if sx == ex and abs(ey - sy) == 2:
            return self.can_castle(color, sy < ey)
        return False

    def can_castle(self, color, kingside):
        row = 0 if color == 'white' else 7
        if self.king_moved[color]:
            return False
        rook_index = 1 if kingside else 0
        if self.rook_moved[color][rook_index]:
            return False
        if kingside:
            return self.board[row][5] == self.board[row][6] == "." and self.board[row][7].lower() == "r"
        else:
            return self.board[row][1] == self.board[row][2] == self.board[row][3] == "." and self.board[row][0].lower() == "r"

    def is_valid_move(self, start, end):
        sx, sy = start
        ex, ey = end

        if not self.in_bounds(sx, sy) or not self.in_bounds(ex, ey):
            return False

        piece = self.board[sx][sy]
        target = self.board[ex][ey]

        if piece == "." or start == end:
            return False

        if self.turn == 'white' and piece.islower():
            return False
        if self.turn == 'black' and piece.isupper():
            return False

        if target != "." and not self.is_opponent_piece(piece, target):
            return False

        pt = piece.lower()
        if pt == "p":
            return self.is_valid_pawn(sx, sy, ex, ey, piece)
        elif pt == "r":
            return self.is_valid_rook(sx, sy, ex, ey)
        elif pt == "n":
            return self.is_valid_knight(sx, sy, ex, ey)
        elif pt == "b":
            return self.is_valid_bishop(sx, sy, ex, ey)
        elif pt == "q":
            return self.is_valid_queen(sx, sy, ex, ey)
        elif pt == "k":
            return self.is_valid_king(sx, sy, ex, ey, self.turn)

        return False

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            piece = self.board[sx][sy]

            if piece.lower() == "k" and abs(ey - sy) == 2:
                self.handle_castling(sx, sy, ex, ey)
            else:
                self.board[ex][ey] = piece
                self.board[sx][sy] = "."
                if piece.lower() == 'k':
                    self.kings_position[self.turn] = (ex, ey)
                    self.king_moved[self.turn] = True
                elif piece.lower() == 'r':
                    if sy == 0:
                        self.rook_moved[self.turn][0] = True
                    elif sy == 7:
                        self.rook_moved[self.turn][1] = True
                if piece.lower() == 'p' and (ex == 0 or ex == 7):
                    self.board[ex][ey] = 'Q' if piece.isupper() else 'q'

            self.turn = 'black' if self.turn == 'white' else 'white'
            if self.in_check(self.turn):
                if self.is_checkmate(self.turn):
                    self.print_board()
                    print(f"Checkmate! {self.turn.capitalize()} loses.")
                    exit()
                else:
                    print(f"{self.turn.capitalize()} is in check!")
        else:
            print("Invalid move. Try again.")

    def handle_castling(self, sx, sy, ex, ey):
        if ey > sy:
            self.board[sx][6] = self.board[sx][4]
            self.board[sx][5] = self.board[sx][7]
            self.board[sx][4] = self.board[sx][7] = "."
        else:
            self.board[sx][2] = self.board[sx][4]
            self.board[sx][3] = self.board[sx][0]
            self.board[sx][4] = self.board[sx][0] = "."
        self.king_moved[self.turn] = True
        self.rook_moved[self.turn][0 if ey < sy else 1] = True
        self.kings_position[self.turn] = (sx, ey)

    def in_check(self, color):
        king_pos = self.kings_position[color]
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != "." and self.is_opponent_piece(self.board[king_pos[0]][king_pos[1]], self.board[x][y]):
                    if self.is_valid_move((x, y), king_pos):
                        return True
        return False

    def is_checkmate(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece == ".":
                    continue
                if (color == 'white' and piece.isupper()) or (color == 'black' and piece.islower()):
                    for i in range(8):
                        for j in range(8):
                            temp_board = [row[:] for row in self.board]
                            if self.is_valid_move((x, y), (i, j)):
                                self.board[i][j] = piece
                                self.board[x][y] = "."
                                if not self.in_check(color):
                                    self.board = temp_board
                                    return False
                                self.board = temp_board
        return True

    def play(self):
        while True:
            self.print_board()
            print(f"{self.turn.capitalize()}'s turn")
            try:
                start = tuple(map(int, input("Enter start position (row col): ").split()))
                end = tuple(map(int, input("Enter end position (row col): ").split()))
                self.move_piece(start, end)
            except ValueError:
                print("Invalid input. Enter two numbers separated by a space.")

if __name__ == "__main__":
    game = ChessGame()
    game.play()
