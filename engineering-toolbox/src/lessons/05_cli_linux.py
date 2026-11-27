from lib import *

LESSON("Basics", "Moving around and reading files", """
<p>Servers, containers and CI runners have no mouse — the shell is how you work with them. A path starting with <code>/</code> is absolute; others start from the current directory; <code>~</code> is your home, <code>..</code> the parent.</p>
<pre><code class="py">pwd; ls -la; cd ~/projects/app; cd -          # where am I, what's here, go back
cat config.yaml; less app.log; head -n 20 data.csv; tail -f app.log
wc -l data.csv                                   # how many lines
cp -r src backup/; mv old.txt new.txt; mkdir -p logs/2026; rm -i tmp.txt
ls *.py; ls data/202?-*.csv                      # globs are expanded by the shell</code></pre>
<p>Every file has an owner, a group and permissions for owner/group/others: <code>-rwxr-x---</code> is <code>750</code>. Scripts need <code>x</code> to run; secrets should be <code>600</code>.</p>
""", practice=["Resolve Paths", "Match Shell Globs", "head and tail", "wc: Lines, Words, Characters", "Read ls -l Permissions", "Apply chmod Changes"])

LESSON("Core", "Pipes: small tools, combined", """
<p>Each Unix tool does one thing and reads standard input; the pipe <code>|</code> sends one tool's output into the next. Together they answer real questions in one line:</p>
<pre><code class="py">grep -c " 500 " access.log                         # how many server errors?
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head   # top client IPs
grep -rn "TODO" --include="*.py" src/              # find TODOs with line numbers
find logs -name "*.log" -size +1M -mtime +30       # big old logs
du -sh * | sort -h; df -h                          # what's using the disk</code></pre>
<p>Every command returns an <b>exit code</b> (0 = success; <code>echo $?</code> shows it). <code>a &amp;&amp; b</code> runs b only if a succeeded, <code>a || b</code> only if it failed — CI scripts rely on this, and <code>set -euo pipefail</code> makes a script stop at the first failure.</p>
""", practice=["grep With Flags", "sort | uniq -c | sort -rn | head", "cut Columns", "find Files by Name, Size and Age", "du -sh: What's Using the Disk?", "Disk Space Alerts", "Exit Codes, && and ||", "Parse an Access Log"])

LESSON("Core", "Writing your own command-line tools", """
<p>Python scripts become real tools with <code>argparse</code> (built in) or Typer/Click: positional arguments, options with defaults, flags, help text, and a non-zero exit code on error.</p>
<pre><code class="py">import argparse, sys

def main(argv=None):
    p = argparse.ArgumentParser(prog="report", description="Summarise sales files.")
    p.add_argument("inputs", nargs="+", help="CSV files to read")
    p.add_argument("--since", help="only rows on or after this date")
    p.add_argument("--format", choices=["csv", "json"], default="csv")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())

# pyproject.toml → installs a `report` command
[project.scripts]
report = "app.cli:main"</code></pre>
<p>The shell does work before your program starts: it splits the line into arguments (respecting quotes) and expands <code>$VARIABLES</code>. Quote values with spaces: <code>"$FILE"</code>.</p>
""", practice=["Build a CLI With argparse", "Split a Command Line Like the Shell", "Expand Shell Variables"])

LESSON("Advanced", "Processes, signals and scheduled jobs", """
<ul>
<li><code>ps aux</code>, <code>top</code>/<code>htop</code> show processes; each has a parent. Stop a service's children before the parent.</li>
<li><code>kill</code> sends <b>SIGTERM</b> (please finish up); after a grace period, <b>SIGKILL</b> ends it with no cleanup. Handle SIGTERM in long-running code so containers shut down cleanly.</li>
<li><b>cron</b> runs jobs on a schedule: <code>minute hour day month weekday</code>. On Kubernetes it's a CronJob; in Airflow, a schedule.</li>
</ul>
<pre><code class="py">import signal, sys
def stop(signum, frame):
    finish_current_batch(); sys.exit(0)
signal.signal(signal.SIGTERM, stop)

# crontab -e
*/15 9-17 * * 1-5  /opt/app/.venv/bin/python -m app.sync >> /var/log/sync.log 2>&1</code></pre>
""", practice=["Kill a Process Tree", "SIGTERM, Then SIGKILL", "When Does the Cron Job Run?"])
