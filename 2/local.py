'''
This is the code template for Project 2.2 Task 1 (Local search).
You may remove or add any additional classes or methods you require.
'''
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Any
from random import randint

chx = [0,0,1,-1] # 0R 1L 2D 3U 
chy = [1,-1,0,0]

class Square:
    def __init__(self, x1, y1, size) -> None:
        self.x1 = x1
        self.y1 = y1
        self.size = size
        self.x2 = x1 + size
        self.y2 = y1 + size

    def move(self, dir):
        sq = Square(self.x1 + chx[dir], self.y1 + chy[dir], self.size)
        return sq
    
    def __str__(self) -> str:
        return f"x1 {self.x1} y1 {self.y1} size {self.size} x2 {self.x2-1} y2 {self.y2-1}"

class Board:
    def __init__(self, n, m) -> None:
        self.n = n
        self.m = m
        self.squares = []
        self.state = [[0 for i in range(m)] for j in range(n)]
        self.heur = n * m
        self.visited = {}
        self.ones = 0

    def add(self, sq: Square):
        self.squares.append(sq)
        for i in range(sq.x1, sq.x2):
            for j in range(sq.y1, sq.y2):
                self.state[i][j] += 1

    def ans(self):
        res = [(s.size, s.x1, s.y1) for s in self.squares]
        for i in range(self.n):
            for j in range(self.m):
                if self.state[i][j] == 0:
                    res.append((1, i, j))
        return res
    
    def fill(self, size):
        res = []
        for i in range(0, self.n, size):
            for j in range(0, self.m, size):
                res.append((size, i, j))
        return res
    
    def update_heuristic(self):
        ans = 0
        for i in range(self.n):
            for j in range(self.m):
                ans += abs(self.state[i][j] - 1)
        self.heur = ans
    
    def move(self, heur, idx, dir):
        sq: Square = self.squares[idx]
        if dir == 0:
            R = sq.y2
            L = sq.y1
            for i in range(sq.x1, sq.x2):
                self.state[i][R] += 1
                self.state[i][L] -= 1
        elif dir == 1:
            R = sq.y2 - 1
            L = sq.y1 - 1
            for i in range(sq.x1, sq.x2):
                self.state[i][R] -= 1
                self.state[i][L] += 1
        elif dir == 2:
            U = sq.x1
            D = sq.x2
            for j in range(sq.y1, sq.y2):
                self.state[U][j] -= 1
                self.state[D][j] += 1
        elif dir == 3:
            U = sq.x1 - 1
            D = sq.x2 - 1
            for j in range(sq.y1, sq.y2):
                self.state[U][j] += 1
                self.state[D][j] -= 1
        self.squares[idx] = sq.move(dir)
        self.heur = heur

    def check_heur(self, idx, dir):
        ans = 0
        grid = [[0 for i in range(self.m)] for j in range(self.n)]
        for id, sq in enumerate(self.squares):
            if id == idx:
                sq = sq.move(dir)
            for i in range(sq.x1, sq.x2):
                for j in range(sq.y1, sq.y2):
                    grid[i][j] += 1
        for i in grid:
            for j in i:
                ans += abs(j - 1)
        return ans

    def heuristic(self, idx, dir) -> int:
        sq: Square = self.squares[idx]
        diff = 0
        if dir == 0:
            R = sq.y2
            L = sq.y1
            for i in range(sq.x1, sq.x2):
                diff += abs(self.state[i][R]) - abs(self.state[i][R] - 1)
                diff += abs(self.state[i][L] - 2) - abs(self.state[i][L] - 1)
        elif dir == 1:
            R = sq.y2 - 1
            L = sq.y1 - 1
            for i in range(sq.x1, sq.x2):
                diff += abs(self.state[i][R] - 2) - abs(self.state[i][R] - 1)
                diff += abs(self.state[i][L]) - abs(self.state[i][L] - 1)
        elif dir == 2:
            U = sq.x1
            D = sq.x2
            for j in range(sq.y1, sq.y2):
                diff += abs(self.state[U][j] - 2) - abs(self.state[U][j] - 1)
                diff += abs(self.state[D][j]) - abs(self.state[D][j] - 1)
        elif dir == 3:
            U = sq.x1 - 1
            D = sq.x2 - 1
            for j in range(sq.y1, sq.y2):
                diff += abs(self.state[U][j]) - abs(self.state[U][j] - 1)
                diff += abs(self.state[D][j] - 2) - abs(self.state[D][j] - 1)
        return self.heur + diff

    def try_all(self):
        res = []
        for i in range(len(self.squares)):
            sq: Square = self.squares[i]
            for dir in range(4):
                if sq.x1 + chx[dir] >= 0 and sq.y1 + chy[dir] >= 0 and \
                sq.x2 - 1 + chx[dir] < self.n and sq.y2 - 1 + chy[dir] < self.m:
                    res.append((self.heuristic(i, dir), i, dir))
        res.sort(key=lambda x: x[0])
        heur, i, dir = res[0]
        if heur > self.heur:
            return None
        if heur == self.heur: # sidemove
            if heur not in self.visited:
                self.visited[heur] = set()
            j = 0
            while j < len(res) and res[j][0] == heur:
                _, i, dir = res[j]
                sq = self.squares[i]
                if (i, sq.x1 + chx[dir], sq.x2 + chy[dir]) not in self.visited[heur]:
                    self.visited[heur].add((i, sq.x1 + chx[dir], sq.x2 + chy[dir]))
                    return heur, i, dir
                j += 1
            return None
        return heur, i, dir

    def search(self):
        if self.heur == self.ones:
            return True
        for _ in range(self.n * self.m * len(self.squares)):
            if self.heur == self.ones:
                return True
            res = self.try_all()
            if not res:
                return False
            heur, i, dir = res
            self.move(heur, i, dir)

def run_local(d : Dict[str : Any]) -> List[Tuple[int, int, int]]:
    n = d['height']
    m = d['width']
    squares = d['input_squares']
    while True:
        board = Board(n, m)
        for size in squares:
            if len(squares) == 1:
                return board.fill(size)
            if size == 1:
                board.ones = squares[size]
                continue
            for _ in range(squares[size]):
                x = randint(0, n - size)
                y = randint(0, m - size)
                board.add(Square(x, y, size))
        board.update_heuristic()
        if board.search():
            return board.ans()

