from lib import *

THEORY("Container vs virtual machine", """
<table>
<tr><th></th><th>Container</th><th>Virtual machine</th></tr>
<tr><td>Isolation</td><td>shares the host kernel</td><td>own kernel and OS</td></tr>
<tr><td>Start time</td><td>milliseconds to seconds</td><td>tens of seconds to minutes</td></tr>
<tr><td>Size</td><td>MBs</td><td>GBs</td></tr>
<tr><td>Use</td><td>packaging and running apps</td><td>strong isolation, different OSes</td></tr>
</table>
""")

THEORY("CMD vs ENTRYPOINT, COPY vs ADD", """
<ul>
<li><b>ENTRYPOINT</b> is the program that always runs; <b>CMD</b> supplies default arguments you can override at <code>docker run</code>.</li>
<li><b>COPY</b> copies local files; <b>ADD</b> can also fetch URLs and unpack archives — prefer COPY for clarity.</li>
<li>Use the JSON form <code>CMD ["python", "app.py"]</code> so signals reach your process.</li>
</ul>
""")

FAQ("Why is my image so big?", "<p>A full base image, build tools left in, package caches, copying .git or data into the context, or many layers of deleted files. Use slim bases, multi-stage builds, .dockerignore and --no-cache-dir.</p>")
FAQ("Why does a tiny code change rebuild everything?", "<p>An early COPY of the whole project invalidates every later layer. Copy and install dependencies first, then copy source code.</p>")
FAQ("How do you keep data when a container is removed?", "<p>Store it in a named volume or a bind mount; the container's writable layer is deleted with the container.</p>")
FAQ("How should secrets reach a container?", "<p>At runtime via environment variables from a secret store, mounted secret files, or BuildKit secrets during builds — never baked into an image layer.</p>")
FAQ("Liveness vs readiness probe?", "<p>Liveness failing means the container is broken and gets restarted; readiness failing means it's alive but shouldn't receive traffic yet (warming up, dependency down).</p>")
FAQ("Docker Compose or Kubernetes?", "<p>Compose for local development and small single-host deployments; Kubernetes when you need many machines, self-healing, autoscaling and rolling deploys.</p>")
