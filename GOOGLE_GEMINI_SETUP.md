# Google Gemini 模型配置指南

## 📋 概述

已为 OpenClaw 添加 Google Gemini 3 Pro 模型支持，配置到以下 Agent：
- ✅ main (乙维斯)
- ✅ dev (DevBot)

## 🔧 配置位置

配置文件位于：
- `/root/.openclaw/agents/main/agent/models.json`
- `/root/.openclaw/agents/dev/agent/models.json`

## 📝 配置详情

```json
{
  "providers": {
    "google": {
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
      "apiKey": "YOUR_GOOGLE_API_KEY_HERE",
      "api": "openai-compatible",
      "models": [
        {
          "id": "gemini-3-pro",
          "name": "Gemini 3 Pro",
          "reasoning": false,
          "input": ["text", "image"],
          "contextWindow": 2097152,
          "maxTokens": 65536
        }
      ]
    }
  }
}
```

## 🚀 获取 API Key

### 步骤 1: 访问 Google AI Studio
前往：https://aistudio.google.com/app/apikey

### 步骤 2: 创建 API Key
1. 登录 Google 账号
2. 点击 "Create API Key"
3. 选择项目或创建新项目
4. 复制生成的 API Key

### 步骤 3: 替换配置
编辑配置文件，将 `YOUR_GOOGLE_API_KEY_HERE` 替换为你的实际 API Key：

```bash
# 编辑 main agent 配置
nano /root/.openclaw/agents/main/agent/models.json

# 编辑 dev agent 配置
nano /root/.openclaw/agents/dev/agent/models.json
```

找到这一行：
```json
"apiKey": "YOUR_GOOGLE_API_KEY_HERE"
```

替换为：
```json
"apiKey": "你的实际 API Key"
```

## ✅ 验证配置

配置完成后，可以通过以下方式验证：

```bash
# 检查配置文件
cat /root/.openclaw/agents/main/agent/models.json | grep -A 5 "google"
```

## 📊 模型特性

### Gemini 3 Pro
- **上下文窗口**: 2M tokens（约 150 万汉字）
- **最大输出**: 65,536 tokens
- **多模态支持**: 文本 + 图像
- **适用场景**: 
  - 长文档分析
  - 代码审查
  - 图像理解
  - 复杂推理任务

## ⚠️ 注意事项

1. **API Key 安全**: 
   - 不要将 API Key 提交到 Git 仓库
   - 不要在不安全的地方分享
   - 定期轮换密钥

2. **费用**: 
   - Gemini API 可能有使用费用
   - 查看 Google AI 定价页面：https://ai.google.dev/pricing

3. **速率限制**: 
   - 免费版本有每分钟请求数限制
   - 付费版本有更高的配额

## 🔄 使用方式

配置完成后，在对话中可以使用：
- `使用 gemini-3-pro 模型`
- `切换到 gemini 模型`

或者在 Agent 配置中设置为默认模型。

---

**配置时间**: 2026-03-04  
**配置者**: Winston
