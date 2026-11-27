from lib import *

THEORY("Commands you'll use every day", """
<table>
<tr><th>Goal</th><th>Command</th></tr>
<tr><td>Undo unstaged changes to a file</td><td><code>git restore app.py</code></td></tr>
<tr><td>Unstage a file</td><td><code>git restore --staged app.py</code></td></tr>
<tr><td>Fix the last commit message</td><td><code>git commit --amend</code></td></tr>
<tr><td>Undo a pushed commit safely</td><td><code>git revert &lt;id&gt;</code></td></tr>
<tr><td>Throw away local commits (careful)</td><td><code>git reset --hard origin/main</code></td></tr>
<tr><td>Find a lost commit</td><td><code>git reflog</code></td></tr>
<tr><td>See who changed a line</td><td><code>git blame -L 10,20 app.py</code></td></tr>
</table>
""")

THEORY("Merge vs rebase", """
<table>
<tr><th></th><th>Merge</th><th>Rebase</th></tr>
<tr><td>History</td><td>true, with merge commits</td><td>linear, rewritten</td></tr>
<tr><td>Safe on shared branches</td><td>yes</td><td>no — rewrites commits</td></tr>
<tr><td>Conflicts</td><td>resolved once</td><td>possibly once per commit</td></tr>
</table>
""")

FAQ("What's the difference between git fetch and git pull?", "<p><code>fetch</code> downloads new commits without touching your branch; <code>pull</code> is fetch followed by a merge (or rebase with <code>--rebase</code>) into your current branch.</p>")
FAQ("How do you resolve a merge conflict?", "<p>Open the files with conflict markers, decide the correct combined code (not just one side), remove the markers, run the tests, then <code>git add</code> and continue the merge or rebase.</p>")
FAQ("You committed a password. What now?", "<p>Rotate the secret immediately — assume it's compromised. Then remove it from history (git filter-repo or BFG) and force-push, and add a secret-scanning pre-commit hook.</p>")
FAQ("revert vs reset?", "<p><code>revert</code> adds a new commit that undoes an old one — safe for shared history. <code>reset</code> moves the branch pointer back, discarding commits — only for local work.</p>")
FAQ("What makes a good pull request?", "<p>Small and focused, a clear title and description of why, tests included, CI passing, and screenshots or examples when behaviour changes.</p>")
FAQ("What is semantic versioning?", "<p>MAJOR.MINOR.PATCH: bump major for breaking changes, minor for new backwards-compatible features, patch for backwards-compatible fixes.</p>")
