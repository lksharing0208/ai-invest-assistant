# Claude / Claude Code Adapter

## 映射原则

统一 Agent 源文件位于 `agent/`，模型无关金融能力位于 `skills/`。平台差异只进入 Adapter，不反向污染通用 Skills。

## Skills

将 `skills/<skill-name>/SKILL.md` 映射到 Claude 支持的 Skill 目录，并保留 YAML Front Matter。每个 Skill 的 references、scripts 和 assets 按需映射并保持相对路径。

## Agent

将 `agent/instructions.md` 和 `agent/manifest.yaml` 转换为目标 Claude Runtime 对应的主 Agent/Subagent 指令文件。不要将统一 manifest 的所有字段原样复制到平台 Front Matter。

## 金融约束

- 数据工具只使用当前 Runtime 已注册且授权的工具；
- 保留行情数据源、数据时间、市场和统计口径；
- 不将个人账户信息暴露给未授权上下文；
- 不执行未授权真实交易。

本文件是适配说明，不是 Claude 可直接加载的 Agent 文件。
