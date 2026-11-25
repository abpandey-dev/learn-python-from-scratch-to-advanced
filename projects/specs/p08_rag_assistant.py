import pandas as pd

ARTICLES = [
    ("KB01", "Return policy", "You can return most items within 10 days of delivery. Items must be unused, with the original tags and packaging.\n\nGroceries, beauty products that have been opened, and innerwear cannot be returned for hygiene reasons. Electronics can be returned only if they are faulty or damaged on arrival."),
    ("KB02", "How to start a return", "Open My Orders in the app, choose the item and tap Return. Pick a reason and a pickup slot.\n\nOur courier collects the item from your address. Keep the item packed and ready, with the return label printed or written on the package. You will get an SMS when the pickup is done."),
    ("KB03", "Refund timelines", "Refunds start after the returned item passes a quality check at our warehouse, usually within 2 days of pickup.\n\nMoney goes back to the original payment method. UPI and wallet refunds arrive within 24 hours. Card refunds take 5 to 7 business days. Cash on delivery orders are refunded to your ShopKart wallet or a bank account you add."),
    ("KB04", "Delivery times", "Standard delivery takes 3 to 5 days in metro cities and 5 to 8 days elsewhere. Express delivery, available in 40 cities, delivers the next day if you order before 2 pm.\n\nDelivery dates are shown on the product page after you enter your pincode."),
    ("KB05", "Delivery charges", "Delivery is free on orders above Rs 499. Orders below that have a Rs 40 delivery fee. Express delivery costs Rs 99 extra, and is free for ShopKart Plus members.\n\nBulky items such as furniture may have an extra handling charge, shown at checkout."),
    ("KB06", "Tracking an order", "Go to My Orders and tap the order to see live tracking. You will also get SMS and email updates when the order is packed, shipped and out for delivery.\n\nIf tracking has not changed for 3 days, contact support and we will raise a query with the courier."),
    ("KB07", "Cancelling an order", "You can cancel an order for free until it is shipped. Open My Orders, tap the order and choose Cancel.\n\nAfter the order has shipped you cannot cancel it, but you can refuse the delivery or return it after it arrives. Prepaid cancellations are refunded within 24 hours to UPI and wallets."),
    ("KB08", "Payment methods", "We accept UPI, credit and debit cards, net banking, ShopKart wallet and cash on delivery.\n\nCash on delivery is available for orders up to Rs 10,000 and is not available for gift cards. EMI is available on credit cards for orders above Rs 3,000."),
    ("KB09", "Failed payment but money deducted", "If your payment failed but money was deducted, do not pay again right away. The bank usually reverses the amount automatically within 5 to 7 business days.\n\nIf the order was actually placed, you will see it in My Orders within 30 minutes. If not, the amount is returned to your account by your bank."),
    ("KB10", "ShopKart Plus membership", "ShopKart Plus costs Rs 999 a year. Members get free express delivery, early access to sales and 5 percent extra cashback on the ShopKart credit card.\n\nYou can cancel Plus within 14 days for a full refund if you have not used any benefit."),
    ("KB11", "Warranty and repairs", "Most electronics come with a manufacturer warranty of 1 year. The warranty card or invoice in your order is your proof of purchase.\n\nFor repairs, contact the brand's service centre listed on the warranty card. ShopKart does not repair products, but we can help you find the nearest service centre."),
    ("KB12", "Damaged or wrong item received", "If you receive a damaged, defective or wrong item, report it within 48 hours of delivery from My Orders. Upload clear photos of the item and the package.\n\nWe will arrange a free replacement or a full refund. You do not need to pay any return fee for these cases."),
    ("KB13", "Changing the delivery address", "You can change the delivery address only before the order is shipped. Open the order and tap Change Address.\n\nAfter shipping, the address cannot be changed. You can ask the courier to hold the parcel at the nearest pickup point instead."),
    ("KB14", "Account and password", "To reset your password, tap Forgot Password on the login screen and enter your registered mobile number. We send a one-time password by SMS.\n\nShopKart staff will never ask for your password or OTP. Do not share them with anyone, even if they say they are from ShopKart."),
    ("KB15", "Deleting your account", "You can delete your account from Settings, then Privacy, then Delete Account. Pending orders and refunds must be completed first.\n\nAfter deletion, your order history and wallet balance cannot be recovered. We keep invoices for 8 years as required by tax law."),
    ("KB16", "Gift cards", "ShopKart gift cards are valid for 1 year from the date of purchase and can be used for any product except other gift cards.\n\nGift cards cannot be exchanged for cash. If an order paid with a gift card is returned, the amount goes back to the gift card balance."),
    ("KB17", "Coupons and offers", "Only one coupon can be applied per order. Coupons are not valid on gift cards or on items already marked as deal of the day.\n\nIf you return part of an order that used a coupon, the refund is reduced in proportion to the coupon discount."),
    ("KB18", "Contacting customer support", "Chat with support 24 hours a day from Help in the app. Phone support is available from 8 am to 10 pm on 1800 123 4567, free of charge.\n\nFor complaints that are not resolved in 7 days, you can write to our grievance officer at grievance@shopkart.example."),
]

