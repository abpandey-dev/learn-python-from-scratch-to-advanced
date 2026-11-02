from lib import *

LESSON("Basics", "What greedy means, and when it fails", """
<p>A <b>greedy</b> algorithm makes the choice that looks best <i>right now</i> and never goes back. It's simple and fast — but only correct for some problems.</p>
<p>Coins <code>[1, 3, 4]</code>, amount 6. Greedy takes the biggest coin first: 4 + 1 + 1 = <b>3 coins</b>. The best answer is 3 + 3 = <b>2 coins</b>. Greedy failed, so this problem needs DP.</p>
<p>Before trusting a greedy idea, always try to <b>break it with a small example</b>. If you can't, look for a proof (next lesson).</p>
""")


@LD
def greedy_fail_lesson():
    coins, amount = [4, 3, 1], 6
    left, used = amount, []
    for c in coins:
        while left >= c:
            left -= c
            used.append(c)
            T(f"Greedy takes the largest coin that fits: {c}, {left} left", A("coins (largest first)", coins, hl=[coins.index(c)]), A("used", used), V(left=left))
    T(f"Greedy used {len(used)} coins, but 3 + 3 needs only 2 → greedy is wrong here", A("greedy", used, bad=range(len(used))), A("optimal", [3, 3], ok=[0, 1]))
    return len(used)


LESSON("Core", "Proving a greedy: the exchange argument", """
<p>To show a greedy choice is safe, take <b>any</b> optimal answer and show you can swap one of its choices for the greedy choice without making it worse. Then some optimal answer agrees with greedy, step by step.</p>
<p>Example — <b>assign cookies</b>: give the smallest cookie that satisfies the least greedy child. If an optimal answer gives that child a bigger cookie, swapping it for the smaller one never hurts anyone else.</p>
<p>Greedy problems usually start with the right <b>sort order</b>:</p>
<ul>
<li>Two city scheduling: by <code>costA − costB</code>.</li>
<li>Maximum units on a truck: by units per box, high to low.</li>
<li>Largest number: by the rule "a before b if a + b &gt; b + a".</li>
<li>Queue by height: tallest first, then insert at index k.</li>
</ul>
""", practice=[455, 1029, 1710, 179, 406])


LESSON("Core", "Intervals: sort, then merge", """
<p>An interval is <code>[start, end]</code>. Two intervals overlap when <code>a.start &lt;= b.end</code> and <code>b.start &lt;= a.end</code>. Sorted by start, you only need to compare each interval with the last merged one:</p>
<pre><code class="py">intervals.sort()
out = [intervals[0]]
for s, e in intervals[1:]:
    if s &lt;= out[-1][1]:            # overlaps
        out[-1][1] = max(out[-1][1], e)
    else:
        out.append([s, e])</code></pre>
<p>Insert interval is the same in one pass on an already sorted list: copy the ones before, absorb the overlapping ones, copy the rest. Intersections of two sorted lists use two pointers.</p>
""", practice=[56, 57, 986])


LESSON("Core", "Scheduling: sort by end time", """
<p>"Keep as many non-overlapping intervals as possible" (or "remove as few as possible"): sort by <b>end</b> and always keep the interval that finishes first. Finishing early leaves the most room for the rest — that's the exchange argument.</p>
<pre><code class="py">intervals.sort(key=lambda x: x[1])
end, kept = -inf, 0
for s, e in intervals:
    if s &gt;= end:
        kept += 1; end = e</code></pre>
<p>Same idea: <b>minimum arrows</b> to burst balloons (shoot at the first end), and <b>covered intervals</b> (sort by start, longer first, track the farthest end).</p>
<div class="warn">Sorting by start gives the wrong answer here — a long early interval would block many short ones.</div>
""", practice=[435, 452, 1288])


@LD
def scheduling_lesson():
    meetings = [[1, 4], [2, 3], [3, 5], [4, 7], [6, 8], [5, 9]]
    meetings.sort(key=lambda x: x[1])
    end, kept = float("-inf"), []
    for i, (s, e) in enumerate(meetings):
        if s >= end:
            kept.append(i)
            end = e
            T(f"[{s},{e}] starts after {('the last end') if kept[:-1] else 'nothing'} → keep it", A("sorted by end", [f"{a}-{b}" for a, b in meetings], ok=kept, hl=[i], i=i), V(kept=len(kept), last_end=end), at="prev")
        else:
            T(f"[{s},{e}] overlaps the last kept meeting → skip", A("sorted by end", [f"{a}-{b}" for a, b in meetings], ok=kept, bad=[i], i=i), V(kept=len(kept), last_end=end))
    return len(kept)


LESSON("Core", "Reach and running balance", """
<ul>
<li><b>Jump game</b>: track the furthest index reachable so far. If you stand past it, you're stuck.</li>
<li><b>Jump game II</b>: like BFS — the current reach window is "reachable in k jumps"; the furthest point from it starts the next window.</li>
<li><b>Gas station</b>: if the tank goes negative at station i, no start between the current start and i can work — restart at i + 1.</li>
<li><b>Valid parenthesis string</b>: keep the range [lo, hi] of possible open counts.</li>
<li><b>Stock II</b>: add every positive day-to-day rise.</li>
<li><b>Lemonade change</b>: give the biggest bills first to keep small ones.</li>
</ul>
""", practice=[55, 45, 134, 678, 122, 860])


LESSON("Advanced", "Sweep lines and two passes", """
<h4>Sweep line</h4>
<p>Turn intervals into <b>events</b>: <code>+1</code> at a start, <code>−1</code> at an end. Sort events by time (ends before starts at the same time when touching doesn't overlap) and walk them with a running total. The peak is the max overlap — rooms needed, passengers in the car.</p>
<h4>Two passes</h4>
<p>When a rule involves both neighbours, satisfy one side at a time. Candy: left → right gives more than the left neighbour; right → left fixes the right neighbour while keeping the max.</p>
<h4>Last occurrence</h4>
<p>Partition labels: record each letter's last index; a part can end only when you reach the furthest last index of the letters inside it.</p>
""", practice=[1094, 135, 763])
