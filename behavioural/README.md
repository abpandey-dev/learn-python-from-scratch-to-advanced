# Behavioural Interviews

Technical rounds decide whether you *can* do the job. Behavioural rounds decide whether they want you on the team, and at senior levels they often decide the level and the offer. This guide shows what interviewers score, how to build stories that prove it, and how to practise until it's natural.

**Web page with a timed practice drill:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/behavioural/

## Contents

- [What interviewers are scoring](#what-interviewers-are-scoring)
- [The STAR method, done properly](#the-star-method-done-properly)
- ["Tell me about yourself"](#tell-me-about-yourself)
- [Build your story bank](#build-your-story-bank)
- [The project deep dive](#the-project-deep-dive)
- [Tricky questions, and how to handle them](#tricky-questions-and-how-to-handle-them)
- [Questions to ask them](#questions-to-ask-them)
- [Salary and offers](#salary-and-offers)
- [Role-specific behavioural questions](#role-specific-behavioural-questions)
- [On the day](#on-the-day)
- [A two-week practice plan](#a-two-week-practice-plan)
- [Question bank](#question-bank)

## What interviewers are scoring

A behavioural question asks about something you **actually did**, because past behaviour is the best predictor of future behaviour. Interviewers usually fill in a scorecard with a few signals, then argue about them in a debrief. Your job is to give them evidence for each signal.

| Signal | What they want to see | Typical question |
|---|---|---|
| Ownership | You take responsibility beyond your ticket, and finish things | "Tell me about something you owned end to end." |
| Impact | Your work changed a number someone cares about | "What's the most impactful thing you've built?" |
| Collaboration | You work well with people who disagree with you | "Tell me about a conflict with a teammate." |
| Communication | You can explain clearly to technical and non-technical people | "Explain a complex project to me as if I'm in sales." |
| Dealing with ambiguity | You make progress when the problem is unclear | "Tell me about a time requirements were vague." |
| Learning and growth | You learn fast and act on feedback | "Tell me about a mistake and what you changed." |
| Judgement | You make sensible trade-offs under constraints | "Tell me about a hard technical decision." |
| Leadership (any level) | You raise the bar for others, with or without a title | "Tell me about a time you influenced without authority." |

**Rounds you may meet:** a recruiter or HR screen (motivation, notice period, salary expectations), a hiring-manager round (your past work and how you operate), a values or "bar raiser" round (deep probing of 2–3 stories), and team-fit chats. Many companies publish their values or leadership principles — read them and map a story to each.

## The STAR method, done properly

Structure every story as **STAR**, and add an **L** for what you learned:

| Part | Share of the answer | What to say |
|---|---|---|
| **S**ituation | ~10% | Context in 1–2 sentences: team, product, scale |
| **T**ask | ~10% | What *you* were responsible for, and why it mattered |
| **A**ction | ~60% | What **you** did, step by step: decisions, trade-offs, who you talked to |
| **R**esult | ~15% | What changed, with numbers, and how you know |
| **L**earning | ~5% | What you'd do differently, or what you now do every time |

Aim for **about 2 minutes**, then stop and let them dig in. Most of the score comes from the follow-up questions, so leave room for them.

**Three rules that separate strong answers from weak ones:**

1. **Say "I", not "we".** The interviewer is hiring you. Describe your part precisely, and credit others honestly.
2. **Use numbers.** "Cut the report from 40 minutes to 6", "reduced on-call pages from 30 a week to 4", "affected 12,000 customers". Estimates are fine if you say they're estimates.
3. **Show your thinking.** The options you considered, and why you chose one, are worth more than the outcome.

### A weak answer and a strong one

**Question:** "Tell me about a time you improved a process."

> **Weak:** "Our deployments were slow, so we automated them with a CI/CD pipeline and things got much better. Everyone was happy."

It's vague ("things got better"), it's "we", and there's no decision or number.

> **Strong:** "Our team of six released once every two weeks, and each release took a full day of manual steps — about 30% of releases needed a hotfix. *(S)* I volunteered to fix the release process, because I'd been the one doing most of them. *(T)* I first wrote down every manual step and timed them, which showed 70% of the time was the manual regression suite. I proposed automating the 40 most-used checks first rather than all 300, because they covered most past hotfixes — my lead wanted all of them, so I showed her the hotfix history and we agreed to start small. I built the pipeline in GitHub Actions over three sprints and paired with a teammate so it didn't depend on me. *(A)* Release time went from a day to 45 minutes, we moved to weekly releases, and hotfixes dropped to about 8% over the next quarter. *(R)* What I learned is to measure before automating — the timings won the argument, not my opinion. *(L)*"

## "Tell me about yourself"

This opens most interviews, and it sets the tone. Use **present → past → future** in about **90 seconds**:

1. **Present:** your current role and the one thing you do best, with a number.
2. **Past:** 1–2 earlier experiences that explain how you got here — only what supports this job.
3. **Future:** why this role, at this company, is the logical next step.

Don't recite your CV, your hobbies or your whole education. End on why you're here, so their next question is about the job.

### Three examples

> **Fresher:** "I'm a final-year computer science student. Over the last year I've built three data projects end to end — the one I'm proudest of is a churn model on 5,000 customers that I took from a notebook to a FastAPI service with monitoring. Before that I did a three-month internship where I automated a weekly sales report in Python and SQL, which saved the analyst about a day a week. I'm applying for this data engineering role because I enjoy the pipeline side most — making data reliable — and your team's work on real-time analytics is exactly what I want to learn."

> **Career switcher (testing → data or AI engineering):** "I'm a test engineer with four years in a large product company, where I own automation for a set of backend services — I built a framework that runs 1,200 API tests on every merge. Testing taught me to think about how systems fail, and over the last year I've moved towards data: I've built pipelines and a RAG assistant as side projects, and at work I've started taking data tickets. I'm applying because I want to do this full time, and I think my reliability background is an advantage when building data platforms."

> **Experienced engineer:** "I'm a senior backend engineer leading payments reliability for a team of five. Last year we cut failed payments by 18% by redesigning retries and idempotency. Before that I spent three years building the order service from its first version to about 2 million orders a day. I'm looking for a staff-level role where I can shape architecture across teams, and your move to an event-driven platform is the kind of problem I want to own."

## Build your story bank

You don't need a story per question — you need **8–10 strong stories** that each cover several signals. Prepare them once, then adapt.

| # | Story type | Covers |
|---|---|---|
| 1 | Your biggest technical achievement | impact, ownership, judgement |
| 2 | A hard problem you debugged | problem solving, persistence, communication |
| 3 | A conflict or disagreement | collaboration, influence, maturity |
| 4 | A failure or mistake | ownership, learning, honesty |
| 5 | A time you led without authority | leadership, influence |
| 6 | Working with vague requirements | ambiguity, judgement |
| 7 | A tight deadline or trade-off | prioritisation, judgement |
| 8 | Going beyond your role | ownership, initiative |
| 9 | Helping or mentoring someone | leadership, team |
| 10 | Feedback you received and acted on | learning, self-awareness |

**For each story, write down:** a one-line title, the STAR+L notes as bullet points (not a script), 2–3 numbers, and the follow-up questions you expect. Then practise saying it aloud — reading it isn't the same.

**Where stories come from:** your job, internships, college projects, open source, hackathons, the industry projects in this course, volunteering. A small story told well beats a big story told vaguely.

**Never** share confidential details of a current or past employer — numbers can be rounded or relative ("cut costs by about a third"), and products can be described generically.

## The project deep dive

Expect at least one interviewer to say: "Pick a project and walk me through it." They will dig until they find the edge of your understanding. Structure it like this:

1. **The problem and why it mattered** (who had it, what it cost) — 30 seconds.
2. **Your role** — what you owned versus the team.
3. **The design** — draw it: data in, processing, storage, outputs. Name the key choices.
4. **The hardest part** — one technical challenge and how you solved it.
5. **Results** — numbers, and how you measured them.
6. **What you'd change** — this shows maturity, and it's often the most valuable minute.

**Follow-ups to prepare:** Why that tool and not the alternative? What happens at 10× the data? What broke in production? How did you test it? What would you monitor? If you had to cut the project time in half, what would you drop?

Each industry project in this course ends with its own interview questions — practise those aloud with your own numbers.

## Tricky questions, and how to handle them

| Question | What they're checking | A good approach |
|---|---|---|
| "What's your biggest weakness?" | Self-awareness, not perfection | A real, non-fatal weakness, plus what you're doing about it and evidence it's improving. Avoid "I'm a perfectionist." |
| "Tell me about a failure." | Ownership and learning | A real failure that was partly your fault, what you did to fix it, and the habit you changed. Don't blame others. |
| "Why are you leaving your job?" | Are you running away or towards something? | Talk about what you want next (growth, a domain, scope). Never criticise your employer. |
| "Why this company?" | Did you do your homework? | Something specific: their product, their engineering blog, a problem they're solving, and how it connects to you. |
| "Why should we hire you?" | Can you connect your strengths to their needs? | Two or three strengths, each tied to something in the job description, with a proof point. |
| "Where do you see yourself in five years?" | Ambition that fits the role | A direction (deeper expertise or leading a team), not a job title at another company. |
| "Explain this gap in your CV." | Honesty | A short, truthful reason (health, family, study, a layoff) and what you did to stay sharp. Then move on. |
| "What are your salary expectations?" | Whether you're in budget | See the offers section: give a researched range, or ask for their band first. |
| "Do you have other offers?" | Your leverage and timeline | Be truthful and brief. "I'm in later stages with two companies, and I'd love to make this work." |
| "What's your notice period?" | When you can start | The real number, and whether it can be shortened or bought out. Don't promise what your contract doesn't allow. |

## Questions to ask them

At the end you'll hear "Do you have any questions?". Always ask 2–3 — it shows genuine interest, and the answers help you decide.

- What would success look like in my first 90 days?
- What's the biggest challenge the team is facing right now?
- How is work planned and prioritised? Who decides?
- How does on-call work, and how often is the team paged?
- How do people grow here — what did the last person promoted on this team do?
- What do you like most about working here, and what would you change?
- How is the team's work measured?
- Is there anything in my background that makes you hesitate? *(Brave, but it lets you address a concern before the debrief.)*

**Avoid** asking about salary or leave in a technical round, or anything a quick look at their website would answer.

## Salary and offers

**Before any salary conversation,** research the range for the role, level and city (salary surveys, job posts that list bands, people you know). Know your current total compensation precisely.

**Understand what's in an offer:** fixed pay, variable or bonus (and how much is usually paid out), joining bonus, stock or ESOPs (vesting schedule and how they'd be valued), benefits, and notice-period buyout. In India, check how the CTC breaks down — fixed salary is what reaches your account monthly, and a high "CTC" can hide a large variable part.

**Negotiating:**

1. Let them make the first offer when you can. If pushed, give a researched **range** whose bottom you'd happily accept.
2. Be enthusiastic and specific: "I'm excited about this role. Based on my research and another offer, I was expecting a fixed salary closer to X. Is there flexibility?"
3. Negotiate the whole package — joining bonus, level, stock, start date — not just the fixed salary.
4. Get the final offer in writing before resigning.
5. Never lie about other offers. Recruiters talk, and offers get verified.

**If your current employer counters,** remember why you started looking. Accept a counter-offer only if it fixes the real reason, not just the pay.

## Role-specific behavioural questions

Interviewers mix technical judgement into behavioural questions. Prepare at least one story for each of these that fits your target role.

**Software engineers:** a production incident you handled; a time you pushed back on a design; how you made a slow system faster; a technical debt trade-off; reviewing someone's code when you disagreed.

**Data engineers and analysts:** a data quality problem you found before (or after) the business did; a pipeline that failed and how you made it reliable; reconciling two numbers that didn't match; explaining a metric to a stakeholder who disagreed with it; a time you said no to a data request.

**ML and AI engineers:** a model that worked offline but not in production; how you chose an evaluation metric; a time the simplest model won; handling a fairness or safety concern; explaining model limitations to a product manager; an LLM feature that failed in testing and what you changed.

**Moving into a new field (for example from testing to data or AI):** why the move, and why now; what you've built to prove it; how your current skills transfer (testing → data quality, reliability, edge cases); what you're still learning and how.

## On the day

- **Video calls:** test your camera, microphone and connection; look at the camera when you speak; keep a glass of water and a notepad nearby; close notifications.
- **Take a breath before answering.** "Let me think of the best example" is perfectly fine.
- **Clarify the question** if it's broad: "Would you like a technical example or one about working with people?"
- **Keep it to ~2 minutes,** then check: "Shall I go deeper into any part?"
- **If you don't have an example,** say so and offer the closest one, or describe what you would do and why.
- **Be honest.** Experienced interviewers spot invented stories in the second follow-up question.
- **Send a short thank-you** after, mentioning one thing you enjoyed discussing.

## A two-week practice plan

| Days | Do this |
|---|---|
| 1–2 | Read the target companies' values and job descriptions. List the signals they care about. |
| 3–5 | Write your story bank: 8–10 stories as STAR+L bullet points, with numbers. |
| 6 | Write and time your "tell me about yourself" for each type of role you're applying to. |
| 7–9 | Use the practice drill below: 5 random questions a day, aloud, with a 2-minute timer. Record yourself once. |
| 10 | Prepare two project deep dives with a diagram you can draw from memory. |
| 11–12 | Mock interviews with a friend or mentor; ask them to probe with "why?" at least three times per story. |
| 13 | Prepare your questions for them, and your salary research. |
| 14 | Light review only. Rest. |

**Before every interview:** re-read the job description, pick the 4–5 stories that fit it best, and prepare one specific reason you want *this* company.

## Question bank

66 questions, grouped by what they test. For each: what the interviewer is really asking, and what a strong answer includes.

### Ownership

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a project you owned end to end. | Do you take responsibility for outcomes, not just tasks? | Scope you defined, decisions you made, how you handled loose ends, a measured result. |
| Tell me about a time you went beyond your role. | Initiative without being asked. | Why you noticed the gap, the risk you took, how you kept your own work on track. |
| Describe a time you took responsibility for a problem you didn't cause. | Do you fix things or point fingers? | Fixing it first, then preventing it, without blaming anyone. |
| Tell me about something you started that others now rely on. | Lasting impact. | Adoption numbers, how you made it maintainable, handing it over. |
| Tell me about a time you had to finish something unpleasant or boring. | Reliability. | Why it mattered, how you made it faster or automated it. |

### Impact

| Question | They're really asking | A strong answer includes |
|---|---|---|
| What's the most impactful thing you've built? | Can you connect work to outcomes? | The business problem, your part, a number before and after. |
| Tell me about a time you used data to make a decision. | Evidence over opinion. | What you measured, what surprised you, the decision and its result. |
| Describe a time you made something significantly faster or cheaper. | Engineering judgement. | How you found the bottleneck, options considered, measured improvement. |
| Tell me about a time you improved a process for your team. | Leverage — making others better. | Before/after metrics and how you got people to adopt it. |
| Tell me about a small change that had a big effect. | Finding leverage. | Why you spotted it and how you proved the effect. |

### Collaboration & conflict

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a disagreement with a teammate. | Can you disagree without damage? | Understanding their view, data over opinion, the outcome, the relationship after. |
| Tell me about a time you disagreed with your manager. | Courage and respect. | How you raised it, what evidence you used, committing once decided. |
| Describe working with someone difficult. | Empathy and professionalism. | What drove their behaviour, what you changed, the result. No character attacks. |
| Tell me about a time you had to rely on another team. | Cross-team skills. | Making the ask easy, aligning priorities, escalating politely if needed. |
| Tell me about a time you received critical feedback. | Coachability. | The feedback, your honest reaction, what you changed, evidence it stuck. |
| Tell me about a time you gave difficult feedback. | Candour with care. | Specific behaviour and impact, private and timely, follow-up. |
| Describe a team project that went badly. What was your part? | Ownership within a team. | Your contribution to the problem and the fix. |

### Ambiguity & judgement

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a time requirements were unclear. | Do you create clarity? | Questions you asked, assumptions you wrote down, a small first version to get feedback. |
| Tell me about a hard technical decision you made. | Trade-off thinking. | Options, criteria, what you gave up, and whether it was right in hindsight. |
| Describe a decision you made with incomplete information. | Comfort with risk. | How you reduced risk, made it reversible, and checked later. |
| Tell me about a time you had to choose between speed and quality. | Pragmatism. | What you shipped, what you deferred, how you paid the debt back. |
| Tell me about a time you changed your mind. | Intellectual honesty. | What new evidence changed it and how you communicated the change. |

### Failure & learning

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a mistake you made. | Honesty and learning. | A real mistake, its impact, how you fixed it, what you now do differently. |
| Tell me about a project that failed. | Resilience. | Why it failed, your part, what you salvaged, what you'd change. |
| Tell me about a production incident you caused or handled. | Calm under pressure. | Detection, mitigation first, root cause, the prevention you added. |
| What's something you learned recently, and how? | Learning speed. | A concrete skill, how you learned it, something you built with it. |
| Tell me about a time you missed a deadline. | Accountability. | When you saw the risk, how early you told people, what you changed. |

### Leadership & influence

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a time you influenced without authority. | Leadership without a title. | Understanding what others cared about, evidence, small wins that built trust. |
| Tell me about a time you mentored or helped someone. | Raising the bar for others. | What they needed, what you did, how they grew. |
| Describe a time you led a team through a difficult period. | Steadiness. | How you kept people informed, focused and motivated. |
| Tell me about a time you convinced people to adopt a new tool or practice. | Change management. | A pilot, proof, addressing objections, adoption numbers. |
| Tell me about a time you said no to a request. | Prioritisation and spine. | Why, how you said it, what you offered instead. |

### Communication

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Explain a complex technical topic to a non-technical person. | Clarity. | An analogy, the 'so what', no jargon — then actually do it in the interview. |
| Tell me about a time you had to deliver bad news. | Honesty and timing. | Telling early, with facts, impact and a plan. |
| Tell me about a misunderstanding that caused a problem. | Self-awareness in communication. | What went wrong, what you now confirm in writing. |
| Tell me about a presentation or document that changed a decision. | Persuasion. | Audience, structure, the evidence that landed. |
| How do you keep stakeholders informed on a long project? | Proactive communication. | Rhythm, format, flagging risks before they're problems. |

### Pressure & priorities

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about a time you had too much to do. | Prioritisation. | How you ranked work, what you dropped or delegated, how you told people. |
| Describe working under a tight deadline. | Delivery under pressure. | Cutting scope sensibly, protecting quality where it mattered. |
| Tell me about a time priorities changed suddenly. | Adaptability. | Understanding why, re-planning fast, not losing the earlier work. |
| How do you handle stress at work? | Sustainability. | Concrete habits, plus a real example where they helped. |

### Motivation & fit

| Question | They're really asking | A strong answer includes |
|---|---|---|
| Tell me about yourself. | Your story and fit, in 90 seconds. | Present → past → future, ending on why this role. |
| Why do you want to work here? | Research and genuine interest. | Something specific about their product or engineering, connected to you. |
| Why are you leaving your current role? | Running towards, not away. | What you want next. No complaints about your employer. |
| What kind of work energises you? | Fit with the role. | Honest answer that matches the job, with an example. |
| Where do you see yourself in five years? | Ambition and fit. | A direction of growth that this role supports. |
| What's your biggest weakness? | Self-awareness. | A real weakness, what you're doing about it, progress so far. |

### By role

**Software engineer**

- Tell me about a production incident you were part of. What did you do in the first hour?
- Tell me about a time you pushed back on a design or a deadline.
- Tell me about technical debt you decided to pay down — or decided not to.
- Tell me about a code review where you disagreed with the author.
- Tell me about the hardest bug you've fixed.

**Data engineer / analyst**

- Tell me about a data quality problem. Who found it, and what did you change?
- Tell me about a pipeline that kept failing and how you made it reliable.
- Two dashboards showed different revenue. How did you resolve it?
- Tell me about a stakeholder who didn't trust your numbers.
- Tell me about a data request you pushed back on.

**ML / AI engineer**

- Tell me about a model that worked offline but disappointed in production.
- How did you choose the evaluation metric for a project, and who disagreed?
- Tell me about a time a simpler model or a rule beat the fancy one.
- Tell me about an LLM feature that failed testing. What did you change?
- Tell me about a fairness, privacy or safety concern you raised.

**Switching fields**

- Why this move, and why now?
- What have you built to prove you can do this job?
- Which of your current skills transfer, and which are you still learning?
- Tell me about the hardest thing you learned on your own for this switch.

---

Edit `content.py` and run `python3 behavioural/build_guide.py` to rebuild this page and the website.
