def search(d: dict):
    n, m = d['rows'], d['cols']
    grid = [[1 for i in range(m)] for j in range(n)]
    for x, y in d['obstacles']:
        grid[x][y] = 0
    goals = set([tuple(i) for i in d['goals']])
    visited = [[0 for i in range(m)] for j in range(n)]
    chx = [0, 0, 1, -1]
    chy = [1, -1, 0, 0]
    q = []
    if grid[d['start'][0]][d['start'][1]]:
        q.append(tuple(d['start']))
        visited[d['start'][0]][d['start'][1]] = 1
    while len(q) > 0:
        pos = q[-1]
        q.pop()
        if pos in goals:
            path = [pos]
            now = pos
            while now != 1:
                now = visited[now[0]][now[1]]
                path.append(now)
            path.pop()
            return path[::-1]
        for i in range(4):
            x = pos[0] + chx[i]
            y = pos[1] + chy[i]
            if x >= 0 and y >= 0 and x < n and y < m and grid[x][y] and visited[x][y] == 0:
                q.append((x, y))
                visited[x][y] = pos
    return []