QUESTIONS = [
    ("How many days do I have to return a shirt?", "KB01"), ("Can I return an opened face cream?", "KB01"),
    ("Can I send back headphones that work fine?", "KB01"), ("How do I request a pickup for my return?", "KB02"),
    ("When will I get my money back on my credit card?", "KB03"), ("My return was picked up, when does the refund start?", "KB03"),
    ("I paid cash on delivery, how do I get a refund?", "KB03"), ("How long does delivery take to a small town?", "KB04"),
    ("Can I get my order tomorrow?", "KB04"), ("Is shipping free?", "KB05"), ("How much is express shipping?", "KB05"),
    ("Where is my package?", "KB06"), ("Tracking has not updated for days, what should I do?", "KB06"),
    ("Can I cancel my order after it has shipped?", "KB07"), ("Is cash on delivery allowed for a 15000 rupee phone?", "KB08"),
    ("Can I pay in EMI?", "KB08"), ("Money was debited but payment failed", "KB09"),
    ("What do I get with Plus membership?", "KB10"), ("How do I cancel my Plus subscription and get a refund?", "KB10"),
    ("My laptop stopped working after 3 months, who repairs it?", "KB11"), ("I received a broken product", "KB12"),
    ("They sent me the wrong colour", "KB12"), ("Can I change my address after shipping?", "KB13"),
    ("I forgot my password", "KB14"), ("Someone called asking for my OTP", "KB14"), ("How do I close my account?", "KB15"),
    ("When does a gift card expire?", "KB16"), ("Can I use two coupons on one order?", "KB17"),
    ("What is the customer care phone number?", "KB18"), ("My complaint is not solved, who do I escalate to?", "KB18"),
]


def make_data(rng):
    return {"kb_articles.csv": pd.DataFrame(ARTICLES, columns=["doc_id", "title", "text"]),
            "kb_questions.csv": pd.DataFrame(QUESTIONS, columns=["question", "doc_id"])}


CLAUDE_CODE = '''
# Optional: generate the final answer with Claude.
# Needs an Anthropic API key (console.anthropic.com) — this costs a little money per call.
#   pip install anthropic   and set the ANTHROPIC_API_KEY environment variable (in Colab: Secrets).
import os, importlib.util
if os.environ.get("ANTHROPIC_API_KEY") and importlib.util.find_spec("anthropic"):
    import anthropic
    client = anthropic.Anthropic()
    question = "Can I return headphones that work fine?"
    prompt = build_prompt(question, retrieve_better(question, 3))
    message = client.messages.create(
        model="claude-haiku-5-5",        # fast and cheap; try "claude-opus-5-5" for the strongest answers
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    print(message.content[0].text)
else:
    print("No API key or anthropic package — skipping the LLM call. Your retrieval and prompt are the hard part, and they're done.")
'''

