from collections import deque

class State:
    def __init__(self, x, y, path, flash, is_flash_active, is_inv, hp) -> None:
        self.x = x
        self.y = y
        self.path = path
        self.flash = flash
        self.is_flash_active = is_flash_active
        self.is_inv = is_inv
        self.hp = hp

def search(d: dict):
    n, m = d['rows'], d['cols']
    grid = [[0 for i in range(m)] for j in range(n)]
    for x, y in d['obstacles']:
        grid[x][y] = -1
    goals = set([tuple(i) for i in d['goals']])
    visited = [[1e9 for i in range(m)] for j in range(n)]
    chx = [-1, 1, 0, 0]
    chy = [0, 0, -1, 1]
    q = deque()
    if grid[d['start'][0]][d['start'][1]] != -1:
        q.append(State(d['start'][0], d['start'][1], [], 0, 0, 0, 0))
        visited[d['start'][0]][d['start'][1]] = 0
    while len(q) > 0:
        pos: State = q[0]
        q.popleft()
        if (pos.x, pos.y) in goals:
            return pos.path
        for i in range(4):
            x = pos.x + chx[i]
            y = pos.y + chy[i]
            if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != -1:
                new_hp = pos.hp + 1
                if new_hp < visited[x][y]:
                    new_path = pos.path.copy()
                    new_path.append(i)
                    q.append(State(x, y, new_path, 0, 0, 0, new_hp))
                    visited[x][y] = 1
    return []
