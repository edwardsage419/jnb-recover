# 故障排查

[English](TROUBLESHOOTING.md) | [简体中文](TROUBLESHOOTING.zh-CN.md)

## iOS 文件选择器中的 JNB 文件是灰色的

请使用已验收的 `JNB_Recover_iPhone_0_5_2.py` Release。该版本会明确要求 Pyto 选择 `.jnb` 扩展名文件。

如果 JNB 仍然无法选择，请确认文件名确实以 `.jnb` 结尾，并且该文件能够通过 iOS Files 应用访问。

## 出现 RESULT: FAILED 和 “not an OLE Compound Document”

这表示输入文件没有被识别为 OLE Compound Document。可能原因包括文件损坏、其他文件被改名为 `.jnb`，或存在当前未支持的容器变体。

排查期间请不要修改原始文件。如果文件可以合法共享，请提交 Compatibility Report，并尽量提供最小复现或独立 ground truth。

## 出现 RESULT: RECOVERED WITH SCIENTIFIC WARNING

恢复已经完成，但一个或多个单元格状态仍然存在歧义或未支持语义。

请不要把这些单元格静默视为普通缺失值或普通数值。在科研复用前应检查 `recovery_manifest.json` 和科学边界说明。

## 出现 RESULT: CANCELLED

当用户关闭 iOS Files 文件选择器且没有选择文件时，这是预期结果。不会执行恢复。

## 找不到输出文件

已验收的 iPhone 工作流会在 Pyto Documents 下创建新的恢复目录。目录名以源文件名主体为基础，如果已存在同名目录，会自动增加后缀，避免覆盖旧结果。

## CSV 中有些单元格看起来是空白

CSV 无法保存所有科学歧义状态。类似缺失值或 ambiguous 的单元格在 CSV 中可能显示为空白。

请使用 `recovery_manifest.json` 检查保留的单元格类型、provenance、警告和原始信息。

## 我需要恢复图形、宏或完整统计报告

这些内容当前不属于已验收项目范围。JNB Recover 目前聚焦只读工作表数据恢复。

## 我发现了可能的恢复错误

不要基于单个尚未解释的现象直接修改解析器语义。请提交 Compatibility Report，并在可能时提供能够独立验证的预期数据。

优先提供公开、synthetic 或其他具备合法共享权利的 fixture。