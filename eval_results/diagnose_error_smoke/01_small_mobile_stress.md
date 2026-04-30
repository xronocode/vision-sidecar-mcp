# diagnose_error real-call smoke (1/1) — small_mobile_stress

**Date:** 2026-04-30
**Backend:** Ollama at INTERNAL-HOST:11434, qwen3-vl:8b
**Source:** vision-sidecar-mcp v0.3.0 (commit a785529)
**Fixture:** `eval_images/kombo/10_small_mobile_stress.png` (320×568 — hero with CTAs below fold)
**Args:** `viewport_hint="small_mobile"`, `error_context=None`

## Telemetry (BLOCK markers, in order)

```
[VisionSidecar][image][_validate_image][BLOCK_VALIDATE_IMAGE]   path=... size_bytes=61775 mime=image/png
[VisionSidecar][image][_preprocess_image][BLOCK_UPSCALE]        from_w=320 from_h=568 to_w=640 to_h=1136 factor=2 method=Lanczos
[VisionSidecar][image][_encode_image][BLOCK_ENCODE_IMAGE]       image_sha256=0991ec7a5fc8663d raw_bytes=61775 processed_bytes=266614 b64_chars=355488
[VisionSidecar][ollama][_call_ollama][BLOCK_CALL_OLLAMA]        phase=entry model=qwen3-vl:8b num_predict=8192 num_ctx=32768 prompt_chars=2251 suppress_thinking=1 response_json=1
HTTP/1.1 200 OK                                                 5.85s
[VisionSidecar][ollama][_call_ollama][BLOCK_CALL_OLLAMA]        phase=exit response_chars=839 wall_seconds=5.85 status=ok
[VisionSidecar][parse][_try_parse_json][BLOCK_PARSE_JSON]       result=ok path=direct
```

All 5 expected critical markers (`BLOCK_VALIDATE_IMAGE`, `BLOCK_UPSCALE`, `BLOCK_ENCODE_IMAGE`, `BLOCK_CALL_OLLAMA × 2`, `BLOCK_PARSE_JSON`) emitted with the documented field shape. **VF-002 satisfied** for the new tool: `</think>` prefill produced `response_chars=839 > 0` on the first attempt, no retry needed.

## Response (parsed JSON)

```json
{
  "error_type": "clipping",
  "description": "Hero section lacks primary action button below subhead. Visible hero heading and subhead present but no in-card primary action button (e.g. 'Start playing') below the subhead, indicating CTAs are clipped below visible fold.",
  "affected_elements": [
    {"label": "hero section", "location": "center"}
  ],
  "visible_error_text": null,
  "suggested_fixes": [
    "Ensure primary action button (e.g. 'Start playing') is positioned below the hero subhead within the visible viewport area",
    "Check CSS for overflow:hidden on hero container to prevent clipping of interactive elements",
    "Verify responsive breakpoints for hero section to ensure primary action button remains visible on small screens"
  ],
  "looks_correct": false,
  "confidence": {"overall": 0.95, "diagnosis": 0.9}
}
```

## Quality assessment (frontier-eyeball)

| Dimension | Verdict |
|---|---|
| `error_type` correctness | ✅ "clipping" matches the actual fault (CTAs below 568px fold) |
| `description` specificity | ✅ Names the exact missing element ("Start playing"), correctly identifies that it's clipped not absent |
| `affected_elements` granularity | ⚠️ Only 1 entry — could list each missing CTA separately, but acceptable |
| `visible_error_text` | ✅ Correct null (no error text rendered in the screenshot) |
| `suggested_fixes` actionability | ✅ All 3 are concrete: (1) layout positioning, (2) CSS overflow audit, (3) responsive breakpoints. The `overflow:hidden` suggestion is a slight red herring (the actual cause is viewport height, not overflow), but not harmful. |
| `looks_correct` | ✅ False, matches reality |
| `confidence.overall` | 0.95 — calibrated |
| Schema compliance | ✅ Valid JSON on first attempt, parse_error=null |
| Glyph preservation | n/a (no special glyphs in this fixture) |
| Wall time | 5.85s (comparable to analyze_structured) |

**Net:** the new tool produces useful, actionable output on a real layout-break case with no regression in the established VLM behavior (prefill works, sampling works, schema parsing works). Confirms `diagnose_error` is functional in v0.3.0.

## Caveats

- Single-fixture smoke. Full evaluation requires the synthetic `eval_images/errors/` dataset described in `docs/verification-plan.xml` SyntheticDatasets — scheduled for v0.3.1.
- Repository will benefit from negative tests too (well-rendered screenshots → `looks_correct=true`) once the dataset is built.
