# Usage Guide

[English](USAGE.md) | [简体中文](USAGE.zh-CN.md)

## Requirements

The accepted mobile workflow uses an iPhone or iPad with Pyto installed. Recovery itself is local and offline.

Use the current accepted release unless you are intentionally testing another version.

## Download

Download `JNB_Recover_iPhone_0_5_2.py` from the latest GitHub Release.

For integrity-sensitive work, compare the downloaded file against `SHA256SUMS.txt`.

Accepted script SHA 256:

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

## Run on iPhone or iPad

1. Open the downloaded Python file in Pyto.
2. Run the script.
3. Choose a `.JNB` file in the iOS Files picker.
4. Wait for the recovery result.
5. Open the generated recovery directory under Pyto Documents.

The tool creates a new output directory and does not intentionally overwrite an earlier recovery directory.

## Outputs

A successful recovery writes one CSV per recovered worksheet plus `recovery_manifest.json`.

CSV is intended for ordinary tabular access and migration.

`recovery_manifest.json` is authoritative for provenance, warnings, raw cell information, and ambiguous scientific states.

## Result states

`RECOVERED` means the supported recovery path completed without reported ambiguous cells.

`RECOVERED WITH SCIENTIFIC WARNING` means recovery completed while one or more cells remain scientifically ambiguous or unsupported. Review `recovery_manifest.json` before scientific reuse.

`FAILED` means the input was rejected or recovery could not complete. The source JNB is intended to remain unchanged.

`CANCELLED` means the file picker was closed without selecting a file.

## Scientific use

Do not interpret an absence of warnings as proof that every semantic detail of every JNB generation is fully specified.

The project deliberately preserves uncertainty when the available evidence does not justify a specific interpretation.

Read `SCIENTIFIC_LIMITS.md` before using recovered data in scientific analysis, archival migration, or publication workflows.

## Reporting a problem

Use the Compatibility Report template for version-specific or file-specific recovery behavior.

Use the Bug Report template for reproducible software defects.

Do not upload confidential, proprietary, personal, or restricted JNB files. Prefer a minimal synthetic or publicly redistributable fixture.