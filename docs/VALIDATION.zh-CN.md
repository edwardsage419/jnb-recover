# 验证记录

当前已验收版本：MVP 0.5.2

恢复引擎：0.3.0

内嵌引擎 SHA 256：

`7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40`

## 科学验证基线

### SigmaPlot 11 公开 JNB 与 CSV corpus

独立比较 56,360 个数值单元格。

数值不一致数量：0

独立比较 13,002 个 CSV 结构空白。

Missing mask 不一致数量：0

### SigmaPlot 12 公开 fixture

基础工作表 record grammar、数值单元格和文本单元格已经得到独立验证。

### SigmaPlot 13 独立 JNB 与 XLSX

在源 XLSX 中独立定位并比较 294 个数值。

观察到的最大浮点差约为 `5.33e-15`。

### SigmaPlot 14 fixtures

解析器增加了一个有明确边界的新序列化变体支持。

测试的 12 个 JNB 全部恢复成功。

870 个数值单元格和 10 个文本或 group 单元格与源 XLSX 数据进行了独立交叉验证。

### SigmaPlot 7 legacy fixture

使用 Pyto 和已验收的单文件工作流，在真实 iPhone 上恢复了 `Samples.jnb`。

观察结果：

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 13
Files written: 14
RESULT: RECOVERED WITH SCIENTIFIC WARNING
Ambiguous cells: 524
```

这验证了 legacy 路径和保守的科学警告路径。

## 真实 iPhone 验收矩阵

### 正常 JNB

Fixture：`pone.0146623.s003.JNB`

观察结果：

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 8
Files written: 9
RESULT: RECOVERED
```

状态：PASS

### 科学警告

Fixture：SigmaPlot 7 `Samples.jnb`

观察结果：

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
Worksheets: 13
Files written: 14
RESULT: RECOVERED WITH SCIENTIFIC WARNING
Ambiguous cells: 524
```

状态：PASS

### 损坏输入

从一个有效 JNB 制作确定性损坏副本，将前 8 个 OLE/CFB magic bytes 替换为零字节。

观察结果：

```text
Recovery engine: 0.3.0
Engine integrity: VERIFIED
RESULT: FAILED
JNBError: file is not an OLE Compound Document
The source JNB was not modified.
```

状态：PASS

### 用户取消

打开 iOS Files 文件选择器后，在没有选择文件的情况下取消。

观察结果：

```text
RESULT: CANCELLED
```

状态：PASS

## Release 验收

MVP 0.5.2 已验收以下路径：

* iOS Files 文件选择器
* 显式 `.JNB` 扩展名选择
* 单文件 Pyto 部署
* 冻结引擎完整性验证
* 正常恢复
* 科学警告恢复
* 损坏输入拒绝
* 用户取消
* 源文件只读行为

MVP 0.5.2 状态：ACCEPTED
