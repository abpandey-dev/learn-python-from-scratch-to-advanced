from lib import *

LESSON("Basics", "What a graph is and how to store it", """
<p>A <b>graph</b> is a set of <b>nodes</b> (vertices) joined by <b>edges</b>. Cities and roads, people and friendships, courses and prerequisites, web pages and links — all graphs.</p>
<ul>
<li><b>Undirected</b> edges go both ways (friendship). <b>Directed</b> edges have an arrow (prerequisite → course).</li>
<li><b>Weighted</b> edges carry a cost (distance, time).</li>
<li>A <b>path</b> is a sequence of edges; a <b>cycle</b> is a path that returns to its start.</li>
</ul>
<h4>Three ways to store one</h4>
<table>
<tr><th>Form</th><th>Looks like</th><th>Good for</th></tr>
<tr><td>Edge list</td><td><code>[(0,1), (1,2), (0,2)]</code></td><td>input format, Kruskal, union-find</td></tr>
<tr><td><b>Adjacency list</b></td><td><code>{0: [1, 2], 1: [0, 2], …}</code></td><td>almost everything — O(V + E) space</td></tr>
<tr><td>Adjacency matrix</td><td><code>m[u][v] = 1</code></td><td>dense graphs, O(1) "is there an edge?"</td></tr>
</table>
<p>A <b>grid</b> is a graph too: each cell is a node connected to its 4 neighbours. You don't build anything — just compute neighbours with <code>(r ± 1, c)</code>, <code>(r, c ± 1)</code>.</p>
""")


