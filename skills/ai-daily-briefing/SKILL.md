---
name: ai-daily-briefing
version: 1.0.0
description: "Start every day focused. Get a morning briefing with overdue tasks, today's priorities, calendar overview, and context from recent meetings. Works with ai-meeting-notes to-do list. No setup. Just say 'briefing'."
author: Jeff J Hunter
homepage: https://jeffjhunter.com
tags: [daily-briefing, morning-routine, productivity, todo, priorities, calendar, focus, daily-ops, task-management, planning]
---

# ☀️ AI Daily Briefing

**Start every day focused. Know exactly what matters.**

Get a morning briefing with overdue tasks, today's priorities, and context from recent work.

No setup. Just say "briefing".

---

## ⚠️ CRITICAL: BRIEFING FORMAT (READ FIRST)

**When the user asks for a briefing, you MUST respond with this EXACT format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ DAILY BRIEFING — [Day], [Month] [Date], [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ OVERDUE ([X] items)
• Task 1 — was due [date]
• Task 2 — was due [date]

📅 TODAY'S PRIORITIES
1. [ ] Priority task 1 — [deadline/context]
2. [ ] Priority task 2 — [deadline/context]
3. [ ] Priority task 3 — [deadline/context]

📆 CALENDAR
• [Time] — [Event]
• [Time] — [Event]
• [Time] — [Event]

💡 CONTEXT (from recent meetings)
• [Key insight 1]
• [Key insight 2]
• [Key insight 3]

🎯 FOCUS FOR TODAY
[One sentence: What's the ONE thing that matters most today?]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### MANDATORY RULES

| Rule | Requirement |
|------|-------------|
| **ONE response** | Complete briefing in a single message |
| **Sections in order** | Overdue → Priorities → Calendar → Context → Focus |
| **Skip empty sections** | If no overdue items, skip that section |
| **Max 5 per section** | Keep it scannable (except calendar, show all) |
| **Focus statement** | Always end with ONE thing to focus on |

---

## Why This Exists

Every morning you face the same questions:
- What's overdue?
- What's due today?
- What meetings do I have?
- What's the context I need to remember?

Instead of checking 5 different places, get one briefing.

---

## What It Does

| Input | Output |
|-------|--------|
| "briefing" | ✅ Complete daily overview |
| "what's overdue?" | ✅ Overdue tasks only |
| "what's on my calendar?" | ✅ Today's schedule |
| "what should I focus on?" | ✅ Priority recommendation |
| "weekly preview" | ✅ Week-ahead view |

---

## Data Sources

The briefing pulls from these locations (if they exist):

### 1. To-Do List (from ai-meeting-notes)

**Location:** `todo.md` in workspace root

```markdown
# To-Do List

## ⚠️ Overdue
| # | Task | Owner | Due | Source |
|---|------|-------|-----|--------|
| 3 | Send proposal | @You | Jan 25 | client-call.md |

## 📅 Due Today
| # | Task | Owner | Source |
|---|------|-------|--------|
| 5 | Review budget | @You | team-sync.md |

## 📆 This Week
| # | Task | Owner | Due | Source |
|---|------|-------|-----|--------|
| 1 | Finalize report | @You | Fri | planning.md |
```

### 2. Meeting Notes

**Location:** `meeting-notes/` folder

- Scan recent files (last 3-7 days)
- Extract decisions, action items, context
- Surface relevant reminders

### 3. Calendar (if available)

- Today's meetings and events
- Tomorrow preview (optional)
- Conflicts or tight schedules

### 4. Memory/Context Files (if using ai-persona-os)

**Locations:**
- `MEMORY.md` — Permanent facts
- `memory/[today].md` — Session notes
- `USER.md` — User preferences

---

## Trigger Phrases

Any of these should trigger a briefing:

| Phrase | Action |
|--------|--------|
| "briefing" | Full daily briefing |
| "daily briefing" | Full daily briefing |
| "morning briefing" | Full daily briefing |
| "what's on my plate?" | Full daily briefing |
| "start my day" | Full daily briefing |
| "what do I need to know?" | Full daily briefing |
| "what's today look like?" | Full daily briefing |
| "give me the rundown" | Full daily briefing |

---

## Works Best With

| Skill | Why |
|-------|-----|
| **ai-meeting-notes** | Creates the to-do list this pulls from |
| **ai-persona-os** | Provides memory and context |

**Standalone:** Works without other skills — just won't have meeting context or persistent todo.

---

## Quick Start

**Day 1:**
```
You: "briefing"
AI: [Shows briefing based on available data, or offers to set up]
```

**After using ai-meeting-notes:**
```
You: "briefing"
AI: [Shows full briefing with overdue items, priorities, context]
```

---

## Customization

Want to customize your briefing? Tell me your preferences:

**Time preferences:**
- "I start work at 6am" → Earlier context
- "Show tomorrow's first meeting" → Tomorrow preview

**Section preferences:**
- "Always show weather" → Add weather
- "Skip calendar" → Omit calendar section
- "Include quotes" → Add motivational quote

**Priority preferences:**
- "Health tasks are always P1" → Boost health items
- "Family first" → Prioritize family commitments

---

## Example Briefing

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ DAILY BRIEFING — Tuesday, February 3, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ OVERDUE (2 items)
• Send Acme proposal — was due Feb 1
• Review Week 2 training materials — was due Jan 31

📅 TODAY'S PRIORITIES
1. [ ] Anne follow-up call — 2pm today
2. [ ] Finalize Week 3 training content — EOD
3. [ ] Prep for Makati trip — flights need booking
4. [ ] Respond to Karlen re: workflow docs
5. [ ] Clear overdue Acme proposal

📆 CALENDAR
• 10:00 AM — Team standup (30 min)
• 2:00 PM — Anne follow-up call (1 hour)
• 4:30 PM — Workshop dry run (90 min)

💡 CONTEXT (from recent meetings)
• Anne partnership confirmed — ready to move forward (from anne-call)
• OpenClaw bot architecture changing to specialists (from pm-meeting)
• Makati trip deadline approaching — need flights by Friday

🎯 FOCUS FOR TODAY
Get the Acme proposal out first thing — it's 2 days overdue and blocking the deal.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
