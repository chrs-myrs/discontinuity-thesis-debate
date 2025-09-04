---
argument-hint: [start phase1|round 1a|positions|status]
description: Main debate orchestration - start phases, manage rounds, track progress
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Discontinuity Thesis Debate Command

## Usage: /debate $1

### Available Subcommands:

**`/debate start phase1`** - Begin Phase 1: Foundation Setting
- Triggers opening position rounds from all experts
- Creates debate tracking file
- Sets up evidence collection framework

**`/debate round 1a`** - Start specific round (format: phase + letter)
- 1a: Opening positions
- 1b: Disagreement mapping  
- 2a-2d: Research-driven analysis
- 3a-3c: Stress testing rounds
- 4a-4b: Cross-examination
- 5a-5b: Synthesis rounds
- 6: Final resolution

**`/debate positions`** - Current expert position summary
- Shows each expert's current stance
- Highlights key disagreements
- Tracks position evolution over time

**`/debate status`** - Debate progress tracker
- Current phase and round
- Completed analysis topics
- Outstanding research requests
- Expert participation summary

---

## Processing Command: $1

Based on your request "$1", I'll coordinate the appropriate debate activity:

### If starting Phase 1:
I'll gather opening positions from all five experts:
- @dr-chen-inevitability (Discontinuity Advocate)
- @dr-martinez-adaptation (Adaptation Economist)  
- @dr-patel-tech-realist (Technology Realist)
- @dr-vasquez-historian (Historical Comparativist)
- @dr-thompson-coordination (Coordination Theorist)

Each expert will provide:
1. Core thesis statement (300 words max)
2. Three key supporting arguments with evidence
3. Three testable predictions with confidence levels
4. Falsification criteria (what would change their mind)

### If requesting positions:
I'll provide a structured summary of where each expert currently stands, highlighting:
- Areas of agreement and disagreement
- Confidence levels in key claims
- Evidence requirements identified
- Research gaps that need addressing

### If checking status:
I'll show:
- Current debate phase and progress
- Topics analyzed so far
- Outstanding questions and research needs
- Next steps in the structured process

### If starting specific round:
I'll coordinate the appropriate activities for that round based on the 6-phase framework.

Ready to proceed with: **$1**