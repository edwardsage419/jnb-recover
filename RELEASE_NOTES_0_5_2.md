# JNB Recover 0.5.2

**English** | [简体中文](RELEASE_NOTES_0_5_2.zh-CN.md)

First accepted public MVP for local, offline SigmaPlot JNB worksheet-data recovery.

## Highlights

* Single-file iPhone and iPad workflow for Pyto
* Local and read-only recovery
* Native iOS Files picker
* CSV worksheet export
* JSON provenance manifest
* Frozen recovery engine 0.3.0 with runtime integrity verification
* Conservative warning state for scientifically ambiguous cells
* Fail-closed handling for corrupted input

## Real-device validation

Normal SigmaPlot 13 JNB recovered 8 worksheets and produced 9 output files.

Legacy SigmaPlot 7 `Samples.jnb` recovered 13 worksheets and conservatively reported 524 ambiguous cells with `RECOVERED WITH SCIENTIFIC WARNING`.

A deliberately corrupted JNB was rejected as an invalid OLE Compound Document and the source file remained unchanged.

Cancelling the iOS picker returned `CANCELLED`.

## Integrity

Accepted script SHA 256:

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

Embedded engine SHA 256:

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

## Scientific boundary

Ambiguous or unsupported cell encodings are preserved conservatively. The project does not claim a complete specification of the JNB format. See `docs/SCIENTIFIC_LIMITS.md` and `docs/VALIDATION.md`.
