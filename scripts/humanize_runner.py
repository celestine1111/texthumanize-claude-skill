#!/usr/bin/env python3
"""
Runner script for TextHumanize — called by the Claude Code /humanize skill.
Outputs JSON so Claude can parse and present results cleanly.
"""

import argparse
import json
import sys
import os


def ensure_installed():
    try:
        import texthumanize  # noqa: F401
    except ImportError:
        import subprocess
        print(json.dumps({"error": "texthumanize not installed. Run: pip install texthumanize"}))
        sys.exit(1)


def run_detect(text: str) -> dict:
    from texthumanize import detect_ai
    result = detect_ai(text)
    score = result.score if hasattr(result, "score") else result.get("score", 0)
    verdict = result.verdict if hasattr(result, "verdict") else result.get("verdict", "unknown")
    confidence = result.confidence if hasattr(result, "confidence") else result.get("confidence", 0)
    return {
        "mode": "detect",
        "score": round(score * 100 if score <= 1 else score, 1),
        "verdict": verdict,
        "confidence": round(confidence * 100 if confidence <= 1 else confidence, 1),
    }


def run_humanize(text: str, intensity: int, lang: str, profile: str,
                 until_human: bool, variants: int, preserve: list) -> dict:
    from texthumanize import humanize, humanize_until_human, humanize_variants

    resolved_lang = None if lang == "auto" else lang
    kwargs = {
        "intensity": intensity,
    }
    if resolved_lang:
        kwargs["lang"] = resolved_lang
    if profile:
        kwargs["profile"] = profile
    if preserve:
        kwargs["preserve"] = preserve

    if until_human:
        result = humanize_until_human(text, **kwargs)
    elif variants > 1:
        results = humanize_variants(text, n=variants, **kwargs)
        result = results[0] if results else humanize(text, **kwargs)
    else:
        result = humanize(text, **kwargs)

    def get(obj, attr, default=None):
        if hasattr(obj, attr):
            return getattr(obj, attr)
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return default

    score_before = get(result, "metrics_before")
    score_after = get(result, "metrics_after")

    if isinstance(score_before, dict):
        ai_before = score_before.get("artificiality_score", score_before.get("ai_score", None))
    elif hasattr(score_before, "artificiality_score"):
        ai_before = score_before.artificiality_score
    else:
        ai_before = None

    if isinstance(score_after, dict):
        ai_after = score_after.get("artificiality_score", score_after.get("ai_score", None))
    elif hasattr(score_after, "artificiality_score"):
        ai_after = score_after.artificiality_score
    else:
        ai_after = None

    changes = get(result, "changes", [])
    change_ratio = get(result, "change_ratio", 0)

    lang_used = get(result, "lang", resolved_lang or "auto-detected")

    return {
        "mode": "humanize",
        "text": get(result, "text", ""),
        "ai_score_before": round(ai_before * 100, 1) if ai_before is not None else None,
        "ai_score_after": round(ai_after * 100, 1) if ai_after is not None else None,
        "change_ratio": round((change_ratio or 0) * 100, 1),
        "changes_summary": changes[:10] if changes else [],
        "intensity_used": intensity,
        "lang_detected": lang_used,
        "until_human": until_human,
        "variants_generated": variants,
    }


def main():
    parser = argparse.ArgumentParser(description="TextHumanize runner for Claude Code skill")
    parser.add_argument("--text", help="Text to process (use - to read from stdin)")
    parser.add_argument("--file", help="Path to input file")
    parser.add_argument("--intensity", type=int, default=60, help="Humanization intensity 0-100")
    parser.add_argument("--lang", default="auto", help="Language code (en, ru, de, fr, ...)")
    parser.add_argument("--profile", default="casual",
                        choices=["casual", "formal", "academic", "blog", "social"],
                        help="Writing style profile")
    parser.add_argument("--until-human", action="store_true",
                        help="Iterate until AI score < 35%")
    parser.add_argument("--detect", action="store_true",
                        help="Only run AI detection, no humanization")
    parser.add_argument("--variants", type=int, default=1,
                        help="Number of variants to generate (best one returned)")
    parser.add_argument("--preserve", default="",
                        help="Comma-separated keywords to preserve unchanged")
    parser.add_argument("--output", help="Write humanized text to this file path")

    args = parser.parse_args()

    ensure_installed()

    # Resolve input text
    if args.file:
        if not os.path.exists(args.file):
            print(json.dumps({"error": f"File not found: {args.file}"}))
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text == "-" or args.text is None:
        text = sys.stdin.read()
    else:
        text = args.text

    text = text.strip()
    if not text:
        print(json.dumps({"error": "No input text provided"}))
        sys.exit(1)

    preserve = [w.strip() for w in args.preserve.split(",") if w.strip()] if args.preserve else []

    try:
        if args.detect:
            result = run_detect(text)
        else:
            result = run_humanize(
                text=text,
                intensity=args.intensity,
                lang=args.lang,
                profile=args.profile,
                until_human=args.until_human,
                variants=args.variants,
                preserve=preserve,
            )

        if args.output and result.get("text"):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result["text"])
            result["saved_to"] = args.output

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)


if __name__ == "__main__":
    main()
