from lib import *

THEORY("Definition", """
<p>A <b>graph</b> G = (V, E) is a non-linear data structure consisting of a set of <b>vertices</b> (nodes) V and a set of <b>edges</b> E, where each edge connects a pair of vertices. Graphs model relationships and networks.</p>
<p>A tree is a special graph: connected, undirected and acyclic, with exactly V − 1 edges.</p>
""")

THEORY("Terminology", """
<table>
<tr><th>Term</th><th>Meaning</th></tr>
<tr><td>Adjacent</td><td>two vertices joined by an edge</td></tr>
<tr><td>Degree</td><td>number of edges at a vertex; in directed graphs, <b>in-degree</b> and <b>out-degree</b></td></tr>
<tr><td>Path</td><td>sequence of vertices joined by edges; <b>simple</b> if no vertex repeats</td></tr>
<tr><td>Cycle</td><td>a path that starts and ends at the same vertex</td></tr>
<tr><td>Connected graph</td><td>a path exists between every pair of vertices (undirected)</td></tr>
<tr><td>Connected component</td><td>a maximal connected piece of an undirected graph</td></tr>
<tr><td>Strongly connected</td><td>directed graph where every vertex reaches every other</td></tr>
<tr><td>DAG</td><td>directed acyclic graph</td></tr>
<tr><td>Spanning tree</td><td>a tree using all vertices and a subset of the edges</td></tr>
<tr><td>Bipartite</td><td>vertices split into two sets with every edge crossing between them</td></tr>
</table>
<p><b>Handshake lemma</b>: in an undirected graph, the sum of all degrees = 2|E| (each edge counts at both ends).</p>
""")

THEORY("Types of graphs", """
<table>
<tr><th>Type</th><th>Description</th><th>Example</th></tr>
<tr><td>Undirected</td><td>edges have no direction</td><td>friendship, roads both ways</td></tr>
<tr><td>Directed (digraph)</td><td>edges point from u to v</td><td>followers, prerequisites, web links</td></tr>
<tr><td>Weighted</td><td>edges carry a cost</td><td>distances, latency, prices</td></tr>
<tr><td>Unweighted</td><td>all edges equal</td><td>grid moves, word ladder</td></tr>
<tr><td>Cyclic / acyclic</td><td>has / has no cycle</td><td>DAG of tasks</td></tr>
<tr><td>Sparse / dense</td><td>E ≈ V vs E ≈ V²</td><td>road networks vs complete graphs</td></tr>
<tr><td>Complete</td><td>every pair connected: V(V − 1)/2 edges</td><td>—</td></tr>
<tr><td>Implicit</td><td>edges computed on the fly, not stored</td><td>grids, puzzle states</td></tr>
</table>
""")

THEORY("Representations", """
<table>
<tr><th></th><th>Adjacency matrix</th><th>Adjacency list</th><th>Edge list</th></tr>
<tr><td>Space</td><td>O(V²)</td><td>O(V + E)</td><td>O(E)</td></tr>
<tr><td>Is (u, v) an edge?</td><td>O(1)</td><td>O(deg u)</td><td>O(E)</td></tr>
<tr><td>List neighbours of u</td><td>O(V)</td><td>O(deg u)</td><td>O(E)</td></tr>
<tr><td>Add edge</td><td>O(1)</td><td>O(1)</td><td>O(1)</td></tr>
<tr><td>Best for</td><td>dense graphs, Floyd–Warshall</td><td>most algorithms (BFS, DFS, Dijkstra)</td><td>Kruskal, Bellman–Ford, input format</td></tr>
</table>
""")

THEORY("Traversals: BFS and DFS", """
<table>
<tr><th></th><th>Breadth-first search</th><th>Depth-first search</th></tr>
<tr><td>Data structure</td><td>queue</td><td>stack / recursion</td></tr>
<tr><td>Order</td><td>level by level (by distance)</td><td>as deep as possible, then backtrack</td></tr>
<tr><td>Shortest path (unweighted)</td><td><b>yes</b></td><td>no</td></tr>
<tr><td>Time</td><td>O(V + E)</td><td>O(V + E)</td></tr>
<tr><td>Space</td><td>O(V) — the frontier can be wide</td><td>O(V) — the recursion can be deep</td></tr>
<tr><td>Uses</td><td>shortest steps, levels, multi-source spread</td><td>components, cycle detection, topological sort, path finding, backtracking</td></tr>
</table>
<p><b>Cycle detection</b>: undirected — a visited neighbour that isn't the parent means a cycle (or union-find). Directed — reaching a vertex that is still on the current DFS path (colour "grey") means a cycle.</p>
""")

