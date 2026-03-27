import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse, os, json, re, warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
import anthropic

load_dotenv()
os.environ.setdefault("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))

# Simulated memory store — 3 papers with overlapping SAR findings
PAPER_MEMORIES = [
    {
        "paper_id": "PMC_001",
        "title": "CETP Inhibition by Benzimidazole Derivatives",
        "year": 2023,
        "key_findings": [
            "Electron-withdrawing groups (CF3, CN) on benzimidazole scaffold increase CETP inhibition (pIC50 7.5-8.1)",
            "Halogen substituents (F, Cl, Br) show moderate activity (pIC50 7.0-7.5)",
            "The benzimidazole core is essential for binding to CETP hydrophobic tunnel",
            "LogP > 3.5 correlates with reduced oral bioavailability",
        ],
        "compounds": ["benz_004_CF3 (pIC50=8.10)", "benz_005_CN (pIC50=7.95)", "benz_001_F (pIC50=7.25)"],
    },
    {
        "paper_id": "PMC_002",
        "title": "Indole-Based CETP Inhibitors: SAR and Optimization",
        "year": 2024,
        "key_findings": [
            "Indole scaffold shows consistently high potency across R-groups (mean pIC50=7.9)",
            "CF3 substitution yields highest activity in indole series (pIC50=8.55)",
            "The indole NH is critical for a key hydrogen bond with CETP Asp240",
            "Indole series has superior metabolic stability compared to benzimidazole",
        ],
        "compounds": ["ind_006_CF3 (pIC50=8.55)", "ind_007_CN (pIC50=8.35)", "ind_003_Br (pIC50=7.65)"],
    },
    {
        "paper_id": "PMC_003",
        "title": "Comparative SAR of Heterocyclic CETP Inhibitors",
        "year": 2024,
        "key_findings": [
            "Scaffold potency ranking: indole > quinoline > benzimidazole > pyridine",
            "CF3 is the optimal substituent across ALL scaffold classes",
            "Pyridine scaffold shows poor activity due to insufficient hydrophobic contact",
            "Benzimidazole is MORE metabolically stable than indole (contradicts PMC_002)",
            "Activity cliffs observed between F and H substituents in all series",
        ],
        "compounds": ["ind_006_CF3 (pIC50=8.55)", "quin_006_CF3 (pIC50=8.25)", "pyr_006_CF3 (pIC50=6.85)"],
    },
]

SYNTHESIS_SYSTEM = """You are a medicinal chemistry expert performing cross-paper synthesis.
Given findings from multiple papers stored in a memory system, identify:
1. Consensus findings (agreed across papers)
2. Conflicts (contradictory claims between papers)
3. Knowledge gaps (areas not covered by any paper)
4. Overall confidence in the SAR model

Respond with ONLY valid JSON:
{
  "consensus": ["finding 1", "finding 2"],
  "conflicts": [{"claim_a": "paper X says...", "claim_b": "paper Y says...", "resolution": "likely explanation"}],
  "knowledge_gaps": ["gap 1", "gap 2"],
  "confidence": 0.0-1.0,
  "synthesis_summary": "2-3 sentence overall synthesis"
}"""


def main():
    parser = argparse.ArgumentParser(
        description="Phase 78 — Cross-paper synthesis query against simulated memory",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--n-papers", type=int, default=3, help="Number of papers to include")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001", help="Model ID")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    papers = PAPER_MEMORIES[:args.n_papers]
    client = anthropic.Anthropic()

    print(f"\nPhase 78 — Cross-Paper Synthesis Query")
    print(f"Model: {args.model} | Papers in memory: {len(papers)}\n")

    # Build memory context
    memory_context = "MEMORY STORE — Papers on CETP Inhibitors:\n\n"
    for p in papers:
        memory_context += f"--- {p['paper_id']}: {p['title']} ({p['year']}) ---\n"
        memory_context += "Key findings:\n"
        for f in p["key_findings"]:
            memory_context += f"  - {f}\n"
        memory_context += f"Compounds: {', '.join(p['compounds'])}\n\n"

    query = (
        "SYNTHESIS QUERY: Based on all papers in memory, what is the current consensus "
        "on CETP inhibitor SAR? Identify any conflicts between papers and knowledge gaps. "
        "Pay special attention to the metabolic stability claims."
    )

    user_msg = f"{memory_context}\n{query}"

    print(f"Memory context: {len(papers)} papers, {sum(len(p['key_findings']) for p in papers)} findings")
    print(f"Query: Cross-paper synthesis with conflict detection\n")

    response = client.messages.create(
        model=args.model,
        max_tokens=1024,
        system=SYNTHESIS_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(b.text for b in response.content if hasattr(b, "text"))
    total_input = response.usage.input_tokens
    total_output = response.usage.output_tokens

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        synthesis = json.loads(match.group())
    else:
        synthesis = {"parse_error": True, "raw": text}

    # Display results
    print("CONSENSUS FINDINGS:")
    for c in synthesis.get("consensus", []):
        print(f"  + {c}")

    print("\nCONFLICTS:")
    for c in synthesis.get("conflicts", []):
        print(f"  ! {c.get('claim_a', '?')}")
        print(f"    vs {c.get('claim_b', '?')}")
        print(f"    Resolution: {c.get('resolution', '?')}")

    print("\nKNOWLEDGE GAPS:")
    for g in synthesis.get("knowledge_gaps", []):
        print(f"  ? {g}")

    print(f"\nConfidence: {synthesis.get('confidence', '?')}")
    print(f"Summary: {synthesis.get('synthesis_summary', 'N/A')}")

    cost = (total_input / 1e6 * 0.80) + (total_output / 1e6 * 4.0)

    report = (
        f"\nPhase 78 — Cross-Paper Synthesis Report\n{'='*50}\n"
        f"Model: {args.model} | Papers: {len(papers)}\n"
        f"Consensus items: {len(synthesis.get('consensus', []))}\n"
        f"Conflicts found: {len(synthesis.get('conflicts', []))}\n"
        f"Knowledge gaps: {len(synthesis.get('knowledge_gaps', []))}\n"
        f"Confidence: {synthesis.get('confidence', '?')}\n\n"
        f"Tokens: in={total_input} out={total_output}\nCost: ${cost:.4f}\n"
    )
    print(report)

    with open(os.path.join(args.output_dir, "synthesis_result.json"), "w") as f:
        json.dump(synthesis, f, indent=2)
    with open(os.path.join(args.output_dir, "synthesis_report.txt"), "w") as f:
        f.write(report)
    print("Done.")


if __name__ == "__main__":
    main()
