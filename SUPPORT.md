# Support

## English

### Before opening an issue

Use the latest accepted release and read the scientific limits first. JNB Recover intentionally reports uncertainty instead of guessing unsupported cell semantics.

For an ordinary usage problem, include the JNB Recover version, device or platform, observed result state, and the exact error text when available.

For a compatibility problem, use the dedicated compatibility report template. Independent CSV or XLSX ground truth is especially useful.

Do not upload confidential, proprietary, personal, or restricted JNB files. If a file cannot be shared publicly, provide a minimal synthetic reproduction or a description of the expected worksheet structure.

For security-sensitive reports, follow `SECURITY.md` and do not publish sensitive exploit details or private scientific data in a public issue.

### Result states

`RECOVERED` means the supported recovery path completed without reported ambiguous cells.

`RECOVERED WITH SCIENTIFIC WARNING` means data was recovered but one or more cells have scientifically ambiguous or unsupported semantics. Review `recovery_manifest.json` before scientific reuse.

`FAILED` means the tool rejected or could not recover the input. The source JNB is intended to remain unchanged.

`CANCELLED` means the user exited the file picker without selecting a file.

---

## 简体中文

### 提交 Issue 前

请优先使用最新已验收 Release，并先阅读科学边界说明。JNB Recover 会保留未证明语义的不确定性，不会为了给出结果而猜测未知单元格含义。

对于普通使用问题，请提供 JNB Recover 版本、设备或平台、观察到的结果状态，以及可获得的完整错误文本。

对于兼容性问题，请使用专门的 Compatibility Report 模板。能够独立验证的 CSV 或 XLSX ground truth 尤其有价值。

请勿上传机密、专有、个人或受限制的 JNB 文件。如果文件不能公开共享，请提供最小 synthetic reproduction，或描述预期的工作表结构。

涉及安全敏感信息时，请遵循 `SECURITY.md`，不要在公开 Issue 中发布敏感漏洞细节或私人科研数据。

### 结果状态

`RECOVERED` 表示受支持的恢复路径已经完成，并且没有报告 ambiguous cells。

`RECOVERED WITH SCIENTIFIC WARNING` 表示已经恢复数据，但存在一个或多个科学语义仍不明确或未支持的单元格。在科研复用前应检查 `recovery_manifest.json`。

`FAILED` 表示工具拒绝该输入或无法完成恢复。源 JNB 设计上应保持不变。

`CANCELLED` 表示用户在没有选择文件的情况下退出文件选择器。
