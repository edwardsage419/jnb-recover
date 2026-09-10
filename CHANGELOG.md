# Changelog

## 0.5.2 — 2026-09-10

Accepted iPhone MVP release.

### Included

* Single-file Pyto workflow for iPhone and iPad
* Native iOS Files picker with explicit `.jnb` extension selection
* Frozen embedded recovery engine 0.3.0
* Runtime SHA 256 verification of the embedded engine
* CSV worksheet export and JSON recovery manifest
* Conservative scientific warning for ambiguous cells
* Non-overwriting recovery directories
* Read-only source workflow

### Real-device acceptance

* Normal SigmaPlot 13 JNB: PASS
* SigmaPlot 7 legacy JNB: PASS
* Scientific warning path: PASS, including 524 ambiguous cells in `Samples.jnb`
* Corrupted JNB fail-closed path: PASS
* User cancellation path: PASS

Accepted artifact SHA 256:

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

Embedded engine SHA 256:

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`
