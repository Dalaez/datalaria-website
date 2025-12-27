---
title: "Autopilot - the Final: From Localhost to the Cloud with GitHub Actions and CI/CD"
date: 2026-01-10
draft: false
categories: ["DevOps", "GitHub Actions", "Python"]
tags: ["CI/CD", "Automation", "Pipeline", "GitOps", "Workflow"]
image: "/images/posts/autopilot-architecture.jpg"
description: "Final chapter of Project Autopilot. I no longer run scripts on my computer. Now, a simple 'git push' wakes up my AI agents, generates content, and publishes it to social media upon my approval."
summary: "In this last chapter, we ditch manual execution. We built a CI/CD pipeline in GitHub Actions that detects new articles, orchestrates AI agents, and manages publishing to Twitter and LinkedIn under human supervision. Welcome to total automation."
---

We have come a long way. We started by designing a **Brain** capable of reading ([Post 2]({{< ref "posts/ai_agents_part2" >}})), we gave it personality with **Creative Agents** ([Post 3]({{< ref "posts/ai_agents_part3" >}})), and we fought against bureaucracy to get some **Hands** (APIs) that could publish legally ([Post 4]({{< ref "posts/ai_agents_part4" >}})).

But there was one last big step left so as not to be a **slave to my terminal**. Right now, to publish, I had to be at my computer, open the console, and run `python main.py`. That's not "Autopilot." That's "Assisted Driving."

Today, in the final chapter, we cut the cords. We move to the cloud and automate the entire process with my AI agents.

![Project concept image - Final](autopilot_final.png)

## The Pipeline Architecture

The goal is **GitOps**: that my only interaction with the system is pushing changes to Git. Everything else must happen by magic (or rather, by **GitHub Actions**).

I have designed a two-phase workflow:

1.  **Detection and Preview Phase (Automatic):**
    * GitHub detects a new `.md` file (or changes to an existing one).
    * The **Orchestrator** activates.
    * The system detects the post language (Spanish/English) and calculates the correct URL.
    * The AI (or template system) proposes a tweet and a LinkedIn post.
    * The system shows me a "Preview" in the execution logs, but **does not publish anything**.

2.  **Publishing Phase (Manual):**
    * The process **pauses** automatically thanks to GitHub *Environments*.
    * I receive an alert to review the deployment.
    * If I click the green button (**Approve**), the system executes the real call to the APIs.

{{< mermaid >}}
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f4f8', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#e6e6e6'}}}%%
graph TD
    %% Initial Node
    START([GitHub detects change in .md]) --> ORC

    %% --- PHASE 1: AUTOMATIC ---
    subgraph Phase1 ["🔹 Phase 1: Detection and Preview (Automatic)"]
        direction TB
        ORC[Orchestrator Activates]
        
        %% Parallel Tasks
        ORC --> TASK1[Detect Language and Calculate URL]
        ORC --> TASK2[AI proposes Tweet and LinkedIn]
        
        %% Convergence
        TASK1 --> LOGS
        TASK2 --> LOGS
        
        LOGS[Show 'Preview' in Execution Logs]
        LOGS --> NOPUB[🚫 NOTHING PUBLISHED YET]
    end

    NOPUB --> PAUSE

    %% --- PHASE 2: MANUAL ---
    subgraph Phase2 ["🔸 Phase 2: Publishing (Manual)"]
        direction TB
        PAUSE((⏸️ AUTOMATIC PAUSE<br/>GitHub Environments))
        
        PAUSE --> ALERT[🔔 Alert arrives to review deployment]
        ALERT --> DECISION{Approve Deployment?}
        
        %% Approval Path
        DECISION -- "Green Button (Approve) ✅" --> EXEC[🚀 Execute real API call]
        
        %% Rejection Path (Implicit)
        DECISION -- "Reject / Cancel ❌" --> STOP([End of flow without publishing])
    end

    %% Styles to highlight final steps
    style EXEC fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style STOP fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#721c24
    style PAUSE fill:#fff3cd,stroke:#ffc107,stroke-width:3px
{{< /mermaid >}}

## The Orchestrator (`orchestrator.py`)

I needed a script to join all the pieces together. To do this, I started developing a Python orchestrator that acts as a bridge between the Markdown file and my social media modules.

This script is in charge of the "fine" logic that we sometimes forget:
* Is it a post in English (`/en/`) or Spanish (`/es/`)?
* Does it have a featured image to generate the Twitter/X or LinkedIn card?
* Do I want the AI to write it, or do I want to write it myself?

### The Star Feature: "Director's Cut"

Sometimes, the AI doesn't get the tone exactly right, or I simply want to write the copy myself for a special announcement. To not lose automation but maintain control, I implemented a "Manual Overwrite" logic using Hugo's *Frontmatter*.

If my script detects this in the article header:

```yaml
---
title: "My Great Post"
social_text: "Today I don't want the AI to write for me. This post is so special that I hand-wrote this. 👇"
---
```

The system **ignores the automatic generation** and uses my exact words. It is the perfect balance: automation by default, manual control when necessary.

## Security and CI/CD: Sleeping Soundly

The `.github/workflows/autopilot.yml` file is where the magic happens. Here we define the "Secrets" (my Twitter and LinkedIn API keys) and the rules of the game.

The most interesting part is the environment protection:

```yaml
jobs:
  publish:
    environment: production  # <--- The key to security
    needs: check_changes
    steps:
      - run: python orchestrator.py
```

By defining the environment as `production`, GitHub forces me to review and approve the deployment. This prevents a code error or an AI "hallucination" from publishing unwanted content.

Additionally, we have configured the system so that **Twitter/X** generates the *Cards* with images automatically and **LinkedIn** treats the content as an "Article," ensuring that on both networks the blog's featured image looks large and attractive.

## The Final Result

Now, my publishing process is this:

1.  I write my article in Markdown peacefully.
2.  I run `git push`.
3.  I have a coffee. ☕
4.  I check GitHub from my phone, see the "Preview" of the generated tweet (in the correct language).
5.  I smile and hit **Approve**.

In seconds, the content appears on Twitter and LinkedIn. Without opening the terminal. Without touching Python. From anywhere.

**Twitter/X Publication**

![Post automatically published on twitter](datalaria_twitter_first_automation.png)

**LinkedIn Publication**

![Post automatically published on linkedin](datalaria_linkedin_first_automation.png)

## Autopilot Project Conclusion

What started as an experiment to test how AI agents work and how they can help in my day-to-day life has turned into a professional publishing system. We have touched upon:
* **Prompt Engineering** to define personalities.
* Complex **OAuth 2.0 APIs** and token management.
* Robust **Python** backend.
* **DevOps** and CI/CD with GitHub Actions.

This blog is no longer just a collection of texts; it is a living application that works for me. And now that I have free time... what shall we automate next?

**Thanks for joining me in this series.**

👉 **Final Source Code:** The entire project is available (and documented) on [GitHub](https://github.com/Dalaez/datalaria-website).