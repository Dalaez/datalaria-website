---
title: "Thomas Bayes: The Reverend Who Taught Us to Update Our Beliefs with Data"
date: 2026-07-18
draft: false
categories: ["case-studies"]
tags: ["bayes", "probability", "bayesian inference", "prophet", "a/b testing", "statistics", "history of data"]
description: "The story of Thomas Bayes, the 18th-century reverend whose posthumous theorem transformed statistics, medicine, machine learning, and demand planning. How Bayesian inference connects with Prophet, Netflix, and the modern supply chain."
summary: "How do you update your opinion when you receive new evidence? If your answer is 'with data,' congratulations: you've been practicing Bayesianism for 260 years without knowing it. This is the story of an 18th-century reverend whose posthumous essay laid the foundation for machine learning, spam filters, medical diagnosis, and the probabilistic models we use today to forecast demand."
social_text: "How do you update your opinion with new evidence? If your answer is 'with data,' you've been practicing Bayesianism for 260 years. The story of Reverend Thomas Bayes and why his theorem powers modern AI 📊🧠⛪ #Bayes #AI #Statistics #TechHistory"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

There is a question every professional who works with data should ask — and almost no one formulates explicitly: **How should I change my opinion when I receive new evidence?** I don't mean a philosophical answer, but a mathematical one. If I believe there's a 30% probability that an electronic component will become obsolete this year, and I suddenly receive an email from the supplier announcing a production capacity reduction, how much should my estimate increase? To 50%? To 70%? How do I calculate it rigorously?

The answer to that question was formulated by an English Presbyterian reverend sometime before 1761, and it wasn't published until two years after his death. His name was **Thomas Bayes**, and his posthumous essay is, without exaggeration, one of the most influential documents in the history of science. From the spam filters in your email to the probabilistic forecasting models we used in the [S&OP Engineering series](/en/posts/sop-engineering-part2-forecasting/) with Facebook Prophet, everything passes through Bayes' Theorem.

In the lineage of historical figures who shaped our relationship with data — [Florence Nightingale](/en/posts/florence-nightingale/) and visualization, [John Snow](/en/posts/john-snow/) and geolocation, [Abraham Wald](/en/posts/abraham_wald/) and survivorship bias, [Kantorovich](/en/posts/kantorovich/) and optimization, [Deming](/en/posts/deming/) and quality, [Claude Shannon](/en/posts/claude_shannon/) and information — Bayes occupies a singular place: he taught us to think of **uncertainty as something quantifiable and updatable**, not as an obstacle but as raw material.

### The Reverend and the Posthumous Essay

Thomas Bayes was born in London in 1702 into a family of religious dissenters. His father, Joshua Bayes, was one of the first Presbyterian ministers ordained in England. Thomas followed in his father's footsteps, was ordained a minister, and spent most of his life as a pastor in Tunbridge Wells, a quiet spa town southeast of London.

But Bayes was no ordinary pastor. He was a Fellow of the **Royal Society** (elected in 1742), which indicates that his mathematical reputation was recognized by the scientific elite of his era. He is known to have published a work defending the logical foundations of Newton's calculus, but during his lifetime he was a discreet figure, almost invisible in the great intellectual debates of the Enlightenment.

History might have completely forgotten Bayes were it not for his friend **Richard Price**, a distinguished Welsh philosopher and mathematician. After Bayes's death in 1761, Price found among his papers an unfinished manuscript titled *"An Essay towards solving a Problem in the Doctrine of Chances"*. Price immediately recognized its importance, completed it, and presented it to the Royal Society in 1763.

The problem Bayes was trying to solve was deceptively simple in its formulation and profoundly revolutionary in its implications: **given a series of observations, what is the probability that the underlying cause is one thing or another?** In other words, how do we reverse the direction of probability? Not "given that the coin is fair, what is the probability of getting 7 heads in 10 flips?" but the inverse question: "given that I observed 7 heads in 10 flips, what is the probability that the coin is fair?"

### The Theorem: Updating Beliefs with Evidence

Bayes' Theorem can be expressed without intimidating formulas using three intuitive concepts:

