from lib import *

TOPIC(
    id="graphs", title="Graphs", glyph="●—●",
    blurb="BFS, DFS, topological sort, union-find and shortest paths — on grids and on adjacency lists.",
    demo_title="BFS spreads one layer at a time; that's why it finds shortest paths",
    theory="""
<h3>What it is</h3>
<p>A <b>graph</b> is a set of nodes connected by edges. Edges may be <b>directed</b> (course prerequisites) or undirected (friendships), and may carry <b>weights</b> (travel time). A grid is a graph too: each cell is a node joined to its 4 (or 8) neighbours.</p>
<pre><code class="py">from collections import defaultdict
graph = defaultdict(list)          # adjacency list
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)             # omit for directed graphs</code></pre>
<h3>Which algorithm?</h3>
<table>
<tr><th>Question</th><th>Tool</th><th>Cost</th></tr>
<tr><td>Visit everything / count components / flood fill</td><td>DFS or BFS with a visited set</td><td>O(V + E)</td></tr>
<tr><td>Shortest path, every edge costs 1</td><td><b>BFS</b> (multi-source: start with all sources in the queue)</td><td>O(V + E)</td></tr>
<tr><td>Shortest path, non-negative weights</td><td><b>Dijkstra</b> with a min-heap</td><td>O(E log V)</td></tr>
<tr><td>Shortest path with ≤ k edges or negative weights</td><td><b>Bellman–Ford</b> (k rounds of relaxing every edge)</td><td>O(k · E)</td></tr>
<tr><td>Order tasks with prerequisites / detect a cycle in a directed graph</td><td><b>Topological sort</b> (Kahn's BFS on in-degrees)</td><td>O(V + E)</td></tr>
<tr><td>"Are these connected?" while edges are added</td><td><b>Union–Find</b> with path compression</td><td>≈ O(1) per op</td></tr>
<tr><td>Cheapest way to connect everything</td><td><b>Minimum spanning tree</b> — Prim or Kruskal</td><td>O(E log V)</td></tr>
</table>
<h3>Template: BFS on a grid</h3>
<pre><code class="py">from collections import deque
q = deque([(sr, sc)]); seen = {(sr, sc)}; steps = 0
while q:
    for _ in range(len(q)):            # one layer = one step
        r, c = q.popleft()
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if 0 &lt;= nr &lt; m and 0 &lt;= nc &lt; n and (nr, nc) not in seen and grid[nr][nc] != WALL:
                seen.add((nr, nc)); q.append((nr, nc))
    steps += 1</code></pre>
<h3>Spot the pattern</h3>
<ul>
<li>"Number of islands / provinces / groups" → count how many times you start a fresh DFS.</li>
<li>"Minimum minutes / steps / distance" on an unweighted grid → BFS by layers.</li>
<li>"Regions not connected to the border" → start the search <b>from the border</b> instead.</li>
<li>"Prerequisites / ordering / can all be finished" → topological sort.</li>
<li>"Merge groups that share something" → union–find.</li>
</ul>
<h3>Common mistakes</h3>
<ul>
<li>Marking a node visited when you <i>pop</i> it instead of when you <i>push</i> it — the same node enters the queue many times.</li>
<li>Using DFS for shortest paths in unweighted graphs (it finds <i>a</i> path, not the shortest).</li>
<li>Dijkstra: not skipping stale heap entries (<code>if d &gt; dist[u]: continue</code>).</li>
</ul>
""")

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@D
def bfs_demo():
    from collections import deque
    n = 7
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 6)]
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = {0: 0}
    q = deque([0])
    while q:
        layer = list(q)
        T(f"Layer at distance {dist[layer[0]]}: {layer}", GR("graph", n, edges, hl=layer, ok=[x for x in dist if x not in layer]), M("distance", dist))
        for _ in range(len(q)):
            u = q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
    return dist


