# JNB Recover 0.5.2 发布说明

[English](RELEASE_NOTES_0_5_2.md) | **简体中文**

这是用于本地、离线恢复 SigmaPlot JNB 工作表数据的首个已验收公开 MVP。

## 主要内容

* 面向 Pyto 的单文件 iPhone 和 iPad 工作流
* 本地、只读恢复
* iOS 原生 Files 文件选择器
* CSV 工作表导出
* JSON provenance manifest
* 冻结恢复引擎 0.3.0，并在运行时验证完整性
* 对科学语义 ambiguous 的单元格保守给出警告
* 对损坏输入 fail closed

## 真实设备验证

正常 SigmaPlot 13 JNB 恢复了 8 个工作表并生成 9 个输出文件。

Legacy SigmaPlot 7 `Samples.jnb` 恢复了 13 个工作表，并保守报告 524 个 ambiguous 单元格，结果为 `RECOVERED WITH SCIENTIFIC WARNING`。

一个人为构造的损坏 JNB 被识别为无效 OLE Compound Document 并拒绝恢复，源文件保持未修改。

取消 iOS 文件选择器返回 `CANCELLED`。

## 完整性

已验收脚本 SHA 256：

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

内嵌引擎 SHA 256：

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

## 科学边界

Ambiguous 或 unsupported 的单元格编码会被保守保存。项目不声称已经获得完整 JNB 格式规范。详细边界见 `docs/SCIENTIFIC_LIMITS.md` 和 `docs/VALIDATION.md`，对应中文版本见 `docs/SCIENTIFIC_LIMITS.zh-CN.md` 和 `docs/VALIDATION.zh-CN.md`。