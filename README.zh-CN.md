# JNB Recover

[English](README.md) | 简体中文

[![Release](https://img.shields.io/github/v/release/edwardsage419/jnb-recover?label=release)](https://github.com/edwardsage419/jnb-recover/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: iPhone/iPad](https://img.shields.io/badge/platform-iPhone%20%7C%20iPad-lightgrey)](#iphone-和-ipad-使用方法)

无需安装 SigmaPlot，即可从 SigmaPlot `.JNB` 文件中恢复科研工作表数据。

JNB Recover 是一个本地、离线、只读的科研数据恢复和互操作工具，重点从专有 SigmaPlot notebook 文件中提取工作表数据，并导出为 CSV 和 JSON 等开放格式。

适用场景包括恢复历史实验数据、迁移归档 SigmaPlot 工作表、审计旧科研 notebook，以及将可恢复的工作表内容转换为开放表格格式。

## 当前版本

**MVP 0.5.2** · [下载最新 Release](https://github.com/edwardsage419/jnb-recover/releases/latest)

当前 iPhone 和 iPad 工作流使用一个适配 Pyto 的单文件 Python 脚本。脚本调用 iOS 原生 Files 文件选择器，在本机执行恢复，并为每个工作表写出一个 CSV，同时生成 `recovery_manifest.json`。

内嵌恢复引擎冻结于 0.3.0。

引擎 SHA 256：

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

已经在真实 iPhone 上验证正常恢复、科学警告恢复、损坏输入拒绝和用户取消四条路径。

## 科学范围

优先支持数值工作表、文本单元格、列名、行列结构、类似缺失值的状态以及 provenance 信息。

对于尚未被独立证据证明的单元格编码，项目保留其不确定性。未知单元格不会被静默猜测为数值或文本。

当前保守解释包括：

* 普通数值编码 → numeric
* 文本编码 → text
* `0x12` 加 NaN 类 payload → `missing_nan_candidate`
* `0x12` 加零 payload → `empty_or_placeholder_candidate`
* 未知编码 → unsupported 或 ambiguous

CSV 用于开放表格数据交换。`recovery_manifest.json` 是 provenance、警告以及科学歧义状态的权威输出。

## 验证摘要

当前证据覆盖多个 SigmaPlot 世代的公开或独立可验证 fixture。

* SigmaPlot 11 corpus：独立比较 56,360 个数值单元格，数值不一致为 0
* SigmaPlot 11 structural blanks：独立比较 13,002 个结构空白，missing mask 不一致为 0
* SigmaPlot 13 独立 JNB 与 XLSX：恢复并独立比对 294 个数值，最大浮点差约 `5.33e-15`
* SigmaPlot 14：12 个测试 JNB 全部恢复，870 个数值单元格和 10 个文本或 group 单元格与源 XLSX 交叉验证
* SigmaPlot 7 legacy `Samples.jnb`：真实 iPhone 上恢复 13 个工作表，并保守报告 524 个 ambiguous cells

详细证据和边界见 [`docs/VALIDATION.zh-CN.md`](docs/VALIDATION.zh-CN.md) 和 [`docs/SCIENTIFIC_LIMITS.zh-CN.md`](docs/SCIENTIFIC_LIMITS.zh-CN.md)。英文原文见 [`docs/VALIDATION.md`](docs/VALIDATION.md) 和 [`docs/SCIENTIFIC_LIMITS.md`](docs/SCIENTIFIC_LIMITS.md)。

## iPhone 和 iPad 使用方法

1. 在 iPhone 或 iPad 安装 Pyto。
2. 从 [最新 GitHub Release](https://github.com/edwardsage419/jnb-recover/releases/latest) 下载 `JNB_Recover_iPhone_0_5_2.py`。
3. 在 Pyto 中打开该文件。
4. 运行脚本。
5. 在 iOS Files 文件选择器中选择 `.JNB` 文件。
6. 工具会在 Pyto Documents 下创建不会覆盖旧结果的恢复目录。

可能的结果状态包括 `RECOVERED`、`RECOVERED WITH SCIENTIFIC WARNING`、`FAILED` 和 `CANCELLED`。

## 兼容性反馈

如果某个 JNB 失败、出现意外科学警告，或疑似恢复错误，请提交 [Compatibility Report](https://github.com/edwardsage419/jnb-recover/issues/new?template=compatibility-report.md)。独立 CSV 或 XLSX ground truth 尤其有价值。

请勿上传机密、专有、个人或受限制的 JNB 文件。优先使用最小化 synthetic fixture 或明确允许公开再分发的 fixture。

一般使用帮助见 [`SUPPORT.md`](SUPPORT.md)。

## 产品边界

当前项目不写入 JNB，不复刻 SigmaPlot，不完整渲染图形，不执行宏，不重建完整统计报告，也不声称掌握完整 JNB 文件格式规范。

## 隐私和依赖

恢复过程在本机离线完成。恢复本身不需要服务器、付费 API、SigmaPlot、Origin 或云端 AI 服务。

## 项目资料

软件引用元数据见 [`CITATION.cff`](CITATION.cff)。贡献规则见 [`CONTRIBUTING.md`](CONTRIBUTING.md)，安全说明见 [`SECURITY.md`](SECURITY.md)，项目独立性与商标说明见 [`TRADEMARKS.md`](TRADEMARKS.md)，用户支持说明见 [`SUPPORT.md`](SUPPORT.md)，仓库设置建议见 [`docs/REPOSITORY_SETUP.md`](docs/REPOSITORY_SETUP.md)。

## 状态

MVP 0.5.2 是当前已验收版本。除非新 fixture 证据证明具体错误或新的未支持序列化变体，否则解析器语义保持冻结。

## 许可证

正式许可证以英文 [`LICENSE`](LICENSE) 为准。中文阅读参考见 [`LICENSE.zh-CN.md`](LICENSE.zh-CN.md)。