# 1 ---------------------------------------------------------------
Q(200, "Number of Islands", "Medium", "DFS flood fill",
  "Count the islands ('1' cells connected up/down/left/right) in a grid of '1' and '0'.",
  [(([["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]],), 1),
   (([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],), 3)],
  ("For each land cell, BFS from scratch to see whether it reaches any earlier land cell; if not, it starts a new island.", "O((m·n)²)", "O(m·n)"),
  ("Scan the grid; each unvisited '1' starts a new island. Flood-fill it (sink it to '0') so it is never counted again.", "O(m·n)", "O(m·n) recursion"),
  viz=([["1", "1", "0", "0", "1"], ["1", "0", "0", "1", "1"], ["0", "0", "1", "0", "0"], ["1", "0", "0", "0", "1"]],))


@B
def num_islands(grid):
    from collections import deque
    m, n = len(grid), len(grid[0])
    land = [(r, c) for r in range(m) for c in range(n) if grid[r][c] == "1"]
    count = 0
    for k, (r, c) in enumerate(land):
        earlier = set(land[:k])
        seen, q, joined = {(r, c)}, deque([(r, c)]), False
        while q and not joined:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1" and (nx, ny) not in seen:
                    if (nx, ny) in earlier:
                        joined = True
                    seen.add((nx, ny))
                    q.append((nx, ny))
        count += not joined
    return count


@O
def num_islands(grid):
    m, n = len(grid), len(grid[0])
    sunk = []

    def sink(r, c):
        if not (0 <= r < m and 0 <= c < n) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sunk.append((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sink(r + dr, c + dc)

    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1":
                count += 1
                start = len(sunk)
                sink(r, c)
                T(f"New island #{count} at ({r},{c}) — flood it so it's not counted again", G("grid", grid, ok=sunk[:start], hl=sunk[start:]), V(islands=count), at="prev")
    return count


# 2 ---------------------------------------------------------------
Q(733, "Flood Fill", "Easy", "DFS from the start pixel",
  "Recolour the region of same-coloured pixels connected to <code>(sr, sc)</code> with <code>color</code>.",
  [(([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), [[2, 2, 2], [2, 2, 0], [2, 0, 1]]), (([[0, 0, 0], [0, 0, 0]], 0, 0, 0), [[0, 0, 0], [0, 0, 0]])],
  ("Recolour the start, then keep sweeping the whole image recolouring any original-coloured pixel next to a recoloured one, until nothing changes.", "O((m·n)²)", "O(m·n)"),
  ("DFS from (sr, sc) recolouring pixels of the original colour. If the new colour equals the old one, return immediately.", "O(m·n)", "O(m·n)"))


@B
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    m, n = len(image), len(image[0])
    done = {(sr, sc)}
    changed = True
    while changed:
        changed = False
        for r in range(m):
            for c in range(n):
                if (r, c) not in done and image[r][c] == old and any((r + dr, c + dc) in done for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    done.add((r, c))
                    changed = True
    for r, c in done:
        image[r][c] = color
    return image


@O
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    m, n = len(image), len(image[0])

    def dfs(r, c):
        if not (0 <= r < m and 0 <= c < n) or image[r][c] != old:
            return
        image[r][c] = color
        T(f"Paint ({r},{c})", G("image", image, hl=[(r, c)]), at="prev")
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    dfs(sr, sc)
    return image


# 3 ---------------------------------------------------------------
Q(695, "Max Area of Island", "Medium", "DFS returning area",
  "Return the area of the largest island (connected 1s) in a binary grid, or 0.",
  [(([[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]],), 6),
   (([[0, 0, 0, 0, 0, 0, 0, 0]],), 0)],
  ("From every land cell, BFS its whole island from scratch to measure it.", "O((m·n)²)", "O(m·n)"),
  ("DFS from each unvisited land cell, sinking cells and returning 1 + the areas of the neighbours.", "O(m·n)", "O(m·n)"),
  viz=([[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1], [0, 1, 1, 1]],))


@B
def max_area_of_island(grid):
    from collections import deque
    m, n, best = len(grid), len(grid[0]), 0
    for r in range(m):
        for c in range(n):
            if grid[r][c]:
                seen, q = {(r, c)}, deque([(r, c)])
                while q:
                    x, y = q.popleft()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            q.append((nx, ny))
                best = max(best, len(seen))
    return best


@O
def max_area_of_island(grid):
    m, n = len(grid), len(grid[0])

    def area(r, c):
        if not (0 <= r < m and 0 <= c < n) or grid[r][c] != 1:
            return 0
        grid[r][c] = 2
        return 1 + sum(area(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                a = area(r, c)
                best = max(best, a)
                T(f"Island from ({r},{c}) has area {a}", G("grid (2 = visited)", grid, hl=[(i, j) for i in range(m) for j in range(n) if grid[i][j] == 2]), V(best=best), at="prev")
    return best


# 4 ---------------------------------------------------------------
Q(994, "Rotting Oranges", "Medium", "Multi-source BFS",
  "Each minute, rotten oranges (2) rot their fresh neighbours (1). Return the minutes until none are fresh, or −1.",
  [(([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4), (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1), (([[0, 2]],), 0)],
  ("Simulate minute by minute, scanning the whole grid each minute.", "O((m·n)²)", "O(m·n)"),
  ("Put every rotten orange in the queue at once and BFS layer by layer; each layer is one minute. Count fresh oranges to detect −1.", "O(m·n)", "O(m·n)"))


@B
def oranges_rotting(grid):
    m, n, minutes = len(grid), len(grid[0]), 0
    while True:
        new = [(r, c) for r in range(m) for c in range(n) if grid[r][c] == 1 and any(0 <= r + dr < m and 0 <= c + dc < n and grid[r + dr][c + dc] == 2 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        if not new:
            break
        for r, c in new:
            grid[r][c] = 2
        minutes += 1
    return -1 if any(1 in row for row in grid) else minutes


@O
def oranges_rotting(grid):
    from collections import deque
    m, n = len(grid), len(grid[0])
    q = deque((r, c) for r in range(m) for c in range(n) if grid[r][c] == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    T("Minute 0: all rotten oranges start in the queue", G("grid", grid, bad=list(q)), V(fresh=fresh))
    while q and fresh:
        layer = []
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    layer.append((nr, nc))
        minutes += 1
        T(f"Minute {minutes}: {len(layer)} orange(s) rot", G("grid", grid, bad=layer), V(fresh=fresh, minutes=minutes), at="prev")
    return -1 if fresh else minutes


# 5 ---------------------------------------------------------------
Q(542, "01 Matrix", "Medium", "Multi-source BFS from zeros",
  "Return a matrix of each cell's distance to the nearest 0.",
  [(([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), [[0, 0, 0], [0, 1, 0], [0, 0, 0]]), (([[0, 0, 0], [0, 1, 0], [1, 1, 1]],), [[0, 0, 0], [0, 1, 0], [1, 2, 1]])],
  ("BFS from every 1 to its nearest 0 separately.", "O((m·n)²)", "O(m·n)"),
  ("Start BFS from all zeros at once. The first time a cell is reached gives its shortest distance.", "O(m·n)", "O(m·n)"),
  viz=([[0, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 1]],))


@B
def update_matrix(mat):
    from collections import deque
    m, n = len(mat), len(mat[0])
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if mat[r][c]:
                seen, q = {(r, c)}, deque([(r, c, 0)])
                while q:
                    x, y, d = q.popleft()
                    if mat[x][y] == 0:
                        out[r][c] = d
                        break
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            q.append((nx, ny, d + 1))
    return out


@O
def update_matrix(mat):
    from collections import deque
    m, n = len(mat), len(mat[0])
    dist = [[0 if mat[r][c] == 0 else -1 for c in range(n)] for r in range(m)]
    q = deque((r, c) for r in range(m) for c in range(n) if mat[r][c] == 0)
    while q:
        layer = []
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
                    layer.append((nr, nc))
        if layer:
            T(f"Cells at distance {dist[layer[0][0]][layer[0][1]]}", G("dist (−1 = not reached)", dist, hl=layer), at="prev")
    return dist


# 6 ---------------------------------------------------------------
Q(130, "Surrounded Regions", "Medium", "Search from the border",
  "Flip every 'O' region that is completely surrounded by 'X' (not touching the border) to 'X'. Modify the board in place.",
  [(([["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]],), [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]), (([["X"]],), [["X"]])],
  ("For every 'O', BFS its region to check whether it reaches the border.", "O((m·n)²)", "O(m·n)"),
  ("Flip the question: DFS from every border 'O' and mark it safe ('S'). Then every remaining 'O' is surrounded → 'X', and every 'S' goes back to 'O'.", "O(m·n)", "O(m·n)"),
  inplace=0, viz=([["X", "X", "X", "X", "X"], ["X", "O", "O", "X", "O"], ["X", "X", "O", "X", "O"], ["X", "O", "X", "X", "X"]],))


@B
def solve_regions(board):
    from collections import deque
    m, n = len(board), len(board[0])
    flip = []
    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                seen, q, edge = {(r, c)}, deque([(r, c)]), False
                while q:
                    x, y = q.popleft()
                    if x in (0, m - 1) or y in (0, n - 1):
                        edge = True
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and board[nx][ny] == "O" and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            q.append((nx, ny))
                if not edge:
                    flip.append((r, c))
    for r, c in flip:
        board[r][c] = "X"


@O
def solve_regions(board):
    m, n = len(board), len(board[0])

    def mark(r, c):
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != "O":
            return
        board[r][c] = "S"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            mark(r + dr, c + dc)

    for r in range(m):
        for c in range(n):
            if (r in (0, m - 1) or c in (0, n - 1)) and board[r][c] == "O":
                mark(r, c)
    T("1) Every 'O' reachable from the border is marked safe (S)", G("board", board, ok=[(r, c) for r in range(m) for c in range(n) if board[r][c] == "S"]))
    for r in range(m):
        for c in range(n):
            board[r][c] = "O" if board[r][c] == "S" else "X"
    T("2) Remaining O's were surrounded → X; S → O", G("board", board, ok=[(r, c) for r in range(m) for c in range(n) if board[r][c] == "O"]))


# 7 ---------------------------------------------------------------
Q(417, "Pacific Atlantic Water Flow", "Medium", "Reverse DFS from both oceans",
  "Water flows to a neighbour of equal or lower height. Pacific touches the top and left edges, Atlantic the bottom and right. Return cells that can reach both oceans.",
  [(([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],), [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]), (([[1]],), [[0, 0]])],
  ("From every cell, DFS downhill and record which oceans it reaches.", "O((m·n)²)", "O(m·n)"),
  ("Search uphill from each ocean's edge cells, collecting everything that can drain into it. The answer is the intersection of the two sets.", "O(m·n)", "O(m·n)"),
  norm=sorted)


@B
def pacific_atlantic(heights):
    m, n = len(heights), len(heights[0])
    res = []
    for r in range(m):
        for c in range(n):
            seen, stack, pac, atl = {(r, c)}, [(r, c)], False, False
            while stack:
                x, y = stack.pop()
                pac |= x == 0 or y == 0
                atl |= x == m - 1 or y == n - 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen and heights[nx][ny] <= heights[x][y]:
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            if pac and atl:
                res.append([r, c])
    return res


@O
def pacific_atlantic(heights):
    m, n = len(heights), len(heights[0])

    def climb(starts):
        seen, stack = set(starts), list(starts)
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return seen

    pac = climb([(0, c) for c in range(n)] + [(r, 0) for r in range(m)])
    T("Cells that can drain into the Pacific (top / left)", G("heights", heights, hl=list(pac)))
    atl = climb([(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m)])
    T("Cells that can drain into the Atlantic (bottom / right)", G("heights", heights, hl=list(atl)))
    both = sorted(pac & atl)
    T("Both oceans = intersection", G("heights", heights, ok=both))
    return [list(x) for x in both]


# 8 ---------------------------------------------------------------
Q(547, "Number of Provinces", "Medium", "Union–Find",
  "<code>isConnected[i][j] = 1</code> if cities i and j are directly connected. Count the connected groups (provinces).",
  [(([[1, 1, 0], [1, 1, 0], [0, 0, 1]],), 2), (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), 3)],
  ("Compute full reachability with Floyd–Warshall style closure, then count distinct reachability rows.", "O(n³)", "O(n²)"),
  ("Union–find: union every connected pair; each successful union merges two provinces, so answer = n − unions. (DFS over the matrix is also O(n²).)", "O(n² · α(n))", "O(n)"),
  viz=([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1]],))


@B
def find_circle_num(is_connected):
    n = len(is_connected)
    reach = [[bool(is_connected[i][j]) or i == j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return len({tuple(row) for row in reach})


@O
def find_circle_num(is_connected):
    n = len(is_connected)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if is_connected[i][j]]
    for i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            groups -= 1
        T(f"Union cities {i} and {j}", GR("cities", n, edges, he=[(i, j)]), A("parent", parent, hl=[i, j]), V(provinces=groups), at="prev")
    return groups


# 9 ---------------------------------------------------------------
Q(785, "Is Graph Bipartite?", "Medium", "BFS 2-colouring",
  "Can the nodes be split into two groups so every edge joins nodes from different groups? <code>graph[i]</code> lists i's neighbours.",
  [(([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],), False), (([[1, 3], [0, 2], [1, 3], [0, 2]],), True)],
  ("Try all 2ⁿ ways to assign the two colours.", "O(2ⁿ · E)", "O(n)"),
  ("Colour each uncoloured node 0, BFS, and give neighbours the opposite colour. A neighbour with the same colour proves it's not bipartite.", "O(V + E)", "O(V)"),
  viz=([[1, 3], [0, 2], [1, 3], [0, 2]],))


@B
def is_bipartite(graph):
    n = len(graph)
    for mask in range(1 << n):
        if all((mask >> u & 1) != (mask >> v & 1) for u in range(n) for v in graph[u]):
            return True
    return False


@O
def is_bipartite(graph):
    from collections import deque
    n = len(graph)
    color = [-1] * n
    edges = [(u, v) for u in range(n) for v in graph[u] if u < v]
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    T(f"Edge {u}–{v} joins two nodes of colour {color[u]} → not bipartite", GR("graph", n, edges, hl=[u, v], he=[(u, v)]), A("color", color, bad=[u, v]))
                    return False
            T(f"Colour {u}'s neighbours with {1 - color[u]}", GR("graph", n, edges, hl=[i for i in range(n) if color[i] == 0], ok=[i for i in range(n) if color[i] == 1]), A("color", color, hl=[u]), at="prev")
    return True


# 10 --------------------------------------------------------------
Q(207, "Course Schedule", "Medium", "Kahn's topological sort",
  "There are <code>numCourses</code> courses; <code>[a, b]</code> means b must be taken before a. Can you finish all courses?",
  [((2, [[1, 0]]), True), ((2, [[1, 0], [0, 1]]), False), ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False)],
  ("From every course, DFS to look for a path back to itself (a cycle), with no memo.", "O(V · (V + E))", "O(V + E)"),
  ("Count in-degrees. Queue every course with in-degree 0, take it, and decrement its dependents. If every course gets taken there is no cycle.", "O(V + E)", "O(V + E)"),
  viz=(5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]))


@B
def can_finish(num_courses, prerequisites):
    adj = {i: [] for i in range(num_courses)}
    for a, b in prerequisites:
        adj[b].append(a)

    def reaches(u, target, seen):
        for v in adj[u]:
            if v == target or (v not in seen and (seen.add(v) or reaches(v, target, seen))):
                return True
        return False
    return not any(reaches(c, c, set()) for c in range(num_courses))


@O
def can_finish(num_courses, prerequisites):
    from collections import deque
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    taken = []
    while q:
        u = q.popleft()
        taken.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        T(f"Take course {u}; its dependents lose one prerequisite", GR("prerequisite → course", num_courses, [(b, a) for a, b in prerequisites], ok=taken, hl=list(q), directed=True), A("in-degree", indeg), A("taken", taken), at="prev")
    return len(taken) == num_courses


# 11 --------------------------------------------------------------
Q(210, "Course Schedule II", "Medium", "Topological order",
  "Return an order to take all courses respecting prerequisites, or <code>[]</code> if impossible.",
  [((2, [[1, 0]]), [0, 1]), ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), [0, 2, 1, 3]), ((2, [[0, 1], [1, 0]]), [])],
  ("Repeatedly scan for any untaken course whose prerequisites are all taken.", "O(V · E)", "O(V)"),
  ("Kahn's algorithm: the order in which courses leave the zero-in-degree queue is a valid order.", "O(V + E)", "O(V + E)"),
  check=lambda a, out: _topo_ok(a[0], a[1], out),
  viz=(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))


def _topo_ok(n, pre, out):
    if not out:
        return _has_cycle(n, pre)
    pos = {c: i for i, c in enumerate(out)}
    return len(out) == n and len(pos) == n and all(pos[b] < pos[a] for a, b in pre)


def _has_cycle(n, pre):
    indeg = [0] * n
    adj = [[] for _ in range(n)]
    for a, b in pre:
        adj[b].append(a)
        indeg[a] += 1
    q = [i for i in range(n) if indeg[i] == 0]
    seen = 0
    while q:
        u = q.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen < n


@B
def find_order(num_courses, prerequisites):
    taken, order = set(), []
    while len(order) < num_courses:
        for c in range(num_courses):
            if c not in taken and all(b in taken for a, b in prerequisites if a == c):
                taken.add(c)
                order.append(c)
                break
        else:
            return []
    return order


@O
def find_order(num_courses, prerequisites):
    from collections import deque
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        T(f"Course {u} is ready → add to the order", GR("prerequisite → course", num_courses, [(b, a) for a, b in prerequisites], ok=order, hl=list(q), directed=True), A("order", order), at="prev")
    return order if len(order) == num_courses else []


# 12 --------------------------------------------------------------
Q(802, "Find Eventual Safe States", "Medium", "3-colour DFS",
  "A node is safe if every path from it ends at a terminal node (no outgoing edges). Return all safe nodes, sorted.",
  [(([[1, 2], [2, 3], [5], [0], [5], [], []],), [2, 4, 5, 6]), (([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []],), [4])],
  ("For each node, explore every path from it and check none loops (no memo).", "O(V · (V + E))", "O(V)"),
  ("DFS with three states: 0 unvisited, 1 on the current path, 2 known safe. Reaching a node in state 1 means a cycle, so everything on that path is unsafe.", "O(V + E)", "O(V)"))


@B
def eventual_safe_nodes(graph):
    def safe(u, path):
        if u in path:
            return False
        return all(safe(v, path | {u}) for v in graph[u])
    return [u for u in range(len(graph)) if safe(u, frozenset())]


@O
def eventual_safe_nodes(graph):
    n = len(graph)
    state = [0] * n
    edges = [(u, v) for u in range(n) for v in graph[u]]

    def dfs(u):
        if state[u]:
            return state[u] == 2
        state[u] = 1
        for v in graph[u]:
            if not dfs(v):
                T(f"{u} can reach a cycle → unsafe", GR("graph", n, edges, hl=[i for i in range(n) if state[i] == 1], ok=[i for i in range(n) if state[i] == 2], directed=True), A("state (1 on path, 2 safe)", state, hl=[u]))
                return False
        state[u] = 2
        T(f"Every path from {u} ends → safe", GR("graph", n, edges, hl=[i for i in range(n) if state[i] == 1], ok=[i for i in range(n) if state[i] == 2], directed=True), A("state (1 on path, 2 safe)", state, ok=[u]), at="prev")
        return True

    return [u for u in range(n) if dfs(u)]


# 13 --------------------------------------------------------------
Q(684, "Redundant Connection", "Medium", "Union–Find detects the cycle edge",
  "A tree of n nodes had one extra edge added. Return the edge that can be removed to make it a tree again (the last such edge in the input).",
  [(([[1, 2], [1, 3], [2, 3]],), [2, 3]), (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4])],
  ("Try removing each edge (from the last) and check whether the rest is connected.", "O(E · (V + E))", "O(V + E)"),
  ("Add edges one by one with union–find. The first edge whose endpoints already share a root closes a cycle — that's the answer.", "O(E · α(V))", "O(V)"))


@B
def find_redundant_connection(edges):
    n = len(edges)
    for skip in range(n - 1, -1, -1):
        adj = {i: [] for i in range(1, n + 1)}
        for k, (a, b) in enumerate(edges):
            if k != skip:
                adj[a].append(b)
                adj[b].append(a)
        seen, stack = {1}, [1]
        while stack:
            for v in adj[stack.pop()]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) == n:
            return edges[skip]


@O
def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for k, (a, b) in enumerate(edges):
        ra, rb = find(a), find(b)
        if ra == rb:
            T(f"{a} and {b} are already connected → [{a}, {b}] is redundant", GR("graph", list(range(1, len(edges) + 1)), edges[:k + 1], he=[(a, b)], hl=[a, b]), A("parent", parent))
            return [a, b]
        parent[ra] = rb
        T(f"Union {a} and {b}", GR("graph", list(range(1, len(edges) + 1)), edges[:k + 1], he=[(a, b)]), A("parent", parent, hl=[a, b]), at="prev")


# 14 --------------------------------------------------------------
Q(721, "Accounts Merge", "Medium", "Union–Find over emails",
  "Each account is [name, emails…]. Accounts sharing any email belong to the same person. Merge them; return [name, sorted emails…] per person.",
  [(([["John", "a@m.co", "b@m.co"], ["John", "a@m.co", "c@m.co"], ["Mary", "m@m.co"], ["John", "j@m.co"]],), [["John", "a@m.co", "b@m.co", "c@m.co"], ["Mary", "m@m.co"], ["John", "j@m.co"]])],
  ("Repeatedly find two accounts that share an email and merge them, until no merge happens.", "O(n² · k) per pass", "O(n · k)"),
  ("Union each account's emails with its first email. Then group emails by their root, sort, and attach the owner's name.", "O(N log N), N = total emails", "O(N)"),
  norm=sorted)


@B
def accounts_merge(accounts):
    groups = [[a[0], set(a[1:])] for a in accounts]
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if groups[i][1] & groups[j][1]:
                    groups[i][1] |= groups.pop(j)[1]
                    merged = True
                    break
            if merged:
                break
    return [[name] + sorted(emails) for name, emails in groups]


@O
def accounts_merge(accounts):
    parent, owner = {}, {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for name, *emails in accounts:
        for e in emails:
            parent.setdefault(e, e)
            owner[e] = name
        for e in emails[1:]:
            parent[find(e)] = find(emails[0])
        T(f"Union {name}'s emails with {emails[0]}", M("parent (email → parent)", parent), at="prev")
    groups = {}
    for e in parent:
        groups.setdefault(find(e), []).append(e)
    T("Group emails by their root", M("groups", {r: sorted(g) for r, g in groups.items()}))
    return [[owner[r]] + sorted(g) for r, g in groups.items()]


# 15 --------------------------------------------------------------
Q(127, "Word Ladder", "Hard", "BFS with wildcard buckets",
  "Transform <code>beginWord</code> to <code>endWord</code> changing one letter at a time, every step a word in <code>wordList</code>. Return the number of words in the shortest sequence, or 0.",
  [(("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5), (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0)],
  ("BFS where each word's neighbours are found by comparing it with every word in the list.", "O(N² · L)", "O(N)"),
  ("BFS, but find neighbours through patterns: 'hot' belongs to buckets '*ot', 'h*t', 'ho*'. Words sharing a bucket differ by one letter.", "O(N · L²)", "O(N · L²)"))


@B
def ladder_length(begin_word, end_word, word_list):
    from collections import deque
    words = set(word_list)
    if end_word not in words:
        return 0
    q, seen = deque([(begin_word, 1)]), {begin_word}
    while q:
        w, d = q.popleft()
        if w == end_word:
            return d
        for x in words:
            if x not in seen and sum(a != b for a, b in zip(w, x)) == 1:
                seen.add(x)
                q.append((x, d + 1))
    return 0


@O
def ladder_length(begin_word, end_word, word_list):
    from collections import deque, defaultdict
    if end_word not in word_list:
        return 0
    L = len(begin_word)
    buckets = defaultdict(list)
    for w in word_list:
        for i in range(L):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    q, seen, steps = deque([begin_word]), {begin_word}, 1
    while q:
        T(f"Step {steps}: frontier {list(q)}", A("frontier", list(q)), M("seen", seen), V(steps=steps))
        for _ in range(len(q)):
            w = q.popleft()
            if w == end_word:
                return steps
            for i in range(L):
                for nxt in buckets[w[:i] + "*" + w[i + 1:]]:
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
        steps += 1
    return 0


# 16 --------------------------------------------------------------
Q(1091, "Shortest Path in Binary Matrix", "Medium", "BFS, 8 directions",
  "Return the length (cells visited) of the shortest clear path of 0s from top-left to bottom-right, moving in 8 directions, or −1.",
  [(([[0, 1], [1, 0]],), 2), (([[0, 0, 0], [1, 1, 0], [1, 1, 0]],), 4), (([[1, 0, 0], [1, 1, 0], [1, 1, 0]],), -1)],
  ("DFS every simple path and keep the shortest.", "O(8^(m·n))", "O(m·n)"),
  ("BFS from (0, 0) over the 8 neighbours. The first time BFS reaches the corner, that layer number is the shortest length.", "O(m·n)", "O(m·n)"),
  viz=([[0, 0, 0, 1], [1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]],))


@B
def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    best = [float("inf")]

    def dfs(r, c, length, seen):
        if length >= best[0]:
            return
        if (r, c) == (n - 1, n - 1):
            best[0] = length
            return
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    dfs(nr, nc, length + 1, seen)
                    seen.remove((nr, nc))
    dfs(0, 0, 1, {(0, 0)})
    return -1 if best[0] == float("inf") else best[0]


@O
def shortest_path_binary_matrix(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    q, seen, length = deque([(0, 0)]), {(0, 0)}, 1
    while q:
        T(f"Layer {length}", G("grid", grid, ok=list(seen), hl=list(q)), V(length=length))
        for _ in range(len(q)):
            r, c = q.popleft()
            if (r, c) == (n - 1, n - 1):
                return length
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))
        length += 1
    return -1


# 17 --------------------------------------------------------------
Q(743, "Network Delay Time", "Medium", "Dijkstra",
  "<code>times[i] = (u, v, w)</code> is a directed edge taking w. A signal starts at node <code>k</code>. Return the time until all n nodes have it, or −1.",
  [(([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2), (([[1, 2, 1]], 2, 1), 1), (([[1, 2, 1]], 2, 2), -1)],
  ("Bellman–Ford: relax every edge n − 1 times.", "O(V · E)", "O(V)"),
  ("Dijkstra: pop the closest unfinished node from a min-heap and relax its edges. Skip stale heap entries. The answer is the largest final distance.", "O(E log V)", "O(V + E)"),
  viz=([[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5]], 4, 1))


@B
def network_delay_time(times, n, k):
    dist = [float("inf")] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    best = max(dist[1:])
    return -1 if best == float("inf") else best


@O
def network_delay_time(times, n, k):
    import heapq
    adj = {i: [] for i in range(1, n + 1)}
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
        T(f"Finalise node {u} at time {d}", GR("network", list(range(1, n + 1)), times, ok=list(dist), hl=[u], directed=True), M("dist", dist, hl=u), A("heap (time, node)", sorted(heap)), at="prev")
    return max(dist.values()) if len(dist) == n else -1


# 18 --------------------------------------------------------------
Q(787, "Cheapest Flights Within K Stops", "Medium", "Bellman–Ford, k + 1 rounds",
  "Find the cheapest price from <code>src</code> to <code>dst</code> using at most <code>k</code> stops, or −1.",
  [((4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1), 700), ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1), 200), ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), 500)],
  ("DFS every route of at most k + 1 flights and keep the cheapest.", "O(n^(k+1))", "O(k)"),
  ("Run k + 1 rounds of relaxing every flight, always reading prices from the previous round's copy so each round adds at most one flight.", "O(k · E)", "O(n)"),
  viz=(5, [[0, 1, 100], [1, 2, 100], [2, 4, 100], [0, 3, 500], [3, 4, 50], [1, 3, 100]], 0, 4, 2))


@B
def find_cheapest_price(n, flights, src, dst, k):
    adj = {i: [] for i in range(n)}
    for u, v, w in flights:
        adj[u].append((v, w))
    best = [float("inf")]

    def dfs(u, cost, used):
        if u == dst:
            best[0] = min(best[0], cost)
            return
        if used == k + 1:
            return
        for v, w in adj[u]:
            dfs(v, cost + w, used + 1)
    dfs(src, 0, 0)
    return -1 if best[0] == float("inf") else best[0]


@O
def find_cheapest_price(n, flights, src, dst, k):
    INF = float("inf")
    price = [INF] * n
    price[src] = 0
    for rnd in range(k + 1):
        nxt = price[:]
        for u, v, w in flights:
            if price[u] + w < nxt[v]:
                nxt[v] = price[u] + w
        price = nxt
        T(f"After round {rnd + 1} (≤ {rnd + 1} flights)", GR("flights", n, flights, ok=[i for i in range(n) if price[i] < INF], hl=[dst], directed=True), A("price", price, hl=[dst]), at="prev")
    return -1 if price[dst] == INF else price[dst]


# 19 --------------------------------------------------------------
Q(1631, "Path With Minimum Effort", "Medium", "Dijkstra on max edge",
  "A route's effort is its largest absolute height difference between consecutive cells. Return the minimum effort from top-left to bottom-right.",
  [(([[1, 2, 2], [3, 8, 2], [5, 3, 5]],), 2), (([[1, 2, 3], [3, 8, 4], [5, 3, 5]],), 1), (([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]],), 0)],
  ("Relax all cells repeatedly (Bellman–Ford style) until no effort improves.", "O((m·n)²)", "O(m·n)"),
  ("Dijkstra where a path's cost is the max edge so far: pop the cell with the smallest effort, relax neighbours with max(effort, |Δh|).", "O(m·n · log(m·n))", "O(m·n)"))


@B
def minimum_effort_path(heights):
    m, n = len(heights), len(heights[0])
    eff = [[float("inf")] * n for _ in range(m)]
    eff[0][0] = 0
    changed = True
    while changed:
        changed = False
        for r in range(m):
            for c in range(n):
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n:
                        e = max(eff[r][c], abs(heights[nr][nc] - heights[r][c]))
                        if e < eff[nr][nc]:
                            eff[nr][nc] = e
                            changed = True
    return eff[m - 1][n - 1]


@O
def minimum_effort_path(heights):
    import heapq
    m, n = len(heights), len(heights[0])
    eff = [[float("inf")] * n for _ in range(m)]
    eff[0][0] = 0
    heap, done = [(0, 0, 0)], []
    while heap:
        e, r, c = heapq.heappop(heap)
        if e > eff[r][c]:
            continue
        done.append((r, c))
        T(f"Settle ({r},{c}) with effort {e}", G("heights", heights, ok=done, hl=[(r, c)]), G("effort", eff), at="prev")
        if (r, c) == (m - 1, n - 1):
            return e
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                if ne < eff[nr][nc]:
                    eff[nr][nc] = ne
                    heapq.heappush(heap, (ne, nr, nc))


# 20 --------------------------------------------------------------
Q(1584, "Min Cost to Connect All Points", "Medium", "Prim's MST (dense)",
  "Connect all points with edges costing their Manhattan distance; return the minimum total cost.",
  [(([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), 20), (([[3, 12], [-2, 5], [-4, 1]],), 18)],
  ("Kruskal: build all n² edges, sort them, add the cheapest that joins two components.", "O(n² log n)", "O(n²)"),
  ("Prim for a dense graph: keep each point's cheapest connection to the tree in an array; repeatedly add the closest point and update the others. No heap or edge list needed.", "O(n²)", "O(n)"))


@B
def min_cost_connect_points(points):
    n = len(points)
    edges = sorted((abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j) for i in range(n) for j in range(i + 1, n))
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    total = 0
    for w, i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            total += w
    return total


@O
def min_cost_connect_points(points):
    n = len(points)
    INF = float("inf")
    best = [INF] * n
    best[0] = 0
    in_tree = [False] * n
    tree_edges, link = [], [-1] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: best[i])
        in_tree[u] = True
        total += best[u]
        if link[u] >= 0:
            tree_edges.append((link[u], u, best[u]))
        for v in range(n):
            d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
            if not in_tree[v] and d < best[v]:
                best[v], link[v] = d, u
        T(f"Add point {u} (cost {best[u]}); update everyone's cheapest link", GR("points", n, tree_edges, ok=[i for i in range(n) if in_tree[i]], hl=[u]), A("cheapest link to tree", best, ok=[i for i in range(n) if in_tree[i]]), V(total=total), at="prev")
    return total