THEORY("Core algorithms", """
<table>
<tr><th>Algorithm</th><th>Solves</th><th>Requirement</th><th>Time</th></tr>
<tr><td>BFS</td><td>single-source shortest path</td><td>unweighted</td><td>O(V + E)</td></tr>
<tr><td>0-1 BFS</td><td>shortest path</td><td>weights 0 or 1 (deque)</td><td>O(V + E)</td></tr>
<tr><td><b>Dijkstra</b></td><td>single-source shortest path</td><td>non-negative weights</td><td>O((V + E) log V)</td></tr>
<tr><td><b>Bellman–Ford</b></td><td>single-source shortest path, detects negative cycles</td><td>any weights</td><td>O(V · E)</td></tr>
<tr><td>Floyd–Warshall</td><td>all-pairs shortest paths</td><td>no negative cycles</td><td>O(V³)</td></tr>
<tr><td><b>Topological sort</b> (Kahn / DFS)</td><td>ordering of a DAG</td><td>directed, acyclic</td><td>O(V + E)</td></tr>
<tr><td><b>Kruskal</b></td><td>minimum spanning tree</td><td>undirected, weighted</td><td>O(E log E)</td></tr>
<tr><td><b>Prim</b></td><td>minimum spanning tree</td><td>undirected, weighted</td><td>O(E log V) heap, O(V²) array</td></tr>
<tr><td>Union–Find</td><td>dynamic connectivity</td><td>—</td><td>≈ O(α(n)) per operation</td></tr>
<tr><td>Kosaraju / Tarjan</td><td>strongly connected components</td><td>directed</td><td>O(V + E)</td></tr>
</table>
<p><b>Why Dijkstra fails with negative edges</b>: it finalises the closest vertex assuming no later path can be shorter; a negative edge discovered later could make it shorter.</p>
""")

THEORY("Applications", """
<ul>
<li>Maps and navigation (shortest routes: Dijkstra, A*).</li>
<li>Social networks (friend suggestions, communities, degrees of separation).</li>
<li>Computer networks (routing protocols use Bellman–Ford / Dijkstra; spanning tree protocol).</li>
<li>Build systems, package managers and course planning (topological sort of dependencies).</li>
<li>Web crawling and PageRank (directed link graph).</li>
<li>Circuit and pipeline design (minimum spanning trees).</li>
<li>Recommendation systems and knowledge graphs.</li>
<li>Image processing (flood fill, connected regions in a pixel grid).</li>
</ul>
""")

FAQ("BFS vs DFS — when do you use each?", "<p>BFS when you need the shortest path or minimum steps in an unweighted graph, or level-by-level processing. DFS for exploring all reachable nodes, connected components, cycle detection, topological sort and backtracking-style searches. Both are O(V + E).</p>")
FAQ("Adjacency list or adjacency matrix?", "<p>List for sparse graphs (most real graphs): O(V + E) space and fast neighbour iteration. Matrix for dense graphs or when you need O(1) edge checks, at O(V²) space.</p>")
FAQ("Why does Dijkstra not work with negative weights?", "<p>Dijkstra permanently fixes a vertex's distance when it's popped as the closest. A negative edge found later could reduce that distance, but the algorithm never revisits it. Use Bellman–Ford instead.</p>")
FAQ("How do you detect a cycle in a directed graph?", "<p>DFS with three colours (unvisited, on stack, done): an edge to an 'on stack' vertex is a back edge → cycle. Or Kahn's algorithm: if the topological order doesn't include all vertices, there is a cycle.</p>")
FAQ("What is a topological sort and when does it exist?", "<p>A linear order of vertices such that every directed edge u → v has u before v. It exists if and only if the graph is a DAG (no directed cycles).</p>")
FAQ("Kruskal vs Prim?", "<p>Both build a minimum spanning tree. Kruskal sorts all edges and adds the cheapest that doesn't form a cycle (union-find) — good for sparse graphs. Prim grows one tree from a start vertex, adding the cheapest edge leaving it — good for dense graphs.</p>")
FAQ("What is union-find and what are its optimisations?", "<p>A structure that tracks which set each element belongs to, supporting <code>find</code> (root of a set) and <code>union</code> (merge sets). Path compression and union by rank/size make both operations nearly O(1) (inverse Ackermann).</p>")
FAQ("How many edges can a graph have?", "<p>Undirected simple graph: at most V(V − 1)/2. Directed: at most V(V − 1). A tree has exactly V − 1; a connected graph needs at least V − 1.</p>")
