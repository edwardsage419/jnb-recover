# Validation Record

Current accepted release: MVP 0.5.2

Recovery engine: 0.3.0

Embedded engine SHA 256:

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

## Scientific validation baseline

### SigmaPlot 11 public JNB and CSV corpus

56,360 numeric cells were independently compared.

Numeric mismatch count: 0

13,002 structural CSV blanks were independently compared.

Missing-mask mismatch count: 0

### SigmaPlot 12 public fixture

The base worksheet record grammar, numeric cells, and text cells were independently demonstrated.

### SigmaPlot 13 independent JNB and XLSX

294 numeric values were independently located in the source XLSX.

Maximum observed floating difference was approximately `5.33e-15`.

### SigmaPlot 14 fixtures

A bounded newer serialization variant was added to the supported parser.

12 of 12 tested JNB files recovered.

870 numeric cells and 10 text or group cells were independently cross-checked against source XLSX data.

### SigmaPlot 7 legacy fixture

`Samples.jnb` was recovered on a real iPhone using Pyto and the accepted single-file workflow.

Observed result:

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 13
Files written: 14
RESULT: RECOVERED WITH SCIENTIFIC WARNING
Ambiguous cells: 524
```

This validates the legacy path and the conservative scientific-warning path.

## Real-device iPhone acceptance matrix

### Normal JNB

Fixture: `pone.0146623.s003.JNB`

Observed:

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 8
Files written: 9
RESULT: RECOVERED
```

Status: PASS

### Scientific warning

Fixture: SigmaPlot 7 `Samples.jnb`

Observed:

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 13
Files written: 14
RESULT: RECOVERED WITH SCIENTIFIC WARNING
Ambiguous cells: 524
```

Status: PASS

### Corrupted input

A deterministic corrupted copy of a valid JNB had its first eight OLE/CFB magic bytes replaced with zero bytes.

Observed:

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
RESULT: FAILED
JNBError: file is not an OLE Compound Document
The source JNB was not modified.
```

Status: PASS

### User cancellation

The iOS Files picker was opened and cancelled without choosing a file.

Observed:

```text
RESULT: CANCELLED
```

Status: PASS

## Release acceptance

The following paths are accepted for MVP 0.5.2:

* iOS Files picker
* explicit `.JNB` extension selection
* single-file Pyto deployment
* frozen engine integrity verification
* normal recovery
* scientific warning recovery
* corrupted input rejection
* user cancellation
* read-only source behavior

MVP 0.5.2 status: ACCEPTED
