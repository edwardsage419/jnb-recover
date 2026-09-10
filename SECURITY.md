# Security Policy

## English

### Supported version

The currently supported public release is JNB Recover 0.5.2.

### Reporting a security issue

Do not publish sensitive exploit details, confidential JNB files, personal data, credentials, or proprietary scientific data in a public issue.

For ordinary compatibility or recovery problems that do not contain sensitive information, use the JNB compatibility issue template.

If a report requires sensitive material, do not attach that material to a public GitHub issue. Provide a minimal synthetic reproduction when possible.

### Security model

JNB Recover is designed for local, offline, read-only recovery. The accepted 0.5.2 release does not require a server, paid API, cloud AI service, SigmaPlot, or Origin for recovery.

The source JNB is intended to remain unmodified. Output is written separately as recovered CSV files and a JSON provenance manifest.

### Scientific integrity

A scientifically incorrect silent interpretation is treated as a serious defect. Unknown or insufficiently proven encodings must remain unsupported or ambiguous until evidence supports a specific interpretation.

### Scope

Security reports should concern JNB Recover itself. Pyto, iOS, GitHub, SigmaPlot, and other third-party software have their own security and support channels.

---

## 简体中文

### 支持版本

当前支持的公开版本为 JNB Recover 0.5.2。

### 报告安全问题

请勿在公开 Issue 中发布敏感漏洞细节、机密 JNB 文件、个人数据、凭据或专有科研数据。

普通兼容性或恢复问题如果不含敏感信息，请使用 JNB Compatibility Report 模板。

如果报告必须涉及敏感材料，请不要把该材料附加到公开 GitHub Issue。应尽可能提供最小 synthetic reproduction。

### 安全模型

JNB Recover 设计为本地、离线、只读恢复工具。已验收的 0.5.2 版本在恢复过程中不需要服务器、付费 API、云端 AI、SigmaPlot 或 Origin。

源 JNB 设计上保持不变。恢复结果单独写出为 CSV 和 JSON provenance manifest。

### 科学完整性

对科研数据进行错误的静默解释应视为严重缺陷。在证据支持具体解释之前，未知或证据不足的编码必须保持 unsupported 或 ambiguous。

### 范围

安全报告应针对 JNB Recover 本身。Pyto、iOS、GitHub、SigmaPlot 和其他第三方软件应使用各自的安全与支持渠道。
