'''
This is the code template for Project 2.2 Task 2 (CSP).
You may remove or add any additional classes or methods you require.
'''
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Any

class Square:
    def __init__(self, x, y, size, n, m) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.n = n
        self.m = m

    def __lt__(self, other: Square):
        return self.size < other.size

    def assign(self, x, y):
        return Square(x, y, self.size, self.n, self.m)

class Board:
    def __init__(self, n, m) -> None:
        self.n = n
        self.m = m
        self.squares = []
        self.chosen = {}
        self.domains = {}
        self.sizes = {}
        self.visited = set()

    def ans(self):
        return [(s.size, s.x, s.y) for s in self.squares]
    
    def find_corner(self, pair):
        x, y = pair
        return x + y

    def state(self):
        res = []
        for s in self.squares:
            if s.x is not None:
                res.append((s.size, s.x, s.y))
        res.sort()
        return tuple(res)
    
    def set_domains(self, obstacles):
        for s in self.squares:
            if s.size not in self.sizes:
                self.sizes[s.size] = 0
            self.sizes[s.size] += 1
        for s in self.sizes:
            self.domains[s] = []
        for size in self.domains:
            viable = [[1 for i in range(self.m)] for j in range(self.n)]
            for x, y in obstacles:
                for i in range(x - size + 1, x + 1):
                    for j in range(y - size + 1, y + 1):
                        if 0 <= i < self.n and 0 <= j < self.m:
                            viable[i][j] = 0
            for i in range(self.n - size + 1):
                for j in range(self.m - size + 1):
                    if viable[i][j]:
                        self.domains[size].append((i, j))
        for s in self.sizes:
            self.domains[s].sort()
    
    def forward_checking(self, size):
        for s in self.sizes:
            if s <= size and len(self.domains[s]) < self.sizes[s] - self.chosen.get(s, 0):
                return True
        return False
    
    def prune(self, other: Square):
        changed = {}
        for size in self.sizes:
            if size > other.size:
                continue
            blocked = set()
            for i in range(other.x - size + 1, other.x + other.size):
                for j in range(other.y - size + 1, other.y + other.size):
                    if 0 <= i < self.n and 0 <= j < self.m:
                        blocked.add((i, j))
            new_domain = []
            changed[size] = self.domains[size]
            for d in self.domains[size]:
                if d not in blocked:
                    new_domain.append(d)
            self.domains[size] = new_domain
        return changed
    
    def revert(self, changed):
        for i in changed:
            self.domains[i] = changed[i]

    def search(self):
        def dfs(i):
            if i == len(self.squares):
                return True
            sq: Square = self.squares[i]
            if self.forward_checking(sq.size):
                return False
            if sq.size not in self.chosen:
                self.chosen[sq.size] = 0
            self.chosen[sq.size] += 1
            for x, y in self.domains[sq.size]:
                assigned_sq = sq.assign(x, y)
                self.squares[i] = assigned_sq
                state = self.state()
                if state in self.visited:
                    continue
                changed = self.prune(assigned_sq)
                if dfs(i + 1):
                    return True
                else:
                    if len(state) > 0:
                        self.visited.add(state)
                self.revert(changed)
            self.chosen[sq.size] -= 1
            return False
        if dfs(0):
            return self.ans()

def solve_CSP(d : Dict[str : Any]) -> List[Tuple[int, int, int]]:
    n = d['rows']
    m = d['cols']
    input_squares = d['input_squares']
    obstacles = set(d['obstacles'])
    board = Board(n, m)
    for size in input_squares:
        for _ in range(input_squares[size]):
            board.squares.append(Square(None, None, size, n, m))
    board.squares.sort(reverse=True)
    board.set_domains(obstacles)
    return board.search()
