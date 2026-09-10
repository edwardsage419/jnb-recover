# 使用指南

[English](USAGE.md) | [简体中文](USAGE.zh-CN.md)

## 使用条件

当前已验收的移动端工作流使用安装了 Pyto 的 iPhone 或 iPad。恢复过程本身在本机离线完成。

除非你有意测试其他版本，否则应优先使用当前已验收 Release。

## 下载

从最新 GitHub Release 下载 `JNB_Recover_iPhone_0_5_2.py`。

如果工作流程对完整性要求较高，可以使用 `SHA256SUMS.txt` 校验下载文件。

已验收脚本 SHA 256：

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

## 在 iPhone 或 iPad 上运行

1. 在 Pyto 中打开下载的 Python 文件。
2. 运行脚本。
3. 在 iOS Files 文件选择器中选择 `.JNB` 文件。
4. 等待恢复结果。
5. 在 Pyto Documents 下打开生成的恢复目录。

工具会创建新的输出目录，设计上不会覆盖之前的恢复目录。

## 输出文件

恢复成功后，每个已恢复工作表会生成一个 CSV，同时生成 `recovery_manifest.json`。

CSV 主要用于普通表格访问和数据迁移。

`recovery_manifest.json` 是 provenance、警告、原始单元格信息和科学歧义状态的权威输出。

## 结果状态

`RECOVERED` 表示受支持的恢复路径已经完成，并且没有报告 ambiguous cells。

`RECOVERED WITH SCIENTIFIC WARNING` 表示恢复已经完成，但一个或多个单元格仍存在科学语义歧义或未支持状态。在科研复用前应检查 `recovery_manifest.json`。

`FAILED` 表示输入被拒绝，或恢复无法完成。源 JNB 设计上应保持不变。

`CANCELLED` 表示用户关闭文件选择器且没有选择文件。

## 科研使用注意事项

没有警告并不等于已经完整证明所有 JNB 世代的每一个语义细节。

当现有证据不足以支持具体解释时，本项目会有意保留不确定性。

在把恢复数据用于科研分析、档案迁移或论文工作流之前，请阅读 `SCIENTIFIC_LIMITS.zh-CN.md`。

## 报告问题

如果问题与特定 SigmaPlot 版本或特定 JNB 文件兼容性有关，请使用 Compatibility Report 模板。

如果是可复现的软件缺陷，请使用 Bug Report 模板。

请勿上传机密、专有、个人或受限制的 JNB 文件。优先提供最小 synthetic fixture 或明确允许公开再分发的 fixture。