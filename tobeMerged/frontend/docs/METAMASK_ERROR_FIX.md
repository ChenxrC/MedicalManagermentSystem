# MetaMask 扩展错误处理指南

## 问题描述

您可能在浏览器控制台看到以下错误：

```
Uncaught runtime errors:
×
ERROR
Failed to connect to MetaMask
s: Failed to connect to MetaMask
    at Object.connect (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/scripts/inpage.js:1:21493)
    at async o (chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/scripts/inpage.js:1:19297
```

## 原因分析

这个错误**不是由应用本身引起的**，而是由MetaMask浏览器扩展导致的。MetaMask是一个加密货币钱包扩展，它会在浏览器中注入JavaScript代码，有时可能会与网页应用发生冲突。

重要说明：
- 应用代码中**没有**集成任何区块链或加密货币相关功能
- 错误来自MetaMask扩展自身的脚本，而不是应用代码
- 这个错误通常不会影响应用的核心功能

## 我们的解决方案

我们已经在应用中添加了以下改进：

1. **增强的错误处理**：在`main.js`中添加了全局错误捕获，专门处理MetaMask相关错误
2. **浏览器环境检测**：在`debug.js`中添加了工具函数，用于记录和分析浏览器环境
3. **自动恢复机制**：当检测到MetaMask错误时，应用会尝试重新初始化
4. **简化日志输出**：移除了可能干扰调试的过多日志信息

## 用户解决方法

如果您遇到这个问题，可以尝试以下解决方案：

### 方法1：禁用MetaMask扩展

1. 在浏览器中打开扩展管理页面
2. 找到MetaMask扩展并暂时禁用它
3. 刷新应用页面

### 方法2：更新MetaMask扩展

1. 确保您的MetaMask扩展是最新版本
2. 有时旧版本的MetaMask可能会导致兼容性问题

### 方法3：使用隐私模式

1. 在浏览器的隐私/隐身模式下打开应用
2. 默认情况下，隐私模式不会加载已安装的扩展

### 方法4：使用其他浏览器

尝试使用未安装MetaMask扩展的浏览器访问应用

## 技术细节

我们添加的代码包括：

1. `src/utils/debug.js`中的`handleExtensionErrors`函数 - 专门检测和处理MetaMask错误
2. `src/utils/debug.js`中的`logBrowserEnvironment`函数 - 记录浏览器环境信息
3. `src/main.js`中的全局错误处理和自动恢复机制

这些改进不会影响应用的正常功能，只是增强了对浏览器扩展冲突的处理能力。

## 联系支持

如果问题持续存在，请联系技术支持并提供：
- 浏览器类型和版本
- MetaMask扩展版本
- 完整的错误日志