@LD
def adjacency_lesson():
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    adj = {i: [] for i in range(5)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        T(f"Edge {u}–{v}: add {v} to {u}'s list and {u} to {v}'s list", GR("graph", 5, edges, he=[(u, v)], hl=[u, v]), M("adjacency list", adj), at="prev")
    return adj


LESSON("Basics", "Depth-first search", """
<p><b>DFS</b> goes as deep as possible along one path before backing up — like exploring a maze by always taking the next unexplored turn. Mark nodes as <b>visited</b> so you never loop forever.</p>
<pre><code class="py">seen = set()
def dfs(u):
    seen.add(u)
    for v in adj[u]:
        if v not in seen:
            dfs(v)</code></pre>
<p>Iterative version: replace recursion with a stack (<code>stack.pop()</code> / <code>stack.append()</code>). Each node and edge is handled once → <b>O(V + E)</b>.</p>
<p>DFS answers "can I reach…?", "how many connected pieces?", "is there a cycle?", and is the base of topological sort.</p>
""", practice=[547, 733])


@LD
def dfs_lesson():
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
    adj = {i: [] for i in range(6)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, order = set(), []

    def dfs(u):
        seen.add(u)
        order.append(u)
        T(f"Visit {u}; go deeper into an unvisited neighbour", GR("graph", 6, edges, hl=[u], ok=[x for x in order if x != u]), A("visit order", order))
        for v in adj[u]:
            if v not in seen:
                dfs(v)

    dfs(0)
    return order


LESSON("Core", "Breadth-first search and shortest paths", """
<p><b>BFS</b> explores in rings: first all nodes 1 edge away, then 2 edges, then 3. It uses a queue. Because of that order, the first time BFS reaches a node is along a <b>shortest path</b> (when every edge costs the same).</p>
<pre><code class="py">dist = {start: 0}
q = deque([start])
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:          # mark when you PUSH
            dist[v] = dist[u] + 1
            q.append(v)</code></pre>
<p><b>Multi-source BFS</b>: put every starting point in the queue at once (all rotten oranges, all zeros). Each layer then means "one more minute" or "one more step from the nearest source".</p>
""", practice=[994, 542, 1091, 127])


LESSON("Core", "Grids: islands and flood fill", """
<p>Most grid problems are "count or measure the connected groups". Loop over every cell; when you find an unvisited land cell, that's a new group — run DFS/BFS from it and mark everything it reaches.</p>
<pre><code class="py">for r in range(m):
    for c in range(n):
        if grid[r][c] == "1":
            count += 1
            sink(r, c)          # DFS that turns the whole island to "0"</code></pre>
<p>Useful twists:</p>
<ul>
<li><b>Return a size</b> from the DFS for max area.</li>
<li><b>Search from the border</b> when the question is about regions <i>not</i> touching the edge (surrounded regions), or reaching an ocean (Pacific–Atlantic: climb uphill from each ocean).</li>
</ul>
""", practice=[200, 695, 130, 417, 733])


LESSON("Core", "Directed graphs: topological order and cycles", """
<p>A <b>topological order</b> lists the nodes of a directed graph so every edge points forward — "take prerequisites before courses". It exists only if there's <b>no cycle</b>.</p>
<h4>Kahn's algorithm</h4>
<ol>
<li>Count each node's <b>in-degree</b> (incoming edges).</li>
<li>Queue every node with in-degree 0 — nothing blocks it.</li>
<li>Pop a node, add it to the order, and decrease the in-degree of its neighbours; push any that reach 0.</li>
<li>If the order has all V nodes, done. If not, the leftovers sit on a cycle.</li>
</ol>
<p>DFS alternative: colour nodes 0 = new, 1 = on the current path, 2 = finished. Reaching a node coloured 1 means a cycle (used in "eventual safe states").</p>
""", practice=[207, 210, 802])


LESSON("Core", "Union–Find (disjoint set union)", """
<p><b>Union–Find</b> keeps track of groups as you connect things. Each node points to a parent; the node at the top of a chain is the group's <b>root</b>.</p>
<pre><code class="py">parent = list(range(n))
def find(x):                       # root of x's group
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False       # already connected → this edge makes a cycle
    parent[ra] = rb
    return True</code></pre>
<p>With path compression (and optionally union by size), each operation is nearly O(1). Use it for counting groups, detecting the edge that closes a cycle, merging accounts, and Kruskal's MST.</p>
""", practice=[547, 684, 721])


@LD
def union_find_lesson():
    parent = list(range(6))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = [(0, 1), (2, 3), (1, 3), (4, 5), (0, 2)]
    done = []
    for a, b in edges:
        ra, rb = find(a), find(b)
        done.append((a, b))
        if ra == rb:
            T(f"{a} and {b} already share root {ra} → this edge would close a cycle", GR("edges so far", 6, done, he=[(a, b)], hl=[a, b]), A("parent", parent, bad=[a, b]))
        else:
            parent[ra] = rb
            T(f"union({a}, {b}): root {ra} now points to root {rb}", GR("edges so far", 6, done, he=[(a, b)]), A("parent", parent, hl=[ra]), V(groups=len({find(i) for i in range(6)})), at="prev")
    return parent


LESSON("Advanced", "Weighted shortest paths", """
<p>When edges have different costs, BFS is no longer enough.</p>
<h4>Dijkstra (no negative weights)</h4>
<p>Keep a min-heap of <code>(distance so far, node)</code>. Pop the closest node — its distance is now final — and relax its edges. Skip stale heap entries. O(E log V).</p>
<pre><code class="py">dist = {}
heap = [(0, src)]
while heap:
    d, u = heapq.heappop(heap)
    if u in dist: continue          # already finalised
    dist[u] = d
    for v, w in adj[u]:
        if v not in dist:
            heapq.heappush(heap, (d + w, v))</code></pre>
<h4>Bellman–Ford</h4>
<p>Relax every edge, V − 1 rounds. Slower (O(V · E)) but handles negative weights, and running only k + 1 rounds gives "cheapest path with at most k stops" — copy the distance array each round.</p>
<p>The "cost" can be anything that only grows along a path: the max height difference (path with minimum effort), probability, time.</p>
""", practice=[743, 787, 1631])


@LD
def dijkstra_lesson():
    import heapq
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]
    adj = {i: [] for i in range(4)}
    for u, v, w in edges:
        adj[u].append((v, w))
    dist, heap = {}, [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            T(f"Pop ({d}, {u}) but {u} is already final → skip stale entry", GR("graph", 4, edges, ok=list(dist), directed=True), M("final dist", dist))
            continue
        dist[u] = d
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
        T(f"Closest unfinished node is {u} at distance {d} → final", GR("graph", 4, edges, ok=list(dist), hl=[u], directed=True), M("final dist", dist, hl=u), A("heap (dist, node)", sorted(heap)), at="prev")
    return dist


LESSON("Advanced", "Spanning trees and two-colouring", """
<h4>Minimum spanning tree</h4>
<p>Connect all nodes with the cheapest total edge cost (no cycles needed).</p>
<ul>
<li><b>Kruskal</b>: sort edges by cost; add each edge whose ends are in different union-find groups. O(E log E).</li>
<li><b>Prim</b>: grow one tree; repeatedly add the cheapest edge leaving it. With a plain array it's O(V²) — best for dense graphs like "connect all points".</li>
</ul>
<h4>Bipartite check</h4>
<p>Can nodes be split into two teams with every edge going across? BFS and colour neighbours with the opposite colour; a same-colour edge means no. A graph is bipartite exactly when it has no odd-length cycle.</p>
""", practice=[1584, 785])