![Visualization of Bayesian updating: from prior to posterior](bayes_updating.png)

1. **Prior (Previous Belief)**: What you believe before seeing the data. Your initial estimate based on experience, intuition, or historical data. In an S&OP context, the *prior* might be: "Historically, we sell about 10,000 units of this product in July."

2. **Evidence (Likelihood)**: The new data you observe and the probability of observing that data under different hypotheses. For example: "This June we've received 40% more advance orders than last year."

3. **Posterior (Updated Belief)**: Your new estimate after integrating the evidence with your previous belief. The *posterior* mathematically combines what you knew before with what the new data tells you. It doesn't discard your prior experience nor lets itself be blinded by a single new data point: **it weighs both**.

The beauty of the Bayesian approach is that it's **iterative**: today's *posterior* becomes tomorrow's *prior*. Each new piece of data refines your estimate. It's not a static photograph; it's a movie that updates frame by frame. It is exactly the same philosophy as [W. Edwards Deming's](/en/posts/deming/) PDCA cycle: plan, do, check, adjust. Repeat.

### Modern Connection: Prophet and Demand Forecasting

Where does Bayes appear in modern data engineering? Virtually everywhere, but the most direct connection with this blog is **Facebook Prophet**, the tool we used in [Part 2 of the S&OP series](/en/posts/sop-engineering-part2-forecasting/) to generate probabilistic demand forecasts.

Prophet is, at its core, a **Bayesian additive model**. It decomposes a time series into three components — trend, seasonality, and holiday effects — and generates not a point prediction, but a **confidence interval**. That confidence interval is, literally, a Bayesian posterior distribution: it reflects the model's uncertainty given the historical evidence.

Why does this matter in practice? Because the **Safety Stock** we calculated in [Part 3 of the S&OP series](/en/posts/sop-engineering-part3-optimization/) — the amount of buffer inventory to absorb demand variability — is calculated on the upper bound of that confidence interval (typically at 95%). If Prophet used a deterministic model (a single number, no uncertainty), our Safety Stock would be a guess. Thanks to Bayes, it's a **decision grounded in the probability distribution of future demand**.

The *prior* in this context is the accumulated experience of the demand planning team and the historical patterns of the time series. The *evidence* is the new data arriving each week or month. The *posterior* is the updated forecast that feeds the [PuLP linear programming engine](/en/posts/sop-engineering-part3-optimization/) to optimize the production plan. Bayes is at the heart of the chain, even though his name is never mentioned in S&OP meetings.

### Modern Connection: A/B Testing and Netflix

When [Netflix](/en/posts/netflix/) decides which thumbnail to show for a series, it runs a massive A/B test: it shows version A to millions of users and version B to millions of others, then measures which generates more clicks. The classical (frequentist) approach requires waiting until a predetermined sample size is reached to declare a "winner" with statistical significance. If you do *peeking* — looking at results before time — you invalidate the experiment.

The **Bayesian** approach to A/B testing eliminates this problem. Instead of a binary hypothesis test (is there a difference or not?), Bayesian A/B testing continuously calculates the **probability that version A is better than version B** given the data observed so far. You don't need to wait for a fixed sample size because the posterior distribution updates with each new data point.

This has enormous practical implications for startups and teams with limited traffic. If your product doesn't have millions of users, a frequentist test can take weeks or months to be conclusive. A Bayesian test gives you a useful probability estimate much sooner, with the honesty of telling you: "With current data, there's a 78% probability that A is better than B." You decide if that 78% is enough to act on.

### Modern Connection: Spam Filters and Classification

