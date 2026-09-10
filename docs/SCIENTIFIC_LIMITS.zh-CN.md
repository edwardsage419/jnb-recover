# 科学与产品边界

[English](SCIENTIFIC_LIMITS.md) | **简体中文**

## 缺失值语义

部分 SigmaPlot 单元格状态在二进制规范层面仍有意保持未解决状态。

当前保守解释：

* 普通数值编码 → `numeric`
* 文本编码 → `text`
* `0x12` 加 NaN 类 payload → `missing_nan_candidate`
* `0x12` 加零 payload → `empty_or_placeholder_candidate`
* 未知编码 → `unsupported` 或 ambiguous

解析器不得把所有 `0x12` 单元格都解释为 missing。

候选状态之间的区别保存在 JSON provenance 中。CSV 可能把 missing 类或 ambiguous 状态表示为空白，因为 CSV 无法保留完整语义差异。

## 兼容性边界

当前验证覆盖多个 SigmaPlot 世代的 fixture，包括 SigmaPlot 7 legacy 和较新的序列化变体。

正式版本的支持范围限定于已有证据的工作表记录家族。对于未支持的 JNB 内容，应 fail closed 或保守报告，不得猜测。

## 输出权威性

CSV 用于可互操作的表格恢复。

`recovery_manifest.json` 是 provenance、原始单元格信息、警告和 ambiguous 科学状态的权威输出。

## 当前排除范围

当前项目不以以下能力为目标：

* 写入或修改 JNB 文件
* 复刻 SigmaPlot 应用程序
* 完整渲染图形
* 执行宏
* 重建完整统计报告
* 恢复所有嵌入对象类型
* 声称掌握完整 JNB 文件格式规范

## 只读边界

恢复工作流读取源 JNB，并把输出写入独立恢复目录。恢复失败不得修改源 JNB。

## 科学修改控制

已验收版本的恢复解析器保持冻结。只有当新的 fixture 证据证明现有行为错误、证明新的编码，或建立此前未解决状态的具体语义时，才应修改解析器逻辑或科学单元格语义。