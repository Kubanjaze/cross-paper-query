# Phase 78 — Cross-Paper Synthesis Query Against Memory

**Version:** 1.1 | **Tier:** Micro | **Date:** 2026-03-28

## Goal
Demonstrate cross-paper synthesis querying — simulating a Phase 04 memory store. Given SAR data from multiple "papers" (simulated), ask Claude to synthesize findings across sources and identify consensus/conflicts.

CLI: `python main.py --n-papers 3`

Outputs: synthesis_result.json, synthesis_report.txt

## Logic
1. Create simulated memory store: 3 "papers" with overlapping compound data and SAR conclusions
2. Include a deliberate conflict (metabolic stability: PMC_002 vs PMC_003)
3. Build a synthesis query that references all papers
4. Send to Claude with memory context + query
5. Parse structured synthesis: consensus, conflicts, knowledge_gaps, confidence, summary

## Key Concepts
- Cross-source synthesis (combining findings from multiple papers)
- Simulated memory store (JSON) representing Phase 04 data
- Conflict detection in SAR literature
- Knowledge gap identification
- Confidence scoring based on evidence quality

## Verification Checklist
- [x] 3 simulated paper memories created
- [x] Claude identifies consensus (6 items) and conflicts (1 item)
- [x] Metabolic stability conflict correctly detected
- [x] 7 knowledge gaps identified
- [x] Structured output parseable
- [x] --help works
- [x] Cost < $0.02

## Results
| Metric | Value |
|--------|-------|
| Papers in memory | 3 |
| Consensus findings | 6 |
| Conflicts detected | 1 (metabolic stability: PMC_002 vs PMC_003) |
| Knowledge gaps | 7 |
| Confidence | 0.72 |
| Total tokens | in=807 out=719 |
| Est. cost | $0.0035 |

Key findings:
- Claude detected the deliberate conflict about metabolic stability between PMC_002 and PMC_003
- Confidence dropped from ~0.85 to 0.72 due to the unresolved conflict
- Identified actionable gaps: no in vivo PK data, no crystal structure, no off-target selectivity
- CF3 superiority confirmed across all scaffold classes (consensus)
- Synthesis summary was coherent and actionable

## Risks
- Simulated papers — real memory store would have more complex overlaps
- Single API call — production would need iterative refinement queries
