from lib import *

THEORY("Push vs pull vs hybrid", """
<table>
<tr><th></th><th>Push (write)</th><th>Pull (read)</th><th>Hybrid</th></tr>
<tr><td>Read cost</td><td>one lookup</td><td>merge many lists</td><td>lookup + few merges</td></tr>
<tr><td>Write cost</td><td>followers × posts</td><td>one insert</td><td>bounded</td></tr>
<tr><td>Celebrity</td><td>breaks</td><td>fine</td><td>pulled</td></tr>
<tr><td>Inactive users</td><td>wasted work</td><td>free</td><td>push only to active</td></tr>
</table>
""")

FAQ("How do you handle the celebrity problem?", "<p>Don't fan out their posts. Push posts from normal accounts into feeds; at read time merge in recent posts from the few celebrities the user follows, cached aggressively.</p>")
FAQ("How do you keep chat messages in order?", "<p>A per-conversation sequence number assigned by the server (or the partition leader for that conversation). Clients order by it and detect gaps to re-fetch.</p>")
FAQ("How does a message reach a user on another server?", "<p>Look up the recipient's connection server in the session registry and forward the message (directly or through pub/sub); if they're offline, store it and send a push notification.</p>")
FAQ("Why WebSockets for chat?", "<p>They keep one two-way connection open, so the server can push messages instantly without polling. Use HTTP for history, uploads and other request/response work.</p>")
FAQ("How would you avoid spamming users with notifications?", "<p>Per-user rate limits, digests, deduplication, preference and quiet-hours checks, and priority levels so only critical messages bypass them.</p>")
FAQ("Where do you store the feed?", "<p>Precomputed feeds of post ids in a cache (Redis lists, trimmed to a few hundred), backed by a database for rebuilding; post bodies in a separate post store and cache.</p>")
