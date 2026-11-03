# ChatGPT Plugin Adapter

本目录提供单一 AI 金融助手插件的 ChatGPT 包配置。统一 Agent 源配置位于 `agent/`，金融 Skills 位于 `skills/`，本适配层不复制或拆分业务能力。

## 映射

- `adapters/chatgpt/plugin.json` -> 插件根目录 `plugin.json`
- `adapters/chatgpt/agents/openai.yaml` -> 插件根目录 `agents/openai.yaml`
- `skills/*/SKILL.md` -> 插件根目录 `skills/*/SKILL.md`
- `agent/manifest.yaml`、`agent/instructions.md`、`config/`、`policies/` 和 `references/` -> 主控 Skill 的 references
- `templates/` -> 主控 Skill 的 assets/templates

## 构建

```bash
python scripts/validate_skills.py
python scripts/validate_finance_config.py
python scripts/build_chatgpt_plugin.py
```

输出：`dist/ai-invest-assistant-chatgpt-v1.0.0.zip`。

ZIP 根目录必须直接包含 `plugin.json`、`agents/openai.yaml` 和完整 `skills/`，不应只上传某个 Skill 子目录。

## 能力边界

该包是 Skills-only 插件，不声明未经验证的行情 MCP endpoint 或交易 API。真实数据能力需要部署并登记数据供应商/MCP；真实交易能力必须由单独的交易服务、授权和安全流程提供。