PROJECT = dict(
    slug="support-rag-assistant",
    title="Customer-Support Assistant with RAG",
    role="AI Engineer",
    level="Advanced",
    hours="8–10",
    summary="Build the retrieval half of an LLM support bot over a company help centre: chunking, BM25 search written from scratch, retrieval evaluation, query improvements, a grounded prompt with citations, and an optional Claude call.",
    skills=["RAG", "chunking", "BM25", "retrieval evaluation", "hit@k / MRR", "query expansion", "prompt design", "grounded answers", "Claude API"],
    brief="""
**The situation.** *ShopKart*'s support team answers the same questions all day: returns, refunds, delivery, payments. They want an assistant that answers customers **from the help-centre articles only**, cites the article it used, and says "I don't know" rather than inventing a policy.

That's **retrieval-augmented generation (RAG)**: find the right passages, then ask an LLM to answer using only them. Most RAG failures are retrieval failures — the model can't use a passage it was never given — so that's where you'll spend your effort, and you'll measure it properly with a labelled test set.
""",
    deliverable="a chunked knowledge base, a BM25 retriever written by hand, a retrieval evaluation (hit@1, hit@3, MRR), an improved retriever with before/after numbers, a grounded prompt with citations, an extractive fallback answerer, and (optionally) answers from Claude.",
    data_notes="""
**kb_articles.csv** — 18 help-centre articles: doc_id, title, text (paragraphs separated by a blank line)

**kb_questions.csv** — 30 real-style customer questions with the article that answers them (doc_id): your **evaluation set**. Never tune on what you'll report — in a real project you'd keep part of it hidden.
""",
    setup="""
import re
from collections import Counter
kb = load("kb_articles.csv")
questions = load("kb_questions.csv")
STOP = set("a an the is are was were be to of and or in on at for with my i me you your do does did can how what when where who which it this that from by as if after before not no any have has get".split())
SYNONYMS = {"money": ["refund"], "back": ["return", "refund"], "shipping": ["delivery"], "ship": ["delivery"],
            "package": ["order", "tracking"], "parcel": ["order", "tracking"], "broken": ["damaged", "defective"],
            "close": ["delete", "deletion"], "debited": ["deducted", "payment"], "escalate": ["grievance", "complaint"],
            "phone": ["support", "call"], "care": ["support"], "tomorrow": ["express", "next", "day"],
            "headphones": ["electronics"], "laptop": ["electronics", "warranty"], "cream": ["beauty", "opened"],
            "otp": ["password"], "expire": ["valid"], "colour": ["wrong", "item"], "pickup": ["return", "courier"]}


def tokens(text):
    # lower-case words without stop words — used by every retriever
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


# Used by later milestones and the checks (they call the functions you write).
def retrieve_better(question, k=3):
    chunks = chunk(kb)
    ids = make_better_search(chunks)(question, k)
    return chunks.set_index("chunk_id").loc[ids].reset_index()


def prompt_rules_ok(question):
    chunks = retrieve_better(question, 5)
    p = build_prompt(question, chunks, max_words=120)
    src = p.split("Sources:")[1].split("Customer question:")[0]
    return ["I don't know based on the help centre." in p, f"[{chunks.doc_id[0]}]" in src,
            len(src.split()) <= 120, p.rstrip().endswith(question)]
""",
    milestones=[
        dict(title="Chunk the knowledge base",
             task="""
LLMs need short, focused passages. Write `chunk(kb, max_words=30)` returning a DataFrame with columns `chunk_id`, `doc_id`, `title`, `text`:
- split each article into paragraphs on blank lines,
- if a paragraph has more than `max_words` words, split it into consecutive pieces of at most `max_words` words,
- `chunk_id` = `"<doc_id>-<n>"` with n counting from 1 within each article.
""",
             starter="""
def chunk(kb, max_words=30):
    raise NotImplementedError
""",
             solution="""
def chunk(kb, max_words=30):
    rows = []
    for doc_id, title, text in kb[["doc_id", "title", "text"]].itertuples(index=False):
        n = 0
        for para in text.split("\\n\\n"):
            words = para.split()
            for start in range(0, len(words), max_words):
                n += 1
                rows.append((f"{doc_id}-{n}", doc_id, title, " ".join(words[start:start + max_words])))
    return pd.DataFrame(rows, columns=["chunk_id", "doc_id", "title", "text"])
""",
             call="[len(chunk(kb)), int(chunk(kb).groupby('doc_id').size().max()), chunk(kb)['chunk_id'].tolist()[:4]]", tol=1e-9),
        dict(title="BM25 search, from scratch",
             task="""
**BM25** is the classic keyword ranking behind search engines, and still a strong first stage in RAG. For a query q and chunk d:

score(d) = Σ over query terms t of IDF(t) × f(t, d) × (k₁ + 1) / (f(t, d) + k₁ × (1 − b + b × |d| / avgdl))

with IDF(t) = ln(1 + (N − n(t) + 0.5) / (n(t) + 0.5)), f = term count in the chunk, |d| = chunk length in tokens, avgdl = average length, N = number of chunks, n(t) = chunks containing t, k₁ = 1.5, b = 0.75.

Write `make_bm25(chunks)` returning a function `search(query, k)` that returns the top-k `chunk_id`s (ties: earlier chunk first). Use `tokens()` for both chunks and queries.
""",
             hint="Precompute token Counters per chunk, the lengths, and document frequencies. Score in a loop, then sort by (−score, position).",
             starter="""
def make_bm25(chunks, k1=1.5, b=0.75):
    def search(query, k):
        raise NotImplementedError
    return search
""",
             solution="""
def make_bm25(chunks, k1=1.5, b=0.75):
    docs = [Counter(tokens(t)) for t in chunks["text"]]
    lengths = [sum(d.values()) for d in docs]
    avgdl = sum(lengths) / len(lengths)
    N = len(docs)
    df = Counter(t for d in docs for t in d)
    idf = {t: math.log(1 + (N - n + 0.5) / (n + 0.5)) for t, n in df.items()}
    ids = chunks["chunk_id"].tolist()

    def search(query, k):
        q = tokens(query)
        scores = []
        for i, d in enumerate(docs):
            s = 0.0
            for t in q:
                f = d.get(t, 0)
                if f:
                    s += idf[t] * f * (k1 + 1) / (f + k1 * (1 - b + b * lengths[i] / avgdl))
            scores.append((-s, i))
        return [ids[i] for _, i in sorted(scores)[:k]]
    return search
""",
             call="[make_bm25(chunk(kb))('how many days do card refunds take', 3), make_bm25(chunk(kb))('is cash on delivery available', 2)]", tol=1e-9),
        dict(title="Measure retrieval",
             task="""
Write `evaluate(search, questions, k=3)` returning `{"hit@1": %, "hit@k": %, "mrr": ...}`:
- a question is a **hit@k** if any of the top-k chunks comes from its correct `doc_id`,
- **MRR** = mean of 1 / (rank of the first chunk from the correct doc), 0 if not in the top k.

Percentages rounded to 1, MRR to 3. Then look at the questions it misses — why do they fail?
""",
             starter="""
def evaluate(search, questions, k=3):
    raise NotImplementedError
""",
             solution="""
def evaluate(search, questions, k=3):
    h1 = hk = rr = 0
    for q, doc in questions[["question", "doc_id"]].itertuples(index=False):
        docs = [c.split("-")[0] for c in search(q, k)]
        if docs and docs[0] == doc:
            h1 += 1
        if doc in docs:
            hk += 1
            rr += 1 / (docs.index(doc) + 1)
    n = len(questions)
    return {"hit@1": round(h1 / n * 100, 1), "hit@k": round(hk / n * 100, 1), "mrr": round(rr / n, 3)}
""",
             call="evaluate(make_bm25(chunk(kb)), questions)", tol=1e-6,
             after="Try `make_bm25(chunk(kb))('When will I get my refund?', 3)`: the article says *refunds*, the query says *refund*, and plain BM25 treats them as different words. Real search engines **stem** words (refunds → refund) — a good extension. Look at the misses: customers say *\"money back\"*, *\"broken\"*, *\"close my account\"*; the articles say *refund*, *damaged*, *delete*. Keyword search can't bridge different words for the same idea. That's the **vocabulary mismatch** problem — the next milestone attacks it."),
        dict(title="Make retrieval better",
             task="""
Two cheap, effective fixes:
1. **Index the title with every chunk** (search `title + " " + text`), so a chunk about refunds is findable even if the word appears only in the title.
2. **Expand the query** with `SYNONYMS`: add the listed words for every query token that has an entry.

Write `make_better_search(chunks)` returning `search(query, k)` that does both on top of your BM25. The check reports the new evaluation — compare with the previous milestone.
""",
             hint="Build a copy of `chunks` whose `text` is title + text and pass it to `make_bm25`. For the query: `query + ' ' + ' '.join(extra words)`.",
             starter="""
def make_better_search(chunks):
    def search(query, k):
        raise NotImplementedError
    return search
""",
             solution="""
def make_better_search(chunks):
    with_titles = chunks.assign(text=chunks["title"] + " " + chunks["text"])
    bm25 = make_bm25(with_titles)

    def search(query, k):
        extra = [s for t in tokens(query) for s in SYNONYMS.get(t, [])]
        return bm25(query + " " + " ".join(extra), k)
    return search

""",
             call="evaluate(make_better_search(chunk(kb)), questions)", tol=1e-6,
             after="**Be honest about this number.** The synonym list was written while looking at these 30 questions, so it is tuned to them and the score is optimistic. Write 10 *new* questions and evaluate on those before you believe it. Production systems close the vocabulary gap with **embeddings** (dense vectors from a model) and combine them with BM25 (hybrid search), then re-rank. The synonym list is the hand-made version of the same idea — and you've now measured exactly how much it helps."),
        dict(title="A grounded prompt with citations",
             task="""
Write `build_prompt(question, chunks, max_words=250)` returning one string that:
- tells the model to answer **only** from the sources, to cite the source id in square brackets like `[KB03]`, and to reply exactly `I don't know based on the help centre.` if the sources don't contain the answer,
- lists the sources as `[doc_id] title: text`, adding them in order and **stopping before the sources part would exceed `max_words` words**,
- ends with the customer's question.

The check verifies the rules on a real question (it doesn't compare exact wording).
""",
             starter="""
def build_prompt(question, chunks, max_words=250):
    raise NotImplementedError
""",
             solution="""
def build_prompt(question, chunks, max_words=250):
    sources, used = [], 0
    for row in chunks.itertuples(index=False):
        line = f"[{row.doc_id}] {row.title}: {row.text}"
        if used + len(line.split()) > max_words:
            break
        sources.append(line)
        used += len(line.split())
    rules = ("You are ShopKart's support assistant. Answer the customer using ONLY the sources below. "
             "Cite the source id in square brackets, like [KB03], after each fact. "
             "If the sources do not contain the answer, reply exactly: I don't know based on the help centre.")
    return rules + "\\n\\nSources:\\n" + "\\n".join(sources) + f"\\n\\nCustomer question: {question}"

""",
             call="prompt_rules_ok('How much is express shipping?')", tol=1e-9),
        dict(title="An answer without an LLM: extractive fallback",
             task="""
When the LLM is down (or too expensive for simple questions), return the single best **sentence** from the retrieved chunks. Write `extractive_answer(question, k=3)` that:
- retrieves the top-k chunks with `retrieve_better(question, k)` (in the setup cell; it uses your `chunk` and `make_better_search`),
- splits them into sentences (on `. ` / `.`),
- returns `(best sentence, its doc_id)`, where best = most query tokens shared, after synonym expansion (ties: earlier sentence first).
""",
             starter="""
def extractive_answer(question, k=3):
    raise NotImplementedError
""",
             solution="""
def extractive_answer(question, k=3):
    q = set(tokens(question)) | {s for t in tokens(question) for s in SYNONYMS.get(t, [])}
    best = None
    for row in retrieve_better(question, k).itertuples(index=False):
        for sentence in re.split(r"(?<=\\.)\\s+", row.text):
            overlap = len(q & set(tokens(sentence)))
            if best is None or overlap > best[0]:
                best = (overlap, sentence.strip(), row.doc_id)
    return best[1], best[2]
""",
             call="[extractive_answer(q)[1] for q in ['When will I get my money back on my credit card?', 'Is shipping free?', 'Someone called asking for my OTP']]", tol=1e-9,
             after="Print the sentences too: `extractive_answer('Is shipping free?')`. Extractive answers are always grounded (they *are* the source), but can't combine facts or rephrase. That's what the LLM adds — below."),
    ],
    extra=[("## Generate the answer with Claude (optional)\n\nWith retrieval and the prompt done, the LLM call is a few lines. It needs an API key and costs a fraction of a rupee per question, so it's optional. Compare its answers with your extractive ones: does it cite sources? Does it say \"I don't know\" for a question the help centre doesn't cover, like *\"Do you sell cars?\"*", CLAUDE_CODE.strip())],
    present="""
Write a short design doc for the support team:

1. **Architecture**: chunking → BM25 (+ titles, synonyms) → prompt with citations → LLM, with the extractive fallback.
2. **Retrieval results**: hit@1, hit@3 and MRR before and after your improvements, and 2–3 examples of remaining failures.
3. **Safety**: grounding rules, citations, the "I don't know" behaviour, and why the bot must never invent policy.
4. **Cost and latency**: an LLM call only when needed; extractive answers for simple questions.
5. **Next steps**: embeddings / hybrid search, re-ranking, an answer-quality evaluation, feedback buttons.
""",
    resume=[
        "Built a retrieval-augmented support assistant over an 18-article help centre with hand-written BM25, title indexing and query expansion",
        "Created a 30-question labelled evaluation set and raised hit@3 from **X%** to **Y%** (MRR **A → B**)",
        "Designed a grounded prompt with citations and an \"I don't know\" rule, plus an extractive fallback, and generated answers with the Claude API",
    ],
    interview=[
        "Why did you evaluate retrieval separately from the final answer?",
        "Explain BM25 in plain words. What do k₁ and b control?",
        "What is the vocabulary-mismatch problem, and how do embeddings solve it?",
        "How do you stop the model from inventing a refund policy?",
        "How would you chunk long documents, and how does chunk size change results?",
        "How would you evaluate the final answers, not just retrieval?",
    ],
    extensions=[
        "Add dense retrieval with a sentence-embedding model and combine it with BM25 (reciprocal rank fusion).",
        "Write 10 questions the help centre can't answer and measure how often the bot correctly says \"I don't know\".",
        "Use an LLM as a judge to score answer faithfulness against the sources.",
        "Serve the assistant as an API (project 7 shows how) with a chat front end.",
    ],
)
