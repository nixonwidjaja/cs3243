from __future__ import annotations
from typing import List, Tuple

class Board:
    def __init__(self, other) -> None:
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.heur = 0
        self.is_end = False
        self.past_heur = None
        self.weight = {
            'King': 1000,
            'Rook': 20,
            'Bishop': 15,
            'Knight': 10,
            'Squire': 5,
            'Combatant': 2
        }
        self.whites = { # (x, y)
            'King': set(),
            'Rook': set(),
            'Bishop': set(),
            'Knight': set(),
            'Squire': set(),
            'Combatant': set()
        }
        self.blacks = { # (x, y)
            'King': set(),
            'Rook': set(),
            'Bishop': set(),
            'Knight': set(),
            'Squire': set(),
            'Combatant': set()
        }
        for p, c, pos in other:
            i, j = pos
            if c == 'white':
                self.board[i][j] = (p, 'W')
                self.heur += self.weight[p]
                self.whites[p].add((i, j))
            else:
                self.board[i][j] = (p, 'B')
                self.heur -= self.weight[p]
                self.blacks[p].add((i, j))

    def next_move(self, move):
        oldx, oldy = move[0]
        newx, newy = move[1]
        piece, color = self.board[oldx][oldy]
        is_terminated = False
        removed_piece, removed_color = None, None
        if self.board[newx][newy] != 0:
            removed_piece, removed_color = self.board[newx][newy]
            if removed_piece == 'King':
                is_terminated = True
                self.is_end = True
                self.past_heur = self.heur
            if removed_color == 'W':
                self.heur -= self.weight[self.board[newx][newy][0]]
                self.whites[removed_piece].remove((newx, newy))
                if self.board[newx][newy][0] == 'King':
                    self.heur = -10000
            else:
                self.heur += self.weight[self.board[newx][newy][0]]
                self.blacks[removed_piece].remove((newx, newy))
                if self.board[newx][newy][0] == 'King':
                    self.heur = 10000
        self.board[newx][newy] = (piece, color)
        self.board[oldx][oldy] = 0
        if color == 'W':
            self.whites[piece].remove((oldx, oldy))
            self.whites[piece].add((newx, newy))
        else:
            self.blacks[piece].remove((oldx, oldy))
            self.blacks[piece].add((newx, newy))
        return is_terminated, removed_piece, removed_color
    
    def undo_move(self, move, removed_piece, removed_color):
        oldx, oldy = move[0]
        newx, newy = move[1]
        piece, color = self.board[newx][newy]
        self.board[oldx][oldy] = (piece, color)
        if color == 'W':
            self.whites[piece].remove((newx, newy))
            self.whites[piece].add((oldx, oldy))
        else:
            self.blacks[piece].remove((newx, newy))
            self.blacks[piece].add((oldx, oldy))
        if removed_piece is None:
            self.board[newx][newy] = 0
        else:
            self.board[newx][newy] = (removed_piece, removed_color)
            if removed_color == 'W':
                self.heur += self.weight[removed_piece]
                self.whites[removed_piece].add((newx, newy))
            else:
                self.heur -= self.weight[removed_piece]
                self.blacks[removed_piece].add((newx, newy))
            if removed_piece == 'King':
                self.heur = self.past_heur
        self.is_end = False
    
    def move_all(self, color):
        ans = []
        order = ['Combatant', 'Squire', 'Knight', 'Bishop', 'Rook', 'King']
        for p in order:
            if color == 'W':
                for i, j in self.whites[p]:
                    ans.extend(self.move(p, color, i, j))
            else:
                for i, j in self.blacks[p]:
                    ans.extend(self.move(p, color, i, j))
        def f(x):
            if self.board[x[1][0]][x[1][1]] != 0:
                return self.weight.get(self.board[x[1][0]][x[1][1]][0], 0)
            return 0
        ans.sort(key=f, reverse=True)
        return ans

    def move(self, piece, color, x, y):
        ans = []

        def add_board(newx, newy):
            ans.append(((x, y), (newx, newy)))
                       
        if piece == 'King':
            chx = [0,0,1,1,1,-1,-1,-1]
            chy = [1,-1,1,0,-1,1,0,-1]
            for i in range(8):
                newx = x + chx[i]
                newy = y + chy[i]
                if newx >= 0 and newx < 8 and newy >= 0 and newy < 8:
                    if self.board[newx][newy] == 0 or self.board[newx][newy][1] != color:
                        add_board(newx, newy)

        elif piece == 'Rook':
            for newx in range(x + 1, 8):
                if self.board[newx][y] == 0:
                    add_board(newx, y)
                elif self.board[newx][y][1] == color:
                    break
                elif self.board[newx][y][1] != color:
                    add_board(newx, y)
                    break
            for newx in range(x - 1, -1, -1):
                if self.board[newx][y] == 0:
                    add_board(newx, y)
                elif self.board[newx][y][1] == color:
                    break
                elif self.board[newx][y][1] != color:
                    add_board(newx, y)
                    break
            for newy in range(y + 1, 8):
                if self.board[x][newy] == 0:
                    add_board(x, newy)
                elif self.board[x][newy][1] == color:
                    break
                elif self.board[x][newy][1] != color:
                    add_board(x, newy)
                    break
            for newy in range(y - 1, -1, -1):
                if self.board[x][newy] == 0:
                    add_board(x, newy)
                elif self.board[x][newy][1] == color:
                    break
                elif self.board[x][newy][1] != color:
                    add_board(x, newy)
                    break

        elif piece == 'Bishop':
            chx = [1, 1, -1, -1]
            chy = [1, -1, 1, -1]
            for i in range(4):
                for j in range(1, 8):
                    newx = x + chx[i] * j
                    newy = y + chy[i] * j
                    if newx >= 0 and newx < 8 and newy >= 0 and newy < 8:
                        if self.board[newx][newy] == 0:
                            add_board(newx, newy)
                        elif self.board[newx][newy][1] == color:
                            break
                        elif self.board[newx][newy][1] != color:
                            add_board(newx, newy)
                            break

        elif piece == 'Knight':
            chx = [1,2,2,1,-1,-2,-2,-1]
            chy = [2,1,-1,-2,-2,-1,1,2]
            for i in range(8):
                newx = x + chx[i]
                newy = y + chy[i]
                if newx >= 0 and newx < 8 and newy >= 0 and newy < 8:
                    if self.board[newx][newy] == 0 or self.board[newx][newy][1] != color:
                        add_board(newx, newy)

        elif piece == 'Squire':
            chx = [0,1,2,1,0,-1,-2,-1]
            chy = [2,1,0,-1,-2,-1,0,1]
            for i in range(8):
                newx = x + chx[i]
                newy = y + chy[i]
                if newx >= 0 and newx < 8 and newy >= 0 and newy < 8:
                    if self.board[newx][newy] == 0 or self.board[newx][newy][1] != color:
                        add_board(newx, newy)

        elif piece == 'Combatant': 
            chx = [0,0,1,-1]
            chy = [1,-1,0,0]
            for i in range(4):
                newx = x + chx[i]
                newy = y + chy[i]
                if newx >= 0 and newx < 8 and newy >= 0 and newy < 8 and self.board[newx][newy] == 0:
                    add_board(newx, newy)
            chx = [1,1,-1,-1]
            chy = [1,-1,-1,1]
            for i in range(4):
                newx = x + chx[i]
                newy = y + chy[i]
                if newx >= 0 and newx < 8 and newy >= 0 and newy < 8 and self.board[newx][newy] != 0 \
                and self.board[newx][newy][1] != color:
                    add_board(newx, newy)
        return ans

