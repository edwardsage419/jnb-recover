# Security Policy

## Supported version

The currently supported public release is JNB Recover 0.5.2.

## Reporting a security issue

Do not publish sensitive exploit details, confidential JNB files, personal data, credentials, or proprietary scientific data in a public issue.

For ordinary compatibility or recovery problems that do not contain sensitive information, use the JNB compatibility issue template.

If a report requires sensitive material, do not attach that material to a public GitHub issue. Provide a minimal synthetic reproduction when possible.

## Security model

JNB Recover is designed for local, offline, read-only recovery. The accepted 0.5.2 release does not require a server, paid API, cloud AI service, SigmaPlot, or Origin for recovery.

The source JNB is intended to remain unmodified. Output is written separately as recovered CSV files and a JSON provenance manifest.

## Scientific integrity

A scientifically incorrect silent interpretation is treated as a serious defect. Unknown or insufficiently proven encodings must remain unsupported or ambiguous until evidence supports a specific interpretation.

## Scope

Security reports should concern JNB Recover itself. Pyto, iOS, GitHub, SigmaPlot, and other third-party software have their own security and support channels.