from tuned_common import get_model, safe_generate
from pathlib import Path
import datetime as dt

TESTS = [
    {"sender": "QuickTech Inc.", "receiver": "Ms. Patel", "subject": "Product demo scheduling"},
    {"sender": "GreenLeaf HR",   "receiver": "Alex Chen", "subject": "Interview confirmation"},
    {"sender": "Nova Logistics", "receiver": "Priya Rao", "subject": "Delay and new delivery ETA"},
]

def prompt_v1(s, r, subj):
    return (
        f"Write a professional email from {s} to {r} about '{subj}'. "
        "Keep it 120–150 words with greeting, body, and closing."
    )

def prompt_v2(s, r, subj):
    return (
        "TASK: Write a formal business email.\n"
        f"FROM: {s}\nTO: {r}\nSUBJECT/TOPIC: {subj}\n\n"
        "STYLE:\n- Polite, concise, professional\n- Active voice; clear call to action\n"
        "FORMAT:\n- Suggested Subject line at top\n- Greeting, exactly 2 short paragraphs, closing\n- 120–150 words\n"
        "GUARDRAILS:\n- No emojis/markdown/placeholders\n- American English\n"
    )

def score_output(text: str) -> int:
    """
    Naive heuristic scorer (0–5). Upgrade later or do human review.
    +1 Subject present, +1 greeting present, +1 closing present,
    +1 within ~150 words, +1 contains action/next step words.
    """
    score = 0
    lower = text.lower()
    if "subject:" in lower[:60]: score += 1
    if any(g in lower for g in ["dear ", "hello ", "hi "]): score += 1
    if any(c in lower for c in ["regards", "sincerely", "best,"]): score += 1
    words = len(text.split())
    if 100 <= words <= 170: score += 1
    if any(x in lower for x in ["schedule", "confirm", "next steps", "please reply", "let me know"]): score += 1
    return score

def run():
    model = get_model({"temperature": 0.3, "max_output_tokens": 400})
    rows = []
    for t in TESTS:
        p1 = prompt_v1(**t)
        p2 = prompt_v2(**t)

        out1 = safe_generate(model, p1)
        out2 = safe_generate(model, p2)

        s1 = score_output(out1)
        s2 = score_output(out2)

        rows.append((t, s1, s2))

    # Print summary and write to logs
    ts = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log = Path(__file__).resolve().parents[1] / "logs" / f"eval_{ts}.txt"
    log.parent.mkdir(parents=True, exist_ok=True)

    with log.open("w", encoding="utf-8") as f:
        total1 = total2 = 0
        for t, s1, s2 in rows:
            f.write(f"{t}\nV1={s1}  V2={s2}\n---\n")
            total1 += s1
            total2 += s2
        f.write(f"\nTOTAL  V1={total1}  V2={total2}\n")
    print(f"✅ Wrote evaluation to {log}")

if __name__ == "__main__":
    run()