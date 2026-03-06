---
name: chaos-memory
description: Hybrid search memory system for AI agents. Manual search and storage - auto-capture is opt-in only.
homepage: https://github.com/hargabyte/Chaos-mind
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "install":
          [
            {
              "id": "chaos-install",
              "kind": "shell",
              "command": "bash install.sh",
              "label": "Install CHAOS Memory",
            },
          ],
      },
  }
---

# CHAOS Memory

**C**ontext-aware **H**ierarchical **A**utonomous **O**bservation **S**ystem

Hybrid search memory for AI agents with 4 retrieval signals:
- **BM25** - Keyword matching
- **Vector** - Semantic similarity  
- **Graph** - Relationship bonuses
- **Heat** - Access patterns + priority

---

## 🤖 For AI Agents: How to Use This Tool

**First time?** Run this to see the complete reference:
```bash
chaos-cli --help
```

**Quick workflow:**
1. **Before a task:** `chaos-cli search "keywords" --mode index --limit 10`
2. **During a task:** `chaos-cli store "important fact" --category decision --priority 0.9`
3. **After a task:** `chaos-cli list 10`

**Token savings:** Use `--mode index` for 90% token savings (~75 tokens/result)

**More help:** Run `chaos help-agents` for the AI-optimized reference guide.

---

## Quick Start

After installation, use `chaos-cli`:

```bash
# Search memories
chaos-cli search "pricing decisions" --limit 5

# Store a memory
chaos-cli store "Enterprise tier: $99/month" --category decision

# List recent
chaos-cli list 10
```

---

## Search Memories

**Quick search** (summary mode):
```bash
chaos-cli search "architecture patterns" --mode summary --limit 5
```

**Fast scan** (index mode, 90% token savings):
```bash
chaos-cli search "team decisions" --mode index --limit 10
```

**Full detail**:
```bash
chaos-cli search "model selection" --mode full --limit 3
```

**Modes:**
| Mode | Tokens/Result | Use Case |
|------|---------------|----------|
| index | ~75 | Quick scan, many results |
| summary | ~250 | Balanced (default) |
| full | ~750 | Deep dive |

---

## Store Memory

```bash
# Decision
chaos-cli store "Qwen3-1.7B is default model" --category decision --priority 0.9

# Core fact
chaos-cli store "Database runs on port 3307" --category core --priority 0.7

# Research finding
chaos-cli store "43x speedup with think=false" --category research --priority 0.8
```

**Categories:** decision, core, semantic, research

**Priority:** 0.0-1.0 (higher = more important)

---

## Get by ID

```bash
chaos-cli get <memory-id>
```

---

## List Recent

```bash
chaos-cli list        # Default 10
chaos-cli list 20     # Show 20
```

---

## Auto-Capture (Optional - Opt-In Only)

**⚠️ DISABLED BY DEFAULT for privacy.**

To enable auto-capture:

1. **Review privacy implications** - reads your session transcripts
2. **Edit config:** `nano ~/.chaos/config/consolidator.yaml`
3. **Set:** `auto_capture.enabled: true`
4. **Configure paths:** Add your session directories to `auto_capture.sources`
5. **Install Ollama:** https://ollama.com (if not already installed)
6. **Pull model:** `ollama pull qwen3:1.7b`
7. **Test:** `chaos-consolidator --auto-capture --once`

**What it extracts:** Decisions, facts, insights  
**What it skips:** Greetings, filler, acknowledgments  
**Where it runs:** 100% local (your machine, no external APIs)  
**Speed:** 2.6s per message (~42s per 16-message session)

**Privacy:** Only processes files you explicitly configure. See SECURITY.md for details.

---

## 🔗 Enhanced Capabilities

CHAOS Memory integrates with other tools for deeper intelligence:

### Cortex (cx) - Semantic Code Anchoring

**What it does:** Anchors memories to specific code locations and files

**Why use it:** Memories become context-aware - "this decision affects Auth.tsx lines 45-67"

**How it works:**
- CHAOS detects if `cx` is available at startup
- Automatically creates semantic links: `memory → code location`
- Search results include related code snippets

**Install Cortex:**
```bash
# Cortex is a separate tool
# Install from: https://github.com/hargabyte/cortex
```

---

## Requirements

- **Dolt** - Version-controlled database
- **Ollama** - Local LLM inference (for auto-capture)
- **Go 1.21+** - To build from source (optional)

The install script handles dependencies automatically.

---

## Security & Privacy

**Data Storage:** All memories stored locally on your machine (`~/.chaos/db`)
- No cloud sync or external transmission
- Your data never leaves your computer
- Database is version-controlled (Dolt) for auditability

**Auto-Capture (Opt-In):**
- **Disabled by default** - you must explicitly enable and configure
- Requires manual configuration of session paths in `~/.chaos/config.yaml`
- Only processes files you explicitly specify in `auto_capture.sources`
- Runs locally using your own Ollama instance (no external API calls)
