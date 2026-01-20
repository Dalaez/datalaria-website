---
title: "Autopilot - The Creatives: How I Programmed an AI to be Cynical on Twitter and Corporate on LinkedIn"
date: 2026-01-03
draft: false
categories: ["Generative AI", "Prompt Engineering", "Python"]
tags: ["CrewAI", "AI Personality", "Automation", "Marketing", "Storytelling"]
image: "cover.png"
description: "Chapter three of Project Autopilot. Transforming cold data into viral stories by creating two agents with opposing personalities: a cynical influencer and a corporate leader."
summary: "Having data isn't enough; no one likes a JSON file. In this post, we design the personality of our Writer Agents, teach Gemini to write 'Broetry' for LinkedIn and 'Shitposting' for Twitter, and scale the architecture to publish in Spanish and English simultaneously."
---

In [Post 2: The Brain]({{< ref "ai_agents_part2" >}}), we achieved something technically important: a Python script capable of reading my technical articles and extracting their essence into a structured JSON.

But I have a problem. **If I publish a JSON on Twitter, no one is going to read it.**

Data is cold. Social media is emotional. For this "Autopilot" system to work, I don't need more analysts; I need **creatives**. I need writers who understand the psychology of each platform.

Today, we are going to give the machine a **soul**. We are going to create **"The Creatives."**

![Conceptual image of the project - The Creatives](autopilot_creative.png)

## The Role Theory ( The Stanislavski Method for AI)

Large Language Models (LLMs) like Gemini are, in essence, method actors. If you ask them to "write a tweet," they will give you a generic, boring tweet full of hashtags like #Technology #Innovation.

But if you give them a **role**, a *backstory*, and a motivation, their behavior changes radically. In prompt engineering, this is the difference between a chatbot and an agent.

For Datalaria, I don't want a generic voice. I want to cover two ends of the spectrum:
1.  **The Chaos (Twitter/X):** Brief, direct, slightly cynical, and allergic to corporate speak.
2.  **The Order (LinkedIn):** Professional, inspiring, focused on business value.

## Designing the Personalities (The Code)

Using **CrewAI**, defining these personalities is as simple (and complex) as writing a biography. Here is the actual code from `src/agents.py` that defines my two new digital employees.

### 1. The Tech Influencer (Twitter)
I explicitly asked it to hate corporate jargon and use lowercase for aesthetics.

```python
def twitter_writer_agent(self):
    return Agent(
        role="Tech Twitter Influencer",
        goal="Convert structured insights into a viral Twitter thread",
        backstory="""You are a tech influencer who hates corporate jargon. 
        You write in a punchy, provocative style. 
        You use lowercase often for aesthetic. 
        You focus on the 'Marketing Hooks' from the input. 
        You NEVER use hashtags like #Technology, only niche ones.""",
        llm=self.llm
    )
```

### 2. The Thought Leader (LinkedIn)
Here we look for the "Broetry" style (short sentences with lots of whitespace) that works on LinkedIn.

```python
def linkedin_writer_agent(self):
    return Agent(
        role="LinkedIn Thought Leader",
        goal="Write a high-engagement LinkedIn post",
        backstory="""You are a respected Voice in the Tech industry. 
        You write with empathy and professionalism. 
        You use the 'Broetry' style (short paragraphs, lots of whitespace). 
        You focus on the 'Key Takeaways' and business value. 
        You start with a strong hook.""",
        llm=self.llm
    )
```

## Refactoring: The Multilingual Challenge

Datalaria is a global blog, so I faced a challenge: **Do I need to create 4 different agents to write in Spanish and English?**

The engineering answer is **NO**. An agent is an entity with a personality; language is just a tool.

Instead of duplicating agents, I duplicated the **Tasks (`Tasks`)**. In `src/tasks.py`, I now explicitly define the output language:

```python
def twitter_task_es(self, agent, context):
    return Task(
        description="Escribe un hilo viral en ESPAÑOL basado en el análisis...",
        agent=agent,
        expected_output="Un hilo de Twitter en Español..."
    )

def twitter_task_en(self, agent, context):
    return Task(
        description="Write a viral Twitter thread in ENGLISH based on the analysis...",
        agent=agent,
        expected_output="A Twitter thread in English..."
    )
```

This makes my pipeline scalable. If tomorrow I want to publish in French, I just add a task, I don't hire a new agent.

## The Battle of the Agents: Real Results

To test this, I used my article on **"S&OP Processes with AI and BPMN."** It's a dense and boring topic if not sold well.

Let's see what the agents did with the same input.

### The Result on Twitter (The Cynic)
*Author's note: This result hurt a little; it's more direct than I am.*

> stop drowning in walls of text.
> manually turning industrial narratives into diagrams is a grind. it’s a waste of brainpower.
> we’re using genai to turn messy s&op docs into precise bpmn diagrams in seconds.
> here is how you stop being a human translator. 🧵
> ---
> most "business analysis" is just expensive friction.
> genai identifies hidden dependencies and feedback loops that human bas miss.
> it’s not just drawing; it’s uncovering the logic buried under corporate fluff.
> #ProcessEngineering #Industry40

### The Result on LinkedIn (The Corporate)

> Stop drowning in 'walls of text' and PDF graveyards. 🧱
>
> Industrial processes are the heartbeat of your company.
>
> But they are often buried in dense S&OP narratives that no one reads.
>
> This creates a massive gap between what the business needs and what engineering builds.
>
> I’ve spent years seeing Technical Leads and Ops Managers struggle with this "translation layer."
>
> The good news? Generative AI is changing the game.
>
> By using AI as a virtual Business Analyst, you can transform complex industrial narratives into precise BPMN diagrams in seconds.
>
> It’s not just about speed. It’s about clarity.
>
> 👇 How is your team currently bridging the gap between business narratives and technical execution? Let’s discuss in the comments.

## Conclusion

The difference is abysmal. The same model (Gemini 1.5 Flash), reading the same article, has generated two pieces of content completely distinct, adapted to the channel and the language.

I already have:
1.  The **Brain** that understands the code.
2.  The **Creatives** that write the copy.
3.  The files generated on my hard drive.

But there is still a "human" in the loop. I still have to run `python main.py` manually and copy-paste these texts onto social media.

In the next post, we enter hostile territory. We are going to try to connect these agents with the outside world.

**Coming soon Post 4: The API Nightmare.** I will try to connect my agents to Twitter and LinkedIn and (probably) almost lose my mind in the process.

👉 **Source Code:** The updated code with the new agents and multilingual support is available in the `/autopilot` folder of the [GitHub repo](https://github.com/Dalaez/datalaria-website).