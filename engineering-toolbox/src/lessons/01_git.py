from lib import *
import hashlib

LESSON("Basics", "What Git actually stores", """
<p>Git is a database of <b>snapshots</b>. Every file version is stored once, named by the SHA-1 hash of its content (a <b>blob</b>); a <b>tree</b> lists the blobs in a folder; a <b>commit</b> points to one tree, its parent commit(s), the author and the message. A <b>branch</b> is just a file holding a commit id, and <code>HEAD</code> says which branch you're on.</p>
<pre><code class="py">git init                      # start a repo
git status                    # what's changed
git add app.py                # stage a snapshot of app.py
git commit -m "feat: add app" # save the staged snapshot
git log --oneline --graph     # history as a graph
git hash-object app.py        # the blob id Git uses for this content</code></pre>
<p>Because ids are content hashes, the same file in two places is stored once, and nobody can change history without every later id changing.</p>
""", practice=["Hash a File the Way Git Does", "Walk the First-Parent History", "What Changed Between Two Commits?", "Contribution Summary (shortlog)"])


@LD
def blob_demo():
    for text in ["hello\n", "hello\n", "hello!\n"]:
        data = text.encode()
        print(repr(text), "->", hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()[:12])


LESSON("Core", "Branches, merges and the merge base", """
<p>When two branches diverge, Git finds their <b>merge base</b> (the latest common ancestor) and does a <b>three-way merge</b>: a line changed on only one side takes that change; a line changed differently on both sides is a <b>conflict</b> you resolve by hand. If your branch hasn't diverged at all, Git simply <b>fast-forwards</b> the pointer.</p>
<pre><code class="py">git switch -c feature/search   # branch off main
git merge main                 # bring main's changes in (may create a merge commit)
git merge-base main feature/search
git rev-list --left-right --count main...feature/search   # behind / ahead</code></pre>
<p>Diffs are built from the <b>longest common subsequence</b> of lines — everything outside it is an addition or a deletion.</p>
""", practice=["Find the Merge Base", "Can It Fast-Forward?", "Ahead and Behind", "Count Added and Removed Lines", "A Three-Way Merge"])

LESSON("Core", "Rewriting history safely", """
<ul>
<li><b>Rebase</b> replays your commits on top of the latest main, giving a straight history. It creates <i>new</i> commits, so never rebase commits other people already pulled.</li>
<li><b>Cherry-pick</b> copies one commit's change to another branch (e.g. a hotfix to a release branch).</li>
<li><b>Stash</b> puts uncommitted work aside: <code>git stash</code>, <code>git stash list</code>, <code>git stash pop</code>.</li>
<li><b>Bisect</b> binary-searches history for the commit that broke something: about log₂(n) test runs.</li>
<li><b>Blame</b> shows who last changed each line — use it to find context, not culprits.</li>
</ul>
<pre><code class="py">git fetch origin &amp;&amp; git rebase origin/main
git rebase -i HEAD~3          # squash or reword your last 3 commits before a PR
git cherry-pick a1b2c3d
git bisect start; git bisect bad; git bisect good v1.4.0; git bisect run pytest -q</code></pre>
""", practice=["Rebase Replays Your Commits", "Cherry-Pick One Commit", "The Stash Stack", "Bisect: Find the First Bad Commit", "Who Wrote This Line? (blame)"])

LESSON("Advanced", "Working in a team", """
<p>Teams usually follow <b>trunk-based development</b>: short-lived branches, small pull requests, merged to <code>main</code> behind <b>branch protection</b> (reviews and passing checks required). Good habits:</p>
<ul>
<li>Small PRs (under ~400 lines) get reviewed faster and better.</li>
<li><b>Conventional commits</b> (<code>feat:</code>, <code>fix:</code>, <code>feat!:</code>) let tools generate changelogs and bump <b>semantic versions</b> automatically.</li>
<li>A <code>.gitignore</code> keeps build output, virtual environments and secrets out; a <b>pre-commit hook</b> scans for secrets before they ever enter history.</li>
<li>Choose a merge strategy per repo: merge commits keep full history, squash keeps main tidy, rebase keeps it linear.</li>
</ul>
<pre><code class="py">pip install pre-commit &amp;&amp; pre-commit install    # runs hooks on every commit
gh pr create --fill                             # open a PR from the terminal</code></pre>
""", practice=["Apply .gitignore Rules", "Validate Conventional Commits", "Bump the Version From Commits", "Branch Protection Rules", "Merge, Squash or Rebase?", "Catch Secrets Before You Commit"])
