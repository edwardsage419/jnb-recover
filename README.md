# JNB Recover

Recover scientific worksheet data from SigmaPlot `.JNB` files without SigmaPlot.

JNB Recover is a local, offline, read-only recovery tool focused on extracting scientific worksheet data trapped in proprietary SigmaPlot notebook files and exporting it to open formats such as CSV and JSON.

## Current release

MVP 0.5.2

The current iPhone workflow is a single Python file designed for Pyto. It uses the native iOS Files picker, performs recovery locally, and writes one CSV per recovered worksheet plus `recovery_manifest.json`.

The embedded recovery engine is frozen at version 0.3.0.

Engine SHA 256:

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

Validated iPhone result paths include normal recovery, scientific warning recovery, corrupted input rejection, and user cancellation.

## Scientific scope

Priority support covers numeric worksheet values, text cells, column names, row and column structure, missing-like states, and provenance.

The project intentionally preserves uncertainty around cell encodings that are not independently proven. Unknown cells are never silently guessed as numeric or text.

Current conservative interpretation includes:

* normal numeric encoding → numeric
* text encoding → text
* `0x12` with NaN-like payload → `missing_nan_candidate`
* `0x12` with zero payload → `empty_or_placeholder_candidate`
* unknown encoding → unsupported or ambiguous

CSV is intended for interoperable tabular recovery. `recovery_manifest.json` is the authoritative place for provenance and ambiguous scientific states.

## Validation summary

Current evidence includes independent comparison across public SigmaPlot fixtures from multiple generations.

* SigmaPlot 11 corpus: 56,360 numeric cells independently compared with 0 numeric mismatch
* SigmaPlot 11 structural blanks: 13,002 compared with 0 missing-mask mismatch
* SigmaPlot 13 independent JNB plus XLSX: 294 numeric values recovered with maximum floating difference approximately `5.33e-15`
* SigmaPlot 14: 12 of 12 tested JNB files recovered, with 870 numeric and 10 text or group cells independently cross-checked
* SigmaPlot 7 legacy `Samples.jnb`: recovered on a real iPhone with 13 worksheets and 524 ambiguous cells conservatively reported as a scientific warning

See `docs/VALIDATION.md` and `docs/SCIENTIFIC_LIMITS.md` for the frozen evidence and boundaries.

## iPhone use

1. Install Pyto on the iPhone or iPad.
2. Open `JNB_Recover_iPhone_0_5_2.py` in Pyto.
3. Run the script.
4. Select a `.JNB` file in the iOS Files picker.
5. The tool writes a non-overwriting recovery folder under Pyto Documents.

Possible result states are `RECOVERED`, `RECOVERED WITH SCIENTIFIC WARNING`, `FAILED`, and `CANCELLED`.

## Product boundaries

This project currently does not write JNB files, clone SigmaPlot, render complete graphs, execute macros, rebuild complete statistical reports, or claim a complete JNB file-format specification.

## Privacy and dependencies

Recovery is local and offline. No server, paid API, SigmaPlot installation, Origin installation, or cloud AI service is required for recovery.

## Status

MVP 0.5.2 is the accepted current release. Parser semantics are frozen until new fixture evidence demonstrates a specific error or unsupported serialization variant.

## License

MIT License. See `LICENSE`.