One of the first triumphs of machine learning in production at scale was the **Bayesian spam filter**. The **Naive Bayes** algorithm (called "naive" because it assumes independence between words, a crude simplification that's surprisingly effective) calculates the probability that an email is spam given the words it contains.

The *prior* is the base rate of spam (approximately 45% of all global email). The *evidence* is the email's words: "offer," "free," "urgent" increase the posterior probability of spam; "meeting," "budget," "attached" reduce it. Each word updates the probability, exactly as Bayes prescribed 260 years ago.

The connection with [Abraham Wald's survivorship bias](/en/posts/abraham_wald/) is direct: in a spam filter, the data you **don't see** (legitimate emails erroneously filtered as spam) is as important as what you do see. If your filter has a high false positive rate, you're making the same mistake as the WWII engineers who only analyzed the planes that returned. Bayes and Wald, separated by two centuries, are talking about the same problem: **absent information distorts your conclusions**.

### Modern Connection: Medical Diagnosis and the Perfect Test Paradox

There's a classic example of Bayesian reasoning that should be mandatory in every engineer's training, because it destroys a very widespread intuition. Suppose there's a medical test for a rare disease (prevalence: 1 in 10,000 people). The test has a sensitivity of 99% (correctly detects 99% of the sick) and a specificity of 99% (correctly identifies 99% of the healthy).

Question: if you test positive, **what is the probability that you're actually sick?**

The intuitive answer most people give — including many physicians — is "99%." The correct Bayesian answer is approximately **1%**. How is this possible? Because the prevalence (the *prior*) is so low that, even with a 99% test, the vast majority of positives are false positives.

This reasoning is directly applicable to AI system engineering. When we configure alerts in the [obsolescence radar](/en/posts/obs_part5_radar_agent/) or in any monitoring system, the false positive rate is the silent enemy. An anomaly detection system with 99% accuracy can generate hundreds of false alerts if the base rate of actual anomalies is very low. Bayes forces us to think about the *prior* before celebrating the *test's* accuracy.

### The Legacy: Think in Distributions, Not Points

Thomas Bayes's deepest contribution was not a formula; it was a **mindset shift**. Before Bayes, probability was conceived as a fixed property of objects: a coin has a 50% chance of landing heads, period. After Bayes, probability became a measure of **our degree of knowledge** about the world, continuously updated with new evidence.

This distinction is the difference between an engineer who says *"July demand will be 10,000 units"* and one who says *"July demand has a 95% probability of falling between 8,500 and 11,500 units, and our production plan must absorb that variability."* The first operates with false certainties; the second, with quantified uncertainty. The first is vulnerable to the *bullwhip effect* that [destroys supply chains](/en/posts/sop_engineering-data-hygiene/); the second is armored against it.

In a world where AI models are stochastic by nature — as we painfully documented in the [Autopilot post-mortem](/en/posts/ai_agents_part9/), where the same pipeline produces different results on each run — thinking Bayesianly isn't a philosophical option: it's an operational necessity. Don't ask "what is the answer?" Ask "what is the distribution of possible answers, and with what confidence?"

A reverend from the 18th century, working in solitude with quill and ink in an English spa town, solved a problem that today powers medicine, marketing, cybersecurity, supply chain management, and artificial intelligence. And he did it with an idea so simple it fits in a single sentence: **update what you believe with what you observe**. Two hundred and sixty years later, we still haven't found better advice.

---

#### Sources of Interest:
* [**Stanford Encyclopedia of Philosophy**: Bayes' Theorem — Foundations and Historical Context](https://plato.stanford.edu/entries/bayes-theorem/)
* [**Royal Society**: Thomas Bayes — Fellow Profile](https://royalsociety.org/people/thomas-bayes-11313/)
* [**3Blue1Brown**: Bayes' theorem, the geometry of changing beliefs (YouTube)](https://www.youtube.com/watch?v=HZGCoVF3YvM)
* [**Datalaria**: Descriptive Statistics — Data Analysis Fundamentals](/en/posts/descriptive-analysis/)
* [**Datalaria**: S&OP Part 2 — Demand Planning with Prophet (Bayesian Model)](/en/posts/sop-engineering-part2-forecasting/)
* [**Datalaria**: Abraham Wald — The Epistemology of Missing Data](/en/posts/abraham_wald/)
* [**Datalaria**: Netflix — How Data Forges an Empire (A/B Testing)](/en/posts/netflix/)
* [**Datalaria**: Claude Shannon — Entropy as Uncertainty](/en/posts/claude_shannon/)
