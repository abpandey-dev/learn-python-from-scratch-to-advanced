from lib import *

LESSON("Basics", "Images, containers and your first Dockerfile", """
<p>"Works on my machine" happens because machines differ. A <b>container image</b> packages your code with its exact runtime and libraries; a <b>container</b> is a running instance of an image, isolated from others. The same image runs on your laptop, in CI and in production.</p>
<pre><code class="py"># Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
RUN useradd --create-home app
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]</code></pre>
<pre><code class="py">docker build -t invoice-api:dev .
docker run --rm -p 8000:8000 -e APP_ENV=dev invoice-api:dev
docker ps; docker logs -f &lt;id&gt;; docker exec -it &lt;id&gt; sh</code></pre>
""", practice=["Read an Image Reference", "Port Mapping Conflicts", "Resolve ARG and ENV", "Pick a Base Image"])

LESSON("Core", "Fast, small and safe images", """
<ul>
<li><b>Layer cache:</b> each instruction is a cached layer; a change invalidates that layer and everything after. Copy the dependency list and install <i>before</i> copying source code, so code edits don't reinstall packages.</li>
<li><b>.dockerignore</b> keeps <code>.git</code>, <code>.venv</code>, data and secrets out of the build context.</li>
<li><b>Multi-stage builds</b> compile in a big image and copy only the results into a slim one.</li>
<li><b>Security:</b> pin base images (tag and ideally digest), run as a non-root user, clean package caches, never bake secrets into images, scan with Trivy or Docker Scout.</li>
</ul>
<pre><code class="py">FROM python:3.12 AS build
COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* &amp;&amp; rm -rf /wheels
COPY app/ /app/app/</code></pre>
""", practice=["Which Layers Rebuild?", "Multi-Stage Builds Shrink Images", "What Goes Into the Build Context?", "Lint a Dockerfile", "Pin Base Images by Digest", "Tag an Image for Release"])

LESSON("Core", "Running a stack with Docker Compose", """
<p>Compose describes several containers — API, database, cache, worker — in one file, with networks, volumes, environment and start order. Containers are disposable, so anything that must survive goes in a <b>volume</b>.</p>
<pre><code class="py"># compose.yaml
services:
  db:
    image: postgres:16
    environment: {POSTGRES_PASSWORD: "${DB_PASS:?set DB_PASS}"}
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck: {test: ["CMD", "pg_isready"], interval: 5s, retries: 5}
  api:
    build: .
    ports: ["8000:8000"]
    environment: {DB_URL: "postgres://postgres:${DB_PASS}@db:5432/postgres"}
    depends_on: {db: {condition: service_healthy}}
    restart: on-failure
volumes:
  pgdata:</code></pre>
<pre><code class="py">docker compose up -d --build; docker compose logs -f api; docker compose down</code></pre>
""", practice=["Compose Start Order", "Interpolate Compose Variables", "Restart Policies", "When Is a Container Unhealthy?", "Where Does the Data Go?", "Read docker compose logs"])

LESSON("Advanced", "From Docker to Kubernetes", """
<p>Kubernetes runs containers across many machines. You declare the desired state (a <b>Deployment</b> with N replicas of an image) and it keeps it true: restarting crashed containers, spreading load, rolling out new versions gradually.</p>
<ul>
<li><b>Requests and limits</b> reserve and cap CPU and memory; they also set the pod's QoS class.</li>
<li><b>Liveness</b> probes restart stuck containers; <b>readiness</b> probes stop traffic to pods that aren't ready.</li>
<li><b>Rolling updates</b> replace pods in waves controlled by <code>maxSurge</code> and <code>maxUnavailable</code>.</li>
</ul>
<pre><code class="py">kubectl apply -f deployment.yaml
kubectl get pods; kubectl logs deploy/api; kubectl rollout status deploy/api
kubectl rollout undo deploy/api          # instant rollback</code></pre>
""", practice=["Share CPUs Fairly", "Kubernetes QoS Classes", "Plan a Rolling Update", "Liveness vs Readiness Probes"])
