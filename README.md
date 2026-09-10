# JNB Recover

English | [简体中文](README.zh-CN.md)

[![Integrity CI](https://github.com/edwardsage419/jnb-recover/actions/workflows/ci.yml/badge.svg)](https://github.com/edwardsage419/jnb-recover/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/edwardsage419/jnb-recover?label=release)](https://github.com/edwardsage419/jnb-recover/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: iPhone/iPad](https://img.shields.io/badge/platform-iPhone%20%7C%20iPad-lightgrey)](#iphone-use)

Recover scientific worksheet data from SigmaPlot `.JNB` files without SigmaPlot.

JNB Recover is a local, offline, read-only scientific data recovery and interoperability tool focused on extracting worksheet data trapped in proprietary SigmaPlot notebook files and exporting it to open formats such as CSV and JSON.

Use cases include recovering legacy experimental data, migrating archived SigmaPlot worksheets, auditing old scientific notebooks, and converting accessible worksheet content into open tabular formats.

## Current release

**MVP 0.5.2** · [Direct download](https://github.com/edwardsage419/jnb-recover/releases/download/v0.5.2/JNB_Recover_iPhone_0_5_2.py) · [Release notes](https://github.com/edwardsage419/jnb-recover/releases/tag/v0.5.2)

Accepted script SHA 256:

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

The current iPhone and iPad workflow is a single Python file designed for Pyto. It uses the native iOS Files picker, performs recovery locally, and writes one CSV per recovered worksheet plus `recovery_manifest.json`.

The embedded recovery engine is frozen at version 0.3.0.

Engine SHA 256:

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

Validated iPhone result paths include normal recovery, scientific warning recovery, corrupted input rejection, and user cancellation.

## Quick documentation

* [Usage guide](docs/USAGE.md) · [简体中文](docs/USAGE.zh-CN.md)
* [Troubleshooting](docs/TROUBLESHOOTING.md) · [简体中文](docs/TROUBLESHOOTING.zh-CN.md)
* [Validation record](docs/VALIDATION.md) · [简体中文](docs/VALIDATION.zh-CN.md)
* [Scientific limits](docs/SCIENTIFIC_LIMITS.md) · [简体中文](docs/SCIENTIFIC_LIMITS.zh-CN.md)

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

See [`docs/VALIDATION.md`](docs/VALIDATION.md) and [`docs/SCIENTIFIC_LIMITS.md`](docs/SCIENTIFIC_LIMITS.md) for the frozen evidence and boundaries.

## iPhone use

1. Install Pyto on the iPhone or iPad.
2. Download [`JNB_Recover_iPhone_0_5_2.py`](https://github.com/edwardsage419/jnb-recover/releases/download/v0.5.2/JNB_Recover_iPhone_0_5_2.py).
3. Open the file in Pyto.
4. Run the script.
5. Select a `.JNB` file in the iOS Files picker.
6. The tool writes a non-overwriting recovery folder under Pyto Documents.

Possible result states are `RECOVERED`, `RECOVERED WITH SCIENTIFIC WARNING`, `FAILED`, and `CANCELLED`.

For detailed steps, see [`docs/USAGE.md`](docs/USAGE.md). For common problems, see [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

## Compatibility reports

If a JNB fails, warns unexpectedly, or appears to recover incorrectly, [open a compatibility report](https://github.com/edwardsage419/jnb-recover/issues/new?template=compatibility-report.md). Independent CSV or XLSX ground truth is especially valuable.

Do not upload confidential, proprietary, personal, or restricted JNB files. A minimal synthetic or publicly redistributable fixture is preferred.

For general help, see [`SUPPORT.md`](SUPPORT.md).

## Product boundaries

This project currently does not write JNB files, clone SigmaPlot, render complete graphs, execute macros, rebuild complete statistical reports, or claim a complete JNB file-format specification.

## Privacy and dependencies

Recovery is local and offline. No server, paid API, SigmaPlot installation, Origin installation, or cloud AI service is required for recovery.

## Project metadata

Software citation metadata is available in [`CITATION.cff`](CITATION.cff). Contribution rules are in [`CONTRIBUTING.md`](CONTRIBUTING.md), security guidance in [`SECURITY.md`](SECURITY.md), project independence and trademark guidance in [`TRADEMARKS.md`](TRADEMARKS.md), repository setup guidance in [`docs/REPOSITORY_SETUP.md`](docs/REPOSITORY_SETUP.md), and discoverability guidance in [`docs/DISCOVERABILITY.md`](docs/DISCOVERABILITY.md).

## Status

MVP 0.5.2 is the accepted current release. Parser semantics are frozen until new fixture evidence demonstrates a specific error or unsupported serialization variant.

## License

MIT License. See the authoritative English [`LICENSE`](LICENSE). An unofficial Simplified Chinese reference translation is available in [`LICENSE.zh-CN.md`](LICENSE.zh-CN.md).
