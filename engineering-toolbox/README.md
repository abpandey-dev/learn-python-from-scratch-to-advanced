# Engineering Toolbox

8 topics · theory with 48 theory questions · 32 lessons from basics to advanced · 160 practice questions with answers · The tools every engineering job assumes on day one: Git, testing with pytest, code quality and type hints, packaging and environments, the command line and Linux, logging and configuration, Docker and CI/CD with GitHub Actions · each tool's core idea is built in plain Python so you see what it really does, with the real commands in every lesson.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Git: From Commits to Pull Requests](#git-from-commits-to-pull-requests) — What Git really stores and how it decides things: content hashes, the commit graph, merge bases, fast-forwards, ahead/behind, diffs, three-way merges, .gitignore rules, conventional commits and version bumps, bisect, rebase and cherry-pick, stash, blame, branch protection, secret scanning and shortlog.
- [Testing With pytest](#testing-with-pytest) — How testing really works and how to do it well: approximate equality, parametrize ids, fixture order and scopes, mocks, injected clocks, line and branch coverage, mutation testing, flaky tests, property-based shrinking, boundary values and partitions, test selection, the pyramid, snapshots, test smells, summaries and durations.
- [Code Quality, Linting & Type Hints](#code-quality-linting-type-hints) — Build the checks that linters and type checkers run, with Python's ast module: unused imports, complexity, long lines, naming, mutable defaults, swallowed errors, docstring and type-hint coverage, runtime type checks, import sorting, duplicates, dead code, magic numbers, long functions, whitespace, shadowed builtins, old-style formatting, line counts, layer rules and rule selection.
- [Packages, Versions & Environments](#packages-versions-environments) — What pip, uv and poetry do for you: comparing versions, matching specifiers, picking and resolving versions, reading pyproject.toml, parsing requirements and markers, wheel tags, lockfile diffs, vulnerability checks, dependency trees, conflicts, configuration precedence, .env files, PATH lookup, pinning policy, safe upgrades, install size and semantic-version API checks.
- [The Command Line & Linux](#the-command-line-linux) — The shell skills every engineer needs, rebuilt in Python: permissions and chmod, globs, paths, argparse CLIs, exit codes and &&/||, wc, sort | uniq -c, grep, head and tail, cut, cron schedules, du, find, log parsing, variable expansion, process trees, signals, disk alerts and shell quoting.
- [Logging, Metrics & Errors in Production](#logging-metrics-errors-in-production) — Make code you can run and debug in production: log levels, formats and JSON logs, logger hierarchies, rotation, error rates, request tracing, redaction, retries, exception chaining, Prometheus counters and histograms, quantiles and rates, health checks, feature flags, log sampling, alert cooldowns, error grouping, config validation and uptime.
- [Docker & Containers](#docker-containers) — Containers from the inside: image references, layer caching and instruction order, multi-stage sizes, .dockerignore, Dockerfile linting, ARG and ENV, port conflicts, compose start order and variables, restart policies, health checks, CPU and memory limits, volumes, release tags, digest pinning, compose logs, base images, and Kubernetes QoS, rolling updates and probes.
- [CI/CD With GitHub Actions](#ci-cd-with-github-actions) — Automate everything after git push: matrix builds, job graphs and critical paths, path and branch filters, cache keys, concurrency, secret masking, step conditions, check status, artifacts, workflow validation, schedules in UTC, CI minutes, test sharding, reruns, changelogs, image pushing rules, environment promotion and DORA metrics.

## Git: From Commits to Pull Requests

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Hash a File the Way Git Does](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/hash-a-file-the-way-git-does) | Easy | Content addressing |
| 2 | [Walk the First-Parent History](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/walk-the-first-parent-history) | Easy | git log --first-parent |
| 3 | [Find the Merge Base](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/find-the-merge-base) | Medium | Where two branches split |
| 4 | [Can It Fast-Forward?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/can-it-fast-forward) | Easy | Moving a branch pointer |
| 5 | [Ahead and Behind](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/ahead-and-behind) | Easy | What git status tells you |
| 6 | [Count Added and Removed Lines](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/count-added-and-removed-lines) | Medium | git diff --stat |
| 7 | [A Three-Way Merge](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/a-three-way-merge) | Medium | Base, ours, theirs |
| 8 | [Apply .gitignore Rules](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/apply-gitignore-rules) | Medium | The last matching rule wins |
| 9 | [Validate Conventional Commits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/validate-conventional-commits) | Easy | Machine-readable messages |
| 10 | [Bump the Version From Commits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/bump-the-version-from-commits) | Medium | Semantic versioning |
| 11 | [Bisect: Find the First Bad Commit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/bisect-find-the-first-bad-commit) | Medium | Binary search through history |
| 12 | [Rebase Replays Your Commits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/rebase-replays-your-commits) | Medium | New commits, same changes |
| 13 | [Cherry-Pick One Commit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/cherry-pick-one-commit) | Medium | Apply a change elsewhere |
| 14 | [The Stash Stack](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/the-stash-stack) | Easy | Put work aside |
| 15 | [Who Wrote This Line? (blame)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/who-wrote-this-line-blame) | Medium | Trace each line to its origin |
| 16 | [Branch Protection Rules](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/branch-protection-rules) | Medium | Can this PR be merged? |
| 17 | [Merge, Squash or Rebase?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/merge-squash-or-rebase) | Easy | What lands on main |
| 18 | [Catch Secrets Before You Commit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/catch-secrets-before-you-commit) | Medium | A pre-commit hook |
| 19 | [What Changed Between Two Commits?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/what-changed-between-two-commits) | Medium | git diff --name-status |
| 20 | [Contribution Summary (shortlog)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/git/contribution-summary-shortlog) | Easy | Who did what |

## Testing With pytest

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Compare Floats Like pytest.approx](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/compare-floats-like-pytest-approx) | Easy | Never use == on floats |
| 2 | [Parametrize: Generate Test Ids](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/parametrize-generate-test-ids) | Easy | One test, many cases |
| 3 | [Fixture Setup and Teardown Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/fixture-setup-and-teardown-order) | Medium | Dependencies first, cleanup in reverse |
| 4 | [How Often Does Each Fixture Run?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/how-often-does-each-fixture-run) | Medium | Fixture scopes |
| 5 | [Mock a Dependency and Check the Calls](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/mock-a-dependency-and-check-the-calls) | Medium | Test behaviour without sending real email |
| 6 | [Inject the Clock](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/inject-the-clock) | Easy | Make time testable |
| 7 | [Line Coverage and Missing Lines](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/line-coverage-and-missing-lines) | Medium | pytest --cov --cov-report=term-missing |
| 8 | [Branch Coverage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/branch-coverage) | Easy | Did both sides of each if run? |
| 9 | [Mutation Testing: Are Your Tests Any Good?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/mutation-testing-are-your-tests-any-good) | Medium | Tests that catch small bugs |
| 10 | [Find the Flaky Tests](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/find-the-flaky-tests) | Easy | Same code, different result |
| 11 | [Shrink a Failing Example](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/shrink-a-failing-example) | Hard | Property-based testing (Hypothesis) |
| 12 | [Boundary Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/boundary-values) | Easy | Bugs live at the edges |
| 13 | [Equivalence Partitions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/equivalence-partitions) | Easy | One test per kind of input |
| 14 | [Run Only the Affected Tests](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/run-only-the-affected-tests) | Medium | Fast feedback in big repos |
| 15 | [Check the Test Pyramid](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/check-the-test-pyramid) | Easy | Many fast tests, few slow ones |
| 16 | [Snapshot Testing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/snapshot-testing) | Medium | Catch unexpected output changes |
| 17 | [Spot Test Smells](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/spot-test-smells) | Medium | Read tests with the ast module |
| 18 | [Write the Summary Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/write-the-summary-line) | Easy | What pytest prints at the end |
| 19 | [Should You Retry Flaky Tests?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/should-you-retry-flaky-tests) | Medium | Odds of a red build |
| 20 | [Find the Slowest Tests](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/testing/find-the-slowest-tests) | Easy | pytest --durations=3 |

## Code Quality, Linting & Type Hints

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Find Unused Imports](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/find-unused-imports) | Medium | Ruff F401 |
| 2 | [Cyclomatic Complexity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/cyclomatic-complexity) | Medium | How many paths through a function? |
| 3 | [Lines Too Long](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/lines-too-long) | Easy | E501 |
| 4 | [Check Naming Conventions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/check-naming-conventions) | Easy | PEP 8 names |
| 5 | [Mutable Default Arguments](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/mutable-default-arguments) | Easy | Bugbear B006 |
| 6 | [Swallowed Exceptions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/swallowed-exceptions) | Medium | Errors that vanish |
| 7 | [Docstring Coverage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/docstring-coverage) | Easy | interrogate |
| 8 | [Type Hint Coverage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/type-hint-coverage) | Easy | How much of the code is typed? |
| 9 | [Check Call Arguments Against Hints](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/check-call-arguments-against-hints) | Medium | What mypy and pydantic catch |
| 10 | [Sort Imports Like isort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/sort-imports-like-isort) | Medium | Three groups, alphabetical |
| 11 | [Find Duplicated Code](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/find-duplicated-code) | Medium | Copy-paste detection |
| 12 | [Unreachable Code](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/unreachable-code) | Easy | Statements after return |
| 13 | [Magic Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/magic-numbers) | Easy | Name your constants |
| 14 | [Functions That Do Too Much](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/functions-that-do-too-much) | Easy | Size limits |
| 15 | [Whitespace Problems](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/whitespace-problems) | Easy | W291, W292, W391 |
| 16 | [Shadowed Builtins](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/shadowed-builtins) | Easy | Don't name a variable list |
| 17 | [Old-Style String Formatting](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/old-style-string-formatting) | Easy | Use f-strings |
| 18 | [Count Lines of Code](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/count-lines-of-code) | Easy | cloc |
| 19 | [Enforce Architecture Layers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/enforce-architecture-layers) | Medium | import-linter |
| 20 | [Which Lint Rules Are On?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/code-quality/which-lint-rules-are-on) | Medium | select and ignore |

## Packages, Versions & Environments

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Sort Versions Correctly](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/sort-versions-correctly) | Easy | 1.10 comes after 1.9 |
| 2 | [Does the Version Match?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/does-the-version-match) | Medium | Version specifiers |
| 3 | [Pick the Newest Allowed Version](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/pick-the-newest-allowed-version) | Easy | What pip install chooses |
| 4 | [Resolve Dependencies](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/resolve-dependencies) | Hard | Backtracking like pip and uv |
| 5 | [Read pyproject.toml](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/read-pyproject-toml) | Easy | The modern project file |
| 6 | [Parse a Requirement Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/parse-a-requirement-line) | Medium | name[extras] spec ; marker |
| 7 | [Evaluate Environment Markers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/evaluate-environment-markers) | Medium | Install this only on Linux, Python < 3.11 |
| 8 | [Read a Wheel Filename](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/read-a-wheel-filename) | Medium | Will this wheel install here? |
| 9 | [What Changed in the Lockfile?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/what-changed-in-the-lockfile) | Easy | Review dependency updates |
| 10 | [Find Vulnerable Packages](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/find-vulnerable-packages) | Medium | pip-audit |
| 11 | [Measure the Dependency Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/measure-the-dependency-tree) | Medium | uv tree |
| 12 | [Why Is This Package Installed?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/why-is-this-package-installed) | Medium | Reverse dependencies |
| 13 | [Spot Version Conflicts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/spot-version-conflicts) | Medium | Two packages want different things |
| 14 | [Configuration Precedence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/configuration-precedence) | Medium | Defaults < file < env < flags |
| 15 | [Parse a .env File](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/parse-a-env-file) | Medium | Twelve-factor config |
| 16 | [Which python Runs?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/which-python-runs) | Easy | PATH and virtual environments |
| 17 | [Pin, Range or Unbounded?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/pin-range-or-unbounded) | Easy | Apps pin, libraries range |
| 18 | [Safe Automatic Upgrades](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/safe-automatic-upgrades) | Medium | Dependabot and Renovate policies |
| 19 | [How Big Is the Environment?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/how-big-is-the-environment) | Easy | Shared dependencies count once |
| 20 | [Is This Release Breaking?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/packaging/is-this-release-breaking) | Medium | Semantic versioning for libraries |

## The Command Line & Linux

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Read ls -l Permissions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/read-ls-l-permissions) | Easy | rwx to octal |
| 2 | [Apply chmod Changes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/apply-chmod-changes) | Medium | u+x, go-w, a=r |
| 3 | [Match Shell Globs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/match-shell-globs) | Easy | *, ? and [abc] |
| 4 | [Resolve Paths](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/resolve-paths) | Medium | cd, ., .. and ~ |
| 5 | [Build a CLI With argparse](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/build-a-cli-with-argparse) | Medium | Options, flags and arguments |
| 6 | [Exit Codes, && and ||](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/exit-codes-and) | Medium | How the shell chains commands |
| 7 | [wc: Lines, Words, Characters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/wc-lines-words-characters) | Easy | Counting text |
| 8 | [sort | uniq -c | sort -rn | head](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/sort-uniq-c-sort-rn-head) | Easy | The classic count pipeline |
| 9 | [grep With Flags](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/grep-with-flags) | Easy | -i, -v, -n, -c |
| 10 | [head and tail](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/head-and-tail) | Easy | Slices of a file |
| 11 | [cut Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/cut-columns) | Easy | cut -d, -f2,4 |
| 12 | [When Does the Cron Job Run?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/when-does-the-cron-job-run) | Medium | minute hour day month weekday |
| 13 | [du -sh: What's Using the Disk?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/du-sh-whats-using-the-disk) | Easy | Sizes by folder |
| 14 | [find Files by Name, Size and Age](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/find-files-by-name-size-and-age) | Easy | find . -name -size -mtime |
| 15 | [Parse an Access Log](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/parse-an-access-log) | Medium | Regex on real log lines |
| 16 | [Expand Shell Variables](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/expand-shell-variables) | Medium | $VAR, ${VAR} and ${VAR:-default} |
| 17 | [Kill a Process Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/kill-a-process-tree) | Medium | Children first |
| 18 | [SIGTERM, Then SIGKILL](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/sigterm-then-sigkill) | Easy | Graceful shutdown |
| 19 | [Disk Space Alerts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/disk-space-alerts) | Easy | df -h |
| 20 | [Split a Command Line Like the Shell](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cli-linux/split-a-command-line-like-the-shell) | Medium | Quotes and escapes |

## Logging, Metrics & Errors in Production

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Which Messages Get Logged?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/which-messages-get-logged) | Easy | Log levels |
| 2 | [Format Log Lines](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/format-log-lines) | Easy | %(levelname)-8s and friends |
| 3 | [Structured JSON Logs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/structured-json-logs) | Medium | Logs machines can query |
| 4 | [The Logger Hierarchy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/the-logger-hierarchy) | Medium | Effective levels |
| 5 | [Rotate Log Files by Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/rotate-log-files-by-size) | Medium | RotatingFileHandler |
| 6 | [Error Rate per Minute](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/error-rate-per-minute) | Easy | From logs to a metric |
| 7 | [Follow a Request Across Services](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/follow-a-request-across-services) | Medium | Correlation ids |
| 8 | [Redact Personal Data From Logs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/redact-personal-data-from-logs) | Medium | Privacy by default |
| 9 | [Retry With Backoff](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/retry-with-backoff) | Medium | Transient failures |
| 10 | [Wrap Errors With Context](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/wrap-errors-with-context) | Medium | raise … from … |
| 11 | [A Prometheus Histogram](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/a-prometheus-histogram) | Medium | Buckets, sum and count |
| 12 | [Estimate a Percentile From Buckets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/estimate-a-percentile-from-buckets) | Medium | histogram_quantile |
| 13 | [Rate From a Counter With Resets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/rate-from-a-counter-with-resets) | Medium | Why rate() handles restarts |
| 14 | [Aggregate Health Checks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/aggregate-health-checks) | Easy | /health for a load balancer |
| 15 | [Roll Out a Feature Flag](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/roll-out-a-feature-flag) | Medium | Percentage rollouts |
| 16 | [Sample Logs, Keep Every Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/sample-logs-keep-every-error) | Easy | Cut log costs safely |
| 17 | [Alert Without Spamming](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/alert-without-spamming) | Easy | Cooldowns |
| 18 | [Group Errors Like Sentry](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/group-errors-like-sentry) | Medium | Fingerprints |
| 19 | [Validate Configuration at Startup](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/validate-configuration-at-startup) | Medium | Fail fast |
| 20 | [Uptime From Health Checks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/logging/uptime-from-health-checks) | Easy | Availability and outages |

## Docker & Containers

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Read an Image Reference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/read-an-image-reference) | Easy | registry/namespace/name:tag@digest |
| 2 | [Which Layers Rebuild?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/which-layers-rebuild) | Medium | Order your Dockerfile for the cache |
| 3 | [Multi-Stage Builds Shrink Images](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/multi-stage-builds-shrink-images) | Easy | Ship only what runs |
| 4 | [What Goes Into the Build Context?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/what-goes-into-the-build-context) | Medium | .dockerignore |
| 5 | [Lint a Dockerfile](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/lint-a-dockerfile) | Medium | hadolint-style rules |
| 6 | [Resolve ARG and ENV](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/resolve-arg-and-env) | Medium | Build-time vs run-time variables |
| 7 | [Port Mapping Conflicts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/port-mapping-conflicts) | Easy | -p host:container |
| 8 | [Compose Start Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/compose-start-order) | Medium | depends_on with health checks |
| 9 | [Interpolate Compose Variables](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/interpolate-compose-variables) | Medium | ${VAR:-default} and ${VAR:?error} |
| 10 | [Restart Policies](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/restart-policies) | Medium | no, on-failure, always |
| 11 | [When Is a Container Unhealthy?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/when-is-a-container-unhealthy) | Medium | HEALTHCHECK settings |
| 12 | [Share CPUs Fairly](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/share-cpus-fairly) | Hard | Limits and contention |
| 13 | [Where Does the Data Go?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/where-does-the-data-go) | Medium | Volumes, bind mounts and the container layer |
| 14 | [Tag an Image for Release](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/tag-an-image-for-release) | Easy | Traceable tags |
| 15 | [Pin Base Images by Digest](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/pin-base-images-by-digest) | Easy | Reproducible builds |
| 16 | [Read docker compose logs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/read-docker-compose-logs) | Easy | Interleave by time |
| 17 | [Pick a Base Image](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/pick-a-base-image) | Easy | Smallest that works |
| 18 | [Kubernetes QoS Classes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/kubernetes-qos-classes) | Easy | Who gets evicted first? |
| 19 | [Plan a Rolling Update](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/plan-a-rolling-update) | Medium | maxSurge and maxUnavailable |
| 20 | [Liveness vs Readiness Probes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/docker/liveness-vs-readiness-probes) | Medium | Restart or stop sending traffic? |

## CI/CD With GitHub Actions

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Expand a Build Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/expand-a-build-matrix) | Medium | strategy.matrix |
| 2 | [Job Waves and the Critical Path](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/job-waves-and-the-critical-path) | Medium | needs: |
| 3 | [Which Workflows Run for This Change?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/which-workflows-run-for-this-change) | Medium | on.push.paths |
| 4 | [Cache Hits, Partial Hits and Misses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/cache-hits-partial-hits-and-misses) | Medium | actions/cache keys |
| 5 | [Cancel Superseded Runs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/cancel-superseded-runs) | Medium | concurrency: cancel-in-progress |
| 6 | [Mask Secrets in Logs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/mask-secrets-in-logs) | Easy | *** in the job output |
| 7 | [Which Steps Run?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/which-steps-run) | Medium | if: success(), failure(), always() |
| 8 | [Can the Pull Request Merge Yet?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/can-the-pull-request-merge-yet) | Easy | Combined check status |
| 9 | [Validate a Workflow](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/validate-a-workflow) | Medium | Catch mistakes before pushing |
| 10 | [Scheduled Workflows Run in UTC](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/scheduled-workflows-run-in-utc) | Easy | Convert cron times |
| 11 | [What Does CI Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/what-does-ci-cost) | Easy | Runner minutes |
| 12 | [Split Tests Across Shards](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/split-tests-across-shards) | Medium | Parallel test jobs |
| 13 | [Re-run Only Failed Jobs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/re-run-only-failed-jobs) | Easy | Save time on flaky failures |
| 14 | [Generate a Changelog](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/generate-a-changelog) | Medium | From conventional commits |
| 15 | [Should This Run Push an Image?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/should-this-run-push-an-image) | Easy | Build everywhere, publish carefully |
| 16 | [Promote Through Environments](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/promote-through-environments) | Medium | dev → staging → prod |
| 17 | [Measure Delivery: DORA Metrics](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/measure-delivery-dora-metrics) | Medium | How good is your delivery pipeline? |
| 18 | [Pass Files Between Jobs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/pass-files-between-jobs) | Easy | upload-artifact / download-artifact |
| 19 | [Pin Third-Party Actions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/pin-third-party-actions) | Easy | Supply-chain safety |
| 20 | [Least-Privilege Token Permissions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/#/q/cicd/least-privilege-token-permissions) | Medium | permissions: |

## Build

```bash
python3 handbook/build.py --book engineering-toolbox
```

Sources live in `engineering-toolbox/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
