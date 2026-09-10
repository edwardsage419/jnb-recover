# Scientific and Product Limits

**English** | [简体中文](SCIENTIFIC_LIMITS.zh-CN.md)

## Missing-value semantics

Some SigmaPlot cell states remain intentionally unresolved at the binary-specification level.

Current conservative interpretation:

* normal numeric encoding → numeric
* text encoding → text
* `0x12` with NaN-like payload → `missing_nan_candidate`
* `0x12` with zero payload → `empty_or_placeholder_candidate`
* unknown encoding → unsupported or ambiguous

The parser must not treat every `0x12` cell as missing.

The distinction between candidate states is preserved in JSON provenance. CSV may represent missing-like or ambiguous states as blank because CSV cannot preserve the full semantic distinction.

## Compatibility boundary

Validation currently spans fixtures from multiple SigmaPlot generations, including legacy SigmaPlot 7 and later serialization variants.

The release remains bounded to worksheet record families that have evidence. Unsupported JNB content should fail closed or be reported conservatively instead of being guessed.

## Output authority

CSV is intended for interoperable tabular recovery.

`recovery_manifest.json` is the authoritative output for provenance, raw cell information, warnings, and ambiguous scientific states.

## Current excluded scope

The project does not currently aim to:

* write or modify JNB files
* reproduce SigmaPlot as an application
* fully render graphs
* execute macros
* rebuild full statistical reports
* recover every embedded object type
* claim a complete specification of the JNB format

## Read-only boundary

The recovery workflow reads source JNB files and writes output to a separate recovery directory. A failed recovery must not modify the source JNB.

## Scientific change control

The recovery parser for an accepted release is frozen. Parser logic or scientific cell semantics should change only when new fixture evidence demonstrates an error, proves a new encoding, or establishes a previously unresolved semantic state.
