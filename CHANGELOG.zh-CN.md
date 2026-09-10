# 更新记录

[English](CHANGELOG.md) | **简体中文**

## 0.5.2 · 2026-09-10

已验收的 iPhone MVP 正式版本。

### 包含内容

* 面向 iPhone 和 iPad 的单文件 Pyto 工作流
* 使用明确 `.jnb` 扩展名筛选的 iOS 原生 Files 文件选择器
* 冻结内嵌恢复引擎 0.3.0
* 运行时 SHA 256 引擎完整性验证
* CSV 工作表导出和 JSON recovery manifest
* 对 ambiguous 单元格给出保守科学警告
* 不覆盖既有结果的恢复目录
* 只读源文件工作流

### 真实设备验收

* 正常 SigmaPlot 13 JNB：PASS
* SigmaPlot 7 legacy JNB：PASS
* 科学警告路径：PASS，包括 `Samples.jnb` 中 524 个 ambiguous 单元格
* 损坏 JNB fail closed 路径：PASS
* 用户取消路径：PASS

已验收 artifact SHA 256：

`d4634214d80fcaf73cc3f901a62e6eb059d86734b9450370f916ec562ca2880c`

内嵌引擎 SHA 256：

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`