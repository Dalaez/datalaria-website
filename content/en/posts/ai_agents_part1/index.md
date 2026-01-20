---
title: "Project Autopilot: Why I Fired Myself as Community Manager to Build an AI agents Army"
date: 2025-12-27
draft: false
categories: ["Automation", "Artificial Intelligence", "DevOps"]
tags: ["Agents", "Gemini", "CrewAI", "GitHub Actions", "Python", "Dogfooding"]
image: "cover.png"
description: "Experimenting with AI and new tech is my passion; distributing that content... not so much. In this series, I document how I'm building an automated team of AI Agents to handle my posts and manage their distribution across social media."
summary: "The 'Organic Traffic Plateau' is real. To overcome it without losing focus on engineering, I'm launching an extreme 'dogfooding' experiment: automating Datalaria's distribution using Gemini, CrewAI, and GitHub Actions. This is the Master Plan."
---

In the world of engineering and technical blogging, we often face the "Builder's Paradox." We can spend 40 hours perfecting a specific topic, defining an architecture, or debugging tiny technical details. Yet, we can't seem to find 15 minutes to effectively promote that work on social media.

I have reached that point with **Datalaria**. The content is there, the architecture is optimized, but the distribution suffers due to the main bottleneck... well, me.

Today, I am making a strategic decision. I am "firing" myself from the role of Community Manager—a role I never truly exercised anyway. In my place, I am not hiring an agency; I am building one, experimenting with the trendy concept of "AI Agents."

Welcome to **Project Autopilot**: a 5-part series where we will build, live and in public, an autonomous system of AI Agents that reads this blog, analyzes it in detail, and autonomously prepares content for promotion and distributes it across social media while I am off doing other things.

## The Strategy: Extreme Dogfooding

The concept is simple but technically ambitious. We are going to execute a strategy of "dogfooding" (eating our own food). Instead of using third-party tools like [Buffer](https://buffer.com/) or [Hootsuite](https://hootsuite.com/), we will build a custom distribution engine using the very technologies we write about: **Generative AI** and **CI/CD Pipelines**.

The "Big Goal" is to transform the blogging process. Currently, "publishing" means pushing a Markdown file to GitHub. In the future, that `git push` will trigger a chain reaction where intelligent agents analyze, create, and distribute content.

![Conceptual image of the project](autopilot.png)

## The Architecture: Meet the Team

To solve this, a simple Python script isn't enough. We need reasoning capabilities. We need a system that understands context, tone, and audience.

We are designing an event-driven architecture hosted entirely within **GitHub Actions**, using **Google Gemini** as the brain and **CrewAI** as the orchestrator.

Here is the conceptual flow of the system we are going to build:

{{< mermaid >}}
graph TD
    %% Styles
    classDef human fill:#ff9f43,stroke:#333,stroke-width:2px,color:white;
    classDef code fill:#5f27cd,stroke:#333,stroke-width:2px,color:white;
    classDef ai fill:#0abde3,stroke:#333,stroke-width:2px,color:white;
    classDef social fill:#ee5253,stroke:#333,stroke-width:2px,color:white;

    %% Nodes
    User("👱‍♂️ Me / Author"):::human
    Git["📂 GitHub Repository <br/> Push new .md file"]:::code
    Action["⚙️ GitHub Actions <br/> CI/CD Runner"]:::code
    
    %% FIX: Subgraph with padding hack for title
    subgraph TeamAI ["🤖 The Team (CrewAI + Gemini)<br/><br/>"]
        direction TB        
        Orchestrator{"🧠 Orchestrator"}:::ai
        Analyst["🕵️ Agent 1: The Analyst <br/> (Extracts Metadata & Hooks)"]:::ai
        WriterX["🐦 Agent 2: Twitter Writer <br/> (Viral/Short Content)"]:::ai
        WriterLI["💼 Agent 3: LinkedIn Writer <br/> (Professional Tone)"]:::ai
    end

    Review("👀 Human Review <br/> Pull Request / Draft"):::human
    
    X["Twitter / X API"]:::social
    LI["LinkedIn API"]:::social

    %% Connections
    User -->|git push| Git
    Git -->|Trigger| Action
    Action -->|Start Process| Orchestrator
    
    Orchestrator -->|Raw Text| Analyst
    Analyst -->|JSON| Orchestrator
    
    Orchestrator -->|Context + Hooks| WriterX
    Orchestrator -->|Context + Key Points| WriterLI
    
    WriterX -->|Draft| Review
    WriterLI -->|Draft| Review
    
    Review -->|Approve| X
    Review -->|Approve| LI
{{< /mermaid >}}

### Architectural Decisions

1.  **The Trigger (GitHub Actions):** Why pay for a server? The blog is static (Hugo), so the automation should be ephemeral. It runs only when I publish.
2.  **The Brain (Gemini Pro):** We chose this model for its large context window. It needs to read entire technical tutorials without "forgetting" the beginning.
3.  **The Orchestrator (CrewAI):** This allows us to assign specific *personas* or roles. We don't want generic AI; we want a "Cynical Twitter Expert" and a "Corporate Strategist" working in parallel.

## Proof of Concept: Can AI Understand My Code?

Before writing a single line of the final pipeline, I needed to validate the core hypothesis: *Can Gemini actually understand the structure of my Hugo posts?*

I ran a test using a system prompt designed to act as a "Senior Tech Editor." The goal was not to write text, but to extract structured data (JSON) from my raw Markdown files.

The result was promising:

![Gemini Analysis Proof of Concept](ia_agents_proof_concept.png)

The model correctly identified the **Tech Stack**, generated a summary, and most importantly, extracted "Provocative Angles" for marketing. This structured JSON is what will feed our writer agents in the next phase.

## The Roadmap

This series is the core of Datalaria's content strategy for the coming months. We will document the pain, the bugs, and the victories in real-time.

* **Post 1: The Strategy (You are here).** The Master Plan and Architecture.
* **Post 2: The Brain.** Configuring Gemini Pro and LangChain/CrewAI to read and "understand" Markdown.
* **Post 3: The Creatives.** Prompt Engineering to create distinct personalities for LinkedIn vs. Twitter.
* **Post 4: The API Nightmare.** An honest look at the challenges of connecting to Social Media APIs.
* **Post 5: The Final Orchestrator.** CI/CD integration with GitHub Actions for fully automated deployment.

## Conclusion: From Content to Product

Through this experiment, we are going to try to "assemble" and "test" my first virtual work team. To do this, we will treat social media content distribution as a product in itself—one that these agents are capable of understanding, exploiting, and promoting.

Automation with these agents aims to prove that:

1.  **Consistency is key:** A bot doesn't get tired or forget to post.
2.  **Context is King:** Generic AI is boring; specialized Agents with clear roles provide value.
3.  **Code is Leverage:** Once assembled, these agents will work forever.

If this experiment fails, I will document the failure. If it works, **Datalaria** will become a blog promoted by itself using AI while its author is busy writing the next post :).

-----

*Ready to see the code? In the next post, we will open our IDE to configure the "Reader Agent" using Python and the Gemini API.*