def studentAgent(gameboard : List[Tuple[str, str, Tuple[int, int]]]) -> Tuple[Tuple[int, int], Tuple[int, int]]: 
    board = Board(gameboard)
    return ab(board, 0, 'W', -1e9, 1e9)[1]

def ab(board: Board, depth, color, a, b):
    if depth == 5 or board.is_end:
        return board.heur, None
    moves = board.move_all(color)
    if color == 'W':
        val = -1e9
        best_move = None
        for m in moves:
            is_terminated, removed_piece, removed_color = board.next_move(m)
            if is_terminated:
                final_heur = board.heur
                board.undo_move(m, removed_piece, removed_color)
                return (final_heur, m if depth == 0 else None)
            new_val, _ = ab(board, depth + 1, 'B', a, b)
            board.undo_move(m, removed_piece, removed_color)
            if new_val > val:
                val = new_val
                best_move = m
            a = max(a, new_val)
            if a >= b:
                break
        return val, best_move
    else:
        val = 1e9
        best_move = None
        for m in moves:
            is_terminated, removed_piece, removed_color = board.next_move(m)
            if is_terminated:
                final_heur = board.heur
                board.undo_move(m, removed_piece, removed_color)
                return (final_heur, m if depth == 0 else None)
            new_val, _ = ab(board, depth + 1, 'W', a, b)
            board.undo_move(m, removed_piece, removed_color)
            if new_val < val:
                val = new_val
                best_move = m
            b = min(b, new_val)
            if b <= a:
                break
        return val, best_move
