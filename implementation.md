# Phase 78 — Cross-Paper Synthesis Query Against Memory

**Version:** 1.0 | **Tier:** Micro | **Date:** 2026-03-28

## Goal
Demonstrate cross-paper synthesis querying — simulating a Phase 04 memory store. Given SAR data from multiple "papers" (simulated), ask Claude to synthesize findings across sources and identify consensus/conflicts.

CLI: `python main.py --n-papers 3`

Outputs: synthesis_result.json, synthesis_report.txt

## Logic
1. Create simulated memory store: 3 "papers" with overlapping compound data and SAR conclusions
2. Build a synthesis query that references all papers
3. Send to Claude with memory context + query
4. Parse structured synthesis: consensus findings, conflicts, confidence, gaps
5. Demonstrates the memory + query pattern without a running memory server

## Key Concepts
- Cross-source synthesis (combining findings from multiple papers)
- Simulated memory store (JSON) representing Phase 04 data
- Synthesis query pattern: "What do these papers agree/disagree on?"
- Conflict resolution in SAR literature

## Verification Checklist
- [ ] 3 simulated paper memories created
- [ ] Claude identifies consensus and conflicts
- [ ] Structured output with findings, conflicts, gaps
- [ ] --help works
- [ ] Cost < $0.02

## Risks
- Simulated papers may be too consistent — add deliberate conflicts
- Without real memory server, pattern is demonstrative only
