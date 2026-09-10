# Troubleshooting

[English](TROUBLESHOOTING.md) | [简体中文](TROUBLESHOOTING.zh-CN.md)

## The JNB file is greyed out in the iOS picker

Use the accepted `JNB_Recover_iPhone_0_5_2.py` release. It explicitly asks Pyto to select files with the `.jnb` extension.

If a JNB is still not selectable, confirm that the file has the `.jnb` filename extension and is accessible through the iOS Files app.

## RESULT: FAILED and “not an OLE Compound Document”

The input is not being recognized as an OLE Compound Document. This can indicate a corrupted file, an unrelated file renamed to `.jnb`, or an unsupported container variant.

Do not modify the original file while investigating. If the file is legally shareable, submit a Compatibility Report with a minimal reproduction or independent ground truth.

## RESULT: RECOVERED WITH SCIENTIFIC WARNING

Recovery completed, while one or more cell states remain ambiguous or unsupported.

Do not silently treat those cells as ordinary missing values or ordinary numbers. Review `recovery_manifest.json` and the scientific limits before scientific reuse.

## RESULT: CANCELLED

This is expected when the iOS Files picker is closed without selecting a file. No recovery is performed.

## I cannot find the output

The accepted iPhone workflow writes a new recovery directory under Pyto Documents. The folder name is based on the source file stem, with a suffix added when needed to avoid overwriting an existing recovery directory.

## The CSV looks blank in some cells

CSV cannot preserve every ambiguous scientific state. Missing-like or ambiguous cells may appear blank in CSV.

Use `recovery_manifest.json` to inspect the preserved cell kind, provenance, warnings, and raw information.

## I need graphs, macros, or complete statistical reports

Those are outside the current accepted project scope. JNB Recover currently focuses on read-only worksheet-data recovery.

## I found a possible recovery error

Do not change parser semantics based on a single unexplained observation. Open a Compatibility Report and include independently verifiable expected data when possible.

A public, synthetic, or otherwise legally shareable fixture is preferred.