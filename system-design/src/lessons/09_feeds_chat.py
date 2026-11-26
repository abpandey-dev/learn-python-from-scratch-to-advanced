from lib import *
import heapq

LESSON("Basics", "Design a news feed", """
<p><b>Requirements</b>: post, follow, see a feed of followed accounts (ranked or by time), very read-heavy, feed loads in &lt; 200 ms.</p>
<p><b>Fan-out on write</b> (push): when someone posts, a worker inserts the post id into each follower's feed list in a cache — reads are a single lookup. <b>Fan-out on read</b> (pull): at read time, fetch recent posts of everyone followed and merge — no write amplification, slower reads. A celebrity with 50 million followers makes push impossible, so real systems are <b>hybrid</b>: push for normal accounts, pull and merge for celebrities.</p>
<p>Store only post ids in feeds; hydrate the post content from a post cache. Rank with an engagement-and-recency score (or an ML model), and enforce diversity rules.</p>
""", practice=["Push or Pull: Count the Work", "Hybrid Fan-Out for Celebrities", "Merge a Pull Timeline", "Rank the Feed", "Keep the Feed Diverse", "Sharded Like Counters"])


@LD
def merge_demo():
    followed = {"asha": [(90, "a2"), (40, "a1")], "star": [(95, "s7"), (60, "s6")], "ravi": [(70, "r1")]}
    newest = heapq.merge(*followed.values(), reverse=True)
    print([pid for _, pid in newest])


LESSON("Core", "Design a chat system", """
<p><b>Real-time path</b>: clients keep a WebSocket to a chat server; a session registry (Redis) maps user → server; a message goes sender → their server → recipient's server → recipient. Offline users get a push notification and fetch messages when they return.</p>
<ul>
<li><b>Ordering</b>: the server assigns a per-conversation sequence number; clients sort by it and sync "everything after seq N" on reconnect.</li>
<li><b>Storage</b>: messages in a wide-column store (Cassandra, HBase) partitioned by conversation id, clustered by seq.</li>
<li><b>Receipts and unread counts</b> come from per-user read pointers.</li>
<li><b>Presence</b> comes from heartbeats with timeouts; throttle typing indicators.</li>
<li>Group chats fan out to each member; very large groups switch to pull.</li>
</ul>
""", practice=["Order Chat Messages", "Unread Counts", "Delivery Receipts", "Who Is Online?", "Route Messages to Connection Servers", "Group Chat Fan-Out", "How Many WebSocket Servers?", "Sync After Reconnecting", "Throttle the Typing Indicator", "How Much Chat Storage?"])

LESSON("Core", "Design a notification service", """
<p>Producers (orders, marketing, security) publish events to a queue. A notification service applies user <b>preferences</b> and <b>channels</b> (push, SMS, email), rate limits and <b>digests</b>, <b>quiet hours</b> in the user's time zone, and templates; then per-channel workers call providers (APNs, FCM, SMS gateways) with retries. Invalid device tokens are removed; every send is logged for deduplication and analytics. Critical messages (OTP) skip digests and go on a priority queue.</p>
""", practice=["Notification Digests", "Respect Quiet Hours", "Choose Notification Channels", "Handle Push-Token Responses"])
