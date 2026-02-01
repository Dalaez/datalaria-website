# Autopilot-Ctrl: AI Agent Content Auditor

A CLI tool that uses GitHub Copilot CLI to audit and improve AI-generated social media content.

## Features

- 🔍 **Audit** - Evaluate content quality using `gh copilot suggest`
- 🔧 **Fix** - Auto-generate improvements for failing content
- 📊 **Report** - Generate detailed audit reports

## Installation

```bash
cd autopilot
pip install -r ctrl/requirements.txt
```

## Usage

```bash
# Audit generated content
python -m ctrl.cli audit generated_content.json

# Audit specific platform
python -m ctrl.cli audit -p twitter generated_content.json

# Generate fixes for failing content
python -m ctrl.cli fix generated_content.json

# Apply fixes automatically
python -m ctrl.cli fix --apply generated_content.json
```

## Requirements

- Python 3.10+
- GitHub CLI (`gh`) with Copilot extension
- Valid GitHub Copilot subscription

## Configuration

Edit `ctrl/config/audit_rules.yaml` to customize quality criteria per platform.
