import heapq
 
class State:
    def __init__(self, x, y, path, flash, is_flash_active, is_inv, hp, dir, heur) -> None:
        self.x = x
        self.y = y
        self.path = path
        self.flash = flash
        self.is_flash_active = is_flash_active
        self.is_inv = is_inv
        self.hp = hp
        self.dir = dir
        self.heur = heur
 
    def __lt__(self, nxt):
        return self.hp + self.heur < nxt.hp + nxt.heur
 
def calculate_max_creep(grid):
    ans = 0
    for i in grid:
        ans = max(ans, max(i))
    return ans
 
def get_min_d(x, y, goals):
    distances = []
    for g in goals:
        distances.append(abs(g[0] - x) + abs(g[1] - y))
    return min(distances)
 
def num_creeps(grid, x, y, is_inv, max_creep):
    if is_inv:
        return max_creep - grid[x][y]
    return grid[x][y]
 
def visited_idx(pos: State):
    return (pos.x, pos.y, pos.flash, pos.is_flash_active, pos.is_inv)
 
def search(d: dict):
    n, m = d['rows'], d['cols']
    grid = [[0 for i in range(m)] for j in range(n)]
    for x, y, c in d['creeps']:
        grid[x][y] = c
    for x, y in d['obstacles']:
        grid[x][y] = -1
    goals = set([tuple(i) for i in d['goals']])
    flash = d['num_flash_left']
    visited = {}
    chx = [-1, 1, 0, 0]
    chy = [0, 0, -1, 1]
    max_creep = calculate_max_creep(grid)
    q = []
    heapq.heapify(q)
    x_start, y_start = d['start']
    if grid[x_start][y_start] != -1:
        init = State(x_start, y_start, [], flash, 0, 0, grid[x_start][y_start], 0, get_min_d(x_start, y_start, goals))
        heapq.heappush(q, init)
        visited[visited_idx(init)] = init.hp
    while len(q) > 0:
        pos: State = heapq.heappop(q)
        if pos.is_flash_active: #HANDLE FLASH ON
            x = pos.x + chx[pos.dir]
            y = pos.y + chy[pos.dir]
            if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != -1: # GO AHEAD
                new_hp = pos.hp + 2
                next_state = State(x, y, pos.path, pos.flash, 1, pos.is_inv, new_hp, pos.dir, get_min_d(x, y, goals))
                heapq.heappush(q, next_state)
            else: # CAN'T MOVE FURTHER
                new_hp = pos.hp + num_creeps(grid, pos.x, pos.y, pos.is_inv, max_creep)
                next_state = State(pos.x, pos.y, pos.path, pos.flash, 0, pos.is_inv, new_hp, pos.dir, get_min_d(x, y, goals))
                if visited_idx(next_state) not in visited or new_hp < visited[visited_idx(next_state)]: 
                    heapq.heappush(q, next_state)
                    visited[visited_idx(next_state)] = new_hp
            continue
        if (pos.x, pos.y) in goals:
            return pos.path
        for i in range(4):
            x = pos.x + chx[i]
            y = pos.y + chy[i]
            if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != -1:
                new_hp = pos.hp + 4 + num_creeps(grid, x, y, pos.is_inv, max_creep)
                new_path = pos.path.copy()
                new_path.append(i)
                next_state = State(x, y, new_path, pos.flash, 0, pos.is_inv, new_hp, i, get_min_d(x, y, goals))
                if visited_idx(next_state) not in visited or new_hp < visited[visited_idx(next_state)]: 
                    heapq.heappush(q, next_state)
                    visited[visited_idx(next_state)] = new_hp
        if pos.is_inv == 0: # INVERSION
            for i in range(4):
                x = pos.x + chx[i]
                y = pos.y + chy[i]
                if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != -1:
                    new_hp = pos.hp + 4 + num_creeps(grid, x, y, 1, max_creep)
                    new_path = pos.path.copy()
                    new_path.append(5)
                    new_path.append(i)
                    next_state = State(x, y, new_path, pos.flash, 0, 1, new_hp, i, get_min_d(x, y, goals))
                    if visited_idx(next_state) not in visited or new_hp < visited[visited_idx(next_state)]: 
                        heapq.heappush(q, next_state)
                        visited[visited_idx(next_state)] = new_hp
        if pos.flash > 0 and not pos.is_flash_active: # TURN ON FLASH
            for i in range(4):
                x = pos.x + chx[i]
                y = pos.y + chy[i]
                if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] != -1:
                    new_hp = pos.hp + 12
                    new_path = pos.path.copy()
                    new_path.append(4)
                    new_path.append(i)
                    next_state = State(x, y, new_path, pos.flash - 1, 1, pos.is_inv, new_hp, i, get_min_d(x, y, goals))
                    if visited_idx(next_state) not in visited or new_hp < visited[visited_idx(next_state)]: 
                        heapq.heappush(q, next_state)
                        visited[visited_idx(next_state)] = new_hp
    return []
