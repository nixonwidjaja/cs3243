from collections import deque
 
def search(d: dict):
    n, m = d['rows'], d['cols']
    grid = [[1 for i in range(m)] for j in range(n)]
    for x, y in d['obstacles']:
        grid[x][y] = 0
    goals = set([tuple(i) for i in d['goals']])
    visited = [[0 for i in range(m)] for j in range(n)]
    chx = [-1, 1, 0, 0]
    chy = [0, 0, -1, 1]
    q = deque()
    if grid[d['start'][0]][d['start'][1]]:
        q.append((tuple(d['start']), []))
        visited[d['start'][0]][d['start'][1]] = 1
    while len(q) > 0:
        pos, path = q[0]
        q.popleft()
        if pos in goals:
            return path
        for i in range(4):
            x = pos[0] + chx[i]
            y = pos[1] + chy[i]
            if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] and visited[x][y] == 0:
                new_path = path.copy()
                new_path.append(i)
                q.append(((x, y), new_path))
                visited[x][y] = 1
    return []
# import json
# with open('0.json', 'r') as f:
#     d = json.load(f)
#     print(search(d))
# with open('1.json', 'r') as f:
#     d = json.load(f)
#     print(search(d))
# with open('2.json', 'r') as f:
#     d = json.load(f)
#     print(search(d))