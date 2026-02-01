# Demo Video Script - Autopilot-Ctrl CLI

## Video Info
- **Duration:** 3-4 minutes
- **Format:** Screen recording with voice narration (in English)
- **Tool:** OBS Studio (free) or Windows Game Bar (Win+G)

---

## SCENE 1: Introduction (30 sec)

**[Show terminal with banner]**

**Narration:**
> "Hi! I'm going to show you Autopilot-Ctrl, a CLI tool that uses GitHub Copilot CLI to audit AI-generated social media content."
>
> "The problem: My blog autopilot generates content automatically, but sometimes the AI produces posts that are too generic or have issues."
>
> "The solution: Use Copilot CLI to evaluate content quality BEFORE publishing."

**Commands:**
```powershell
cd c:\Users\dalae\OneDrive\Emprendiendo\datalaria\autopilot
python -m ctrl --help
```

---

## SCENE 2: Check Setup (20 sec)

**Narration:**
> "First, let's verify that GitHub Copilot CLI is properly installed."

**Commands:**
```powershell
python -m ctrl check
```

**Expected output:**
```
✅ GitHub CLI installed
   gh version 2.85.0
✅ Copilot CLI extension installed
✅ Setup looks good!
```

---

## SCENE 3: Show Sample Content (30 sec)

**Narration:**
> "Here's some AI-generated content that my autopilot system created. Let's see if it's good enough to publish."

**Commands:**
```powershell
cat ctrl\examples\sample_content.json
```

---

## SCENE 4: Run Audit (60 sec) - THE MAIN EVENT

**Narration:**
> "Now, let's audit this content using GitHub Copilot CLI. Under the hood, I'm calling copilot with the -p flag for non-interactive mode."

**Commands:**
```powershell
python -m ctrl audit ctrl\examples\sample_content.json
```

**While spinner runs:**
> "Copilot is now evaluating each platform's content against specific criteria like engagement, structure, and clarity..."

**When results appear:**
> "Look at this! Twitter scored 6 out of 10 - that's a WARNING. LinkedIn and Newsletter passed with 7 and 8. Copilot even detected issues like 'unattributed statistic' and 'generic hook'."

---

## SCENE 5: Fix Command (45 sec)

**Narration:**
> "When content fails the audit, we can ask Copilot to fix it automatically."

**Commands:**
```powershell
python -m ctrl fix ctrl\examples\sample_content.json
```

**Show the improved content output:**
> "Copilot rewrites the failing content, addressing the specific issues it found. Much better!"

---

## SCENE 6: Wrap-up (30 sec)

**Narration:**
> "This tool integrates into my existing GitHub Actions workflow. When I push a blog post, the autopilot generates content. Then autopilot-ctrl audits it before publishing - ensuring quality AI-generated content."
>
> "Thanks for watching! The code is available on GitHub."

**[Show GitHub repo URL]**

---

## Recording Tips

1. **Clean terminal:** Close all tabs, use a clean PowerShell window
2. **Font size:** Increase font to 16-18pt for readability
3. **Practice:** Run through commands 1-2 times before recording
4. **Pace:** Speak slowly and clearly
5. **Mistakes:** If you make a mistake, just keep going or start that scene over
