---
title: "Autopilot - Ctrl: AI Content Auditing with GitHub Copilot CLI"
date: 2026-02-01
draft: false
categories: ["DevOps", "Python", "AI"]
tags: ["devchallenge", "githubchallenge", "cli", "githubcopilot", "Copilot CLI", "Content Audit", "Automation"]
image: "cover.png"
description: "I built autopilot-ctrl, a CLI that uses GitHub Copilot CLI to automatically audit and improve AI-generated content before publishing to social media."
summary: "When AI generates social media content, how do we know if it's good? I built autopilot-ctrl, a tool that uses GitHub Copilot CLI to evaluate content quality before publishing."
---

*This is a submission for the [GitHub Copilot CLI Challenge](https://dev.to/challenges/github-2026-01-21)*

## What I Built

**autopilot-ctrl** is a command-line tool that audits AI-generated social media content before publishing. Think of it as a "quality gate" for your content pipeline.

### The Problem

My blog has an autopilot system that automatically generates posts for Twitter, LinkedIn, and Newsletter every time I publish an article. It works great... most of the time. But sometimes the AI produces:

- 🐦 Generic tweets without hooks
- 💼 LinkedIn posts without proper structure
- 📧 Newsletter intros that reveal too much (or too little)

I needed a way to **evaluate quality BEFORE publishing** and, if something doesn't pass, improve it automatically.

### The Solution

**autopilot-ctrl** uses GitHub Copilot CLI to:

1. **Audit** content against platform-specific criteria
2. Assign a **quality score** (0-10)
3. **Identify specific issues**
4. **Generate improved versions** of failing content

```
                               📊 Audit Results                                
┌─────────────┬─────────┬───────────┬─────────────────────────────────────────┐
│ Platform    │  Score  │  Status   │ Issues                                  │
├─────────────┼─────────┼───────────┼─────────────────────────────────────────┤
│ Twitter     │ 3.0/10  │ [XX] FAIL │ No hook, missing hashtags               │
│ Linkedin    │ 7.0/10  │ [OK] PASS │ -                                       │
│ Newsletter  │ 8.0/10  │ [OK] PASS │ -                                       │
└─────────────┴─────────┴───────────┴─────────────────────────────────────────┘
```

## Demo

{{< youtube KNjx5IB8jr8 >}}

**Available commands:**

```bash
# Check that Copilot CLI is installed
python -m ctrl check

# Audit content
python -m ctrl audit content.json

# Fix failing content
python -m ctrl fix content.json --apply
```

**Screenshots of the flow:**

![1. Autopilot-Ctrl Introduction](PS_Autopilot_Intro.png)

![2. Copilot CLI Verification](PS_Autopilot_Check.png)

![3. Sample Content](PS_Autopilot_SampleContent.png)

![4. Audit Results](PS_Autopilot_Audit.png)

![5. Content Improved by Copilot](PS_Autopilot_Fix.png)

**Source code:** [github.com/Dalaez/datalaria/autopilot/ctrl](https://github.com/Dalaez/datalaria-website)

## My Experience with GitHub Copilot CLI

### 🚀 How I Used Copilot CLI

The magic of autopilot-ctrl lies in how it integrates Copilot CLI in non-interactive mode:

```python
# auditor.py
result = subprocess.run(
    ['copilot', '-s', '--no-ask-user', '-p', prompt],
    capture_output=True,
    text=True,
    timeout=60,
    encoding='utf-8'
)
```

Each audit sends a structured prompt to Copilot CLI and parses the natural language response to extract:
- Numeric score (e.g., "Rating: 7/10")
- List of issues (e.g., "No engagement", "Generic hook")
- Improvement suggestions

### 💡 What I Learned

1. **Flag order matters**: `-p` MUST be the last argument
2. **Simple prompts work better**: Long, structured prompts in non-interactive mode return empty responses
3. **Copilot responds in natural language**: I had to create flexible parsers to extract data from responses like "**Rating: 7/10**"

### ⚡ The Impact on My Workflow

Before autopilot-ctrl, I manually reviewed every generated post. Now:

1. `git push` → Autopilot generates content
2. `python -m ctrl audit generated_content.json` → Copilot evaluates
3. If something fails → `python -m ctrl fix` generates improvements
4. Approved content → Gets published automatically

**Time saved**: ~15 minutes per publication.

### 🛠️ Tech Stack

- **Python + Click**: CLI framework
- **Rich**: Terminal UI with tables and colors
- **GitHub Copilot CLI**: AI evaluation engine
- **YAML configs**: Customizable prompts per platform

---

## Conclusion

autopilot-ctrl demonstrates that GitHub Copilot CLI isn't just for generating code. It's a powerful tool for **integrating AI into any pipeline** - in this case, content quality evaluation.

If you have a system that generates content automatically, consider adding a "quality gate" with Copilot CLI. Your audience (and your engagement metrics) will thank you.

**Questions?** Drop them in the comments 👇

---

*This post is part of the [Autopilot Project](https://datalaria.com/es/posts/ai_agents_part/) series, where I document how I automate content creation and publishing using AI.*
