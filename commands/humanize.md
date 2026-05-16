# Humanize Text

Transform the selected text or provided content into natural, human-like writing using the TextHumanize engine. This reduces AI-sounding patterns, varies sentence structure, and improves naturalness.

**Language support: 25 languages with automatic detection. Never ask the user what language their text is — always detect it automatically.**

Supported languages:
- Tier 1 (full 38-stage pipeline): English (en), Russian (ru), Ukrainian (uk), German (de)
- Tier 2 (~30 stages): French (fr), Spanish (es), Italian (it), Polish (pl), Portuguese (pt), Dutch (nl), Swedish (sv), Czech (cs), Romanian (ro), Hungarian (hu), Danish (da)
- Tier 3 (~20 stages): Arabic (ar), Chinese (zh), Japanese (ja), Korean (ko), Turkish (tr), Hindi (hi), Vietnamese (vi), Thai (th), Indonesian (id), Hebrew (he)
- Tier 0 (universal statistical): any other language

## Usage

```
/humanize [text or file path] [options]
```

**Options:**
- `--intensity 0-100` — How aggressively to transform (default: 60)
- `--lang auto` — Language (default: auto-detect from text). Only override if detection fails.
- `--profile casual|formal|academic|blog|social` — Writing style target (default: casual)
- `--until-human` — Keep iterating until AI detection score is below 35%
- `--detect` — Only run AI detection, don't humanize
- `--variants N` — Generate N variants and return the most natural one (default: 1)
- `--preserve word1,word2` — Comma-separated keywords to preserve unchanged

## What Claude Should Do

When the user invokes `/humanize`:

1. **Check if texthumanize is installed.** Run:
   ```bash
   python3 -c "import texthumanize" 2>&1
   ```
   If it fails, install it first:
   ```bash
   pip install texthumanize
   ```

2. **Determine the input text:**
   - If the user passed a file path, read that file
   - If the user passed text inline, use that
   - If no argument, ask the user to paste the text they want humanized

3. **Always use `--lang auto`** unless the user explicitly specifies a language. The engine detects the language from the text itself — do not guess or hardcode a language.

4. **Run the humanize script** using the arguments provided:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/humanize_runner.py" --text "..." --intensity 60 --lang auto --profile casual
   ```

5. **Parse the JSON output** from the script and present:
   - The humanized text (ready to copy/use)
   - Language that was detected (e.g., "Detected: German")
   - AI score before and after (e.g., "AI score: 87% → 22%")
   - Change ratio (e.g., "18% of text was modified")
   - A brief list of what kinds of changes were made

6. **If `--detect` only:** Report the AI detection score, verdict (human/mixed/ai_generated), and confidence level.

7. **If `--variants`:** Run multiple variants and automatically select the one with the lowest AI detection score. Show the winner and its score.

8. **For mixed-language content:** If the user's project writes content in multiple languages simultaneously, run each language block separately with `--lang auto` so each gets the correct pipeline depth.

## Example Interactions

**User:** `/humanize --intensity 70` followed by pasting a German paragraph
**Claude:** Detects German automatically, runs the full German pipeline, shows the rewritten paragraph with "Detected: de" and before/after scores.

**User:** `/humanize article.txt --until-human`
**Claude:** Reads article.txt, auto-detects language, iterates until AI score < 35%, saves result to article_humanized.txt.

**User:** `/humanize --detect` followed by pasting Spanish text
**Claude:** Detects Spanish, reports only the detection analysis without modifying text.

**User:** `/humanize blog-post.txt --profile blog --intensity 55`
**Claude:** Reads the file, auto-detects language, applies blog-style humanization at intensity 55.

## Important Notes

- This tool works 100% offline — no API calls, no data sent anywhere, no language data uploaded
- Language detection runs on the first 500 chars of text using character trigram profiling
- Processing takes 300ms–2s per paragraph (Tier 1 languages); slightly faster for Tier 2/3
- For long documents, the text is automatically split into chunks at paragraph boundaries
- The `--until-human` flag may run 3–5 iterations for stubborn text
- Always show the user both the original and humanized text so they can review changes
- If language detection reports an unexpected language, the user can override with `--lang xx`
