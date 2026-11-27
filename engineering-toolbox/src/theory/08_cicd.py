from lib import *

THEORY("CI, continuous delivery, continuous deployment", """
<table>
<tr><th>Practice</th><th>Means</th></tr>
<tr><td>Continuous integration</td><td>every change is merged often and built and tested automatically</td></tr>
<tr><td>Continuous delivery</td><td>every passing change is ready to release with one click</td></tr>
<tr><td>Continuous deployment</td><td>every passing change goes to production automatically</td></tr>
</table>
""")

THEORY("DORA metrics", """
<table>
<tr><th>Metric</th><th>Elite teams</th></tr>
<tr><td>Deployment frequency</td><td>on demand, many times a day</td></tr>
<tr><td>Lead time for changes</td><td>less than a day</td></tr>
<tr><td>Change failure rate</td><td>low, single-digit to ~15%</td></tr>
<tr><td>Time to restore service</td><td>less than an hour</td></tr>
</table>
""")

FAQ("What should a CI pipeline check?", "<p>Formatting and linting, type checks, unit tests with coverage, a build of the artefact (package or image), and security scans of dependencies and the image. Slow integration and end-to-end tests can run on merge or nightly.</p>")
FAQ("How do you speed up a slow pipeline?", "<p>Find the critical path, parallelise independent jobs, cache dependencies, shard tests, use path filters, cancel superseded runs and move slow suites out of the pull-request path.</p>")
FAQ("How do you handle secrets in CI?", "<p>Use the platform's secret store, scope secrets to environments, prefer OIDC short-lived credentials, keep token permissions minimal, and never print secrets.</p>")
FAQ("What is a matrix build?", "<p>Running the same job across combinations (Python versions, operating systems) to catch compatibility problems, with include and exclude to tailor the set.</p>")
FAQ("How do you roll back a bad deploy?", "<p>Redeploy the previous image tag (or use the platform's rollout undo), which is why images are immutable and tagged by commit; fix forward afterwards.</p>")
FAQ("Why pin actions to a SHA?", "<p>Tags can be moved to malicious code if an action's repository is compromised; a commit SHA can't change.</p>")
