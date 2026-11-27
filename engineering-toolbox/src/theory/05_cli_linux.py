from lib import *

THEORY("Commands worth knowing", """
<table>
<tr><th>Need</th><th>Command</th></tr>
<tr><td>Search text in files</td><td><code>grep -rn "pattern" dir/</code></td></tr>
<tr><td>Find files</td><td><code>find . -name "*.py" -mtime -7</code></td></tr>
<tr><td>Follow a log</td><td><code>tail -f app.log</code></td></tr>
<tr><td>Disk usage</td><td><code>df -h</code>, <code>du -sh *</code></td></tr>
<tr><td>Processes and ports</td><td><code>ps aux</code>, <code>top</code>, <code>ss -tlnp</code></td></tr>
<tr><td>Remote server</td><td><code>ssh user@host</code>, <code>scp file host:/path</code></td></tr>
<tr><td>HTTP from the terminal</td><td><code>curl -sS https://api/health</code></td></tr>
<tr><td>JSON on the command line</td><td><code>jq '.items[].id' data.json</code></td></tr>
</table>
""")

FAQ("What does chmod 755 mean?", "<p>Owner can read, write and execute (7 = 4+2+1); group and others can read and execute (5 = 4+1). Typical for scripts and directories.</p>")
FAQ("What's the difference between > and >>?", "<p><code>&gt;</code> overwrites the file with the output, <code>&gt;&gt;</code> appends. <code>2&gt;&amp;1</code> sends errors to the same place as normal output.</p>")
FAQ("What's an exit code?", "<p>A number a program returns when it ends: 0 for success, anything else for failure. Shells, CI systems and orchestrators use it to decide what happens next.</p>")
FAQ("SIGTERM vs SIGKILL?", "<p>SIGTERM asks a process to stop and can be handled to clean up; SIGKILL stops it immediately and can't be caught. Always try SIGTERM first.</p>")
FAQ("Why do environment variables matter?", "<p>They configure programs without changing code — paths, credentials, feature switches — and child processes inherit them. <code>export NAME=value</code> sets one for the session.</p>")
FAQ("How do you debug a slow server?", "<p>Check CPU and memory (<code>top</code>), disk (<code>df -h</code>, <code>iostat</code>), open connections (<code>ss</code>), recent errors in logs (<code>tail</code>, <code>grep</code>), and what changed recently.</p>")
