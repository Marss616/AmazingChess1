class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 'white'

    def create_board(self):
        return [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]

    def print_board(self):
        print("\n\n\n")
        print("---- \nWhite side \n----")
        print("  0 1 2 3 4 5 6 7")  # Column headers
        print("-------------------")
        for i, row in enumerate(self.board):
            print(f"{i}|{' '.join(row)}")  # Print row numbers on both sides
        print("---- \nBlack side \n----")
        

    def is_valid_move(self, start, end):
        sx, sy = start
        ex, ey = end
        piece = self.board[sx][sy]

        if piece == ".":
            return False
        
        if self.turn == 'white' and piece.islower():
            return False
        if self.turn == 'black' and piece.isupper():
            return False

        return True

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            self.board[ex][ey] = self.board[sx][sy]
            self.board[sx][sy] = "."
            self.turn = 'black' if self.turn == 'white' else 'white'
        else:
            print("Invalid move. Try again.")

    def play(self):
        while True:
            self.print_board()
            print(f"{self.turn.capitalize()}'s turn")
            try:
                start = tuple(map(int, input("Enter start position (row col): ").split()))
                end = tuple(map(int, input("Enter end position (row col): ").split()))
                self.move_piece(start, end)
            except ValueError:
                print("Invalid input. Enter numbers separated by spaces.")

game = ChessGame()
game.play()
