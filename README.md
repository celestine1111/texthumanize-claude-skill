# TextHumanize — Claude Code Skill

> Created by [mindiam.com](https://mindiam.com) — an AI agency building intelligent tools and automations.
> Implemented in [seobetter.com](https://seobetter.com) — a content creation plugin that optimizes for AI SEO, LLM citations, traditional SEO, and GEO (Generative Engine Optimization).

A Claude Code skill that brings [TextHumanize](https://github.com/ksanyok/TextHumanize) features into your Claude Code workflow. Transform AI-generated text into natural, human-like writing — 100% offline, zero external API calls.

## Install

### Option 1 — One-liner (recommended)

```bash
git clone https://github.com/YOUR_USERNAME/texthumanize-claude-skill
cd texthumanize-claude-skill
bash install.sh
```

### Option 2 — Manual

1. Copy `.claude/commands/humanize.md` to `~/.claude/commands/humanize.md`
2. Copy `scripts/humanize_runner.py` to `~/.claude/scripts/humanize_runner.py`
3. Run `pip install texthumanize`

### Option 3 — VS Code with Claude extension

In VS Code with the Claude extension, skills in `~/.claude/commands/` are available globally. Follow Option 1 or 2 above, then reload VS Code.

## Usage

In any Claude Code session, type:

```
/humanize
```

Then paste the text you want to process, or provide options:

| Command | Description |
|---------|-------------|
| `/humanize` | Humanize pasted text at intensity 60 |
| `/humanize --intensity 80` | Stronger humanization |
| `/humanize --until-human` | Iterate until AI score drops below 35% |
| `/humanize --detect` | Only check AI detection score, no edits |
| `/humanize --variants 3` | Generate 3 variants, return the most natural |
| `/humanize report.txt` | Humanize a file |
| `/humanize --lang de` | Force German language mode |
| `/humanize --profile academic` | Target academic writing style |
| `/humanize --preserve "CompanyName,ProductX"` | Keep specific words unchanged |

## Features

Powered by TextHumanize's full pipeline:

- **38-stage processing pipeline** — watermark removal, debureaucratization, structure diversification, entropy injection, grammar correction, coherence repair
- **PHANTOM™** — gradient-guided adversarial optimization
- **ASH™** — adaptive signature humanization matching real human writing profiles
- **3-layer AI detection** — 18-metric heuristic + 35-feature logistic regression + neural MLP
- **25 languages** — deep support for EN, RU, UK, DE; broad support for FR, ES, IT, PL, and more
- **Intensity 0–100** — fine-grained control
- **Style profiles** — casual, formal, academic, blog, social
- **100% offline** — no data leaves your machine

## Requirements

- Python 3.8+
- `pip install texthumanize`
- Claude Code (VS Code extension or CLI)

## License

MIT License — Copyright (c) 2026 [mindiam.com](https://mindiam.com)

> Note: This skill depends on [TextHumanize](https://github.com/ksanyok/TextHumanize) which is licensed for Personal Use Only by its author. Commercial use requires a separate license from the TextHumanize author.
