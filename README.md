# AI 金融助手（ai-invest-assistant）

统一 Agent + 16 个金融 Skills 的 AI 金融助手项目，基于 `ai-rd-assistant` 的统一 Agent 源定义、低 Token 编排和多平台 Adapter 规范。

## 项目目标

支持宏观分析、市场分析、行业研究、个股研究、指标选股、策略分析、基金 ETF、投资组合、风险管理、交易计划、交易记录、绩效分析和研究报告。

本仓库当前提供 Agent/Skills 规范、金融策略配置模板、数据与风险策略、校验脚本和 ChatGPT 插件打包适配。**尚未配置真实行情供应商、MCP endpoint、个人账户数据库或交易执行服务。**

## 目录结构

```text
ai-invest-assistant/
├── agent/                  # 统一 Agent 源配置
├── adapters/               # ChatGPT / OpenAI / Claude 适配说明
├── config/                 # 路由、市场、选股、策略、风险和绩效配置
├── policies/               # 金融安全、数据质量、用户隔离策略
├── skills/                 # 16 个金融 Skills
├── references/             # 金融指标、数据源、风险与日历规范
├── templates/              # 研究、选股、交易和绩效报告模板
├── scripts/                # 校验和插件 ZIP 构建
├── docs/                   # 架构和实施规范
└── requirements-dev.txt
```

## 16 个 Skills

1. ai-invest-workflow：唯一主控工作流
2. intent-router：金融意图识别
3. market-data：金融数据获取与质量检查
4. macro-analysis：宏观分析
5. market-analysis：大盘市场分析
6. industry-analysis：行业板块研究
7. stock-research：个股研究
8. stock-screening：指标选股
9. strategy-analysis：投资策略分析
10. fund-etf-analysis：基金 ETF 分析
11. portfolio-management：投资组合管理
12. risk-management：投资风险管理
13. trading-plan：交易计划
14. trade-journal：交易记录和复盘
15. performance-analysis：投资绩效分析
16. investment-report：投资研究报告

## 低 Token 约定

- S0：基础解释，不加载专项 Skill。
- S1：一个主 Skill。
- S2：一个主 Skill + 必要辅助 Skills，通常最多 3 个。
- S3：按阶段执行，不预加载全部 Skills。
- 行情/财务数据需标明来源、时间和口径。
- 用户持仓、账户、交易和绩效数据必须按授权隔离。

## 本地校验

需要 Python 3.10+，安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python scripts/validate_finance_config.py
```

## 构建 ChatGPT 插件包

```bash
python scripts/build_chatgpt_plugin.py
```

生成 `dist/ai-invest-assistant-chatgpt-v1.0.0.zip`。ZIP 根目录直接包含 `plugin.json`、`agents/openai.yaml` 和 `skills/`，所有金融 Skills 属于同一个插件。

## 当前能力边界

- 未登记真实供应商前，不提供实时行情或财务数据服务。
- 未接入真实用户身份、账户存储和授权前，不处理真实个人持仓。
- 未接入有授权的交易服务前，不提交、撤销或修改真实订单。
- 策略模板默认 disabled；不预设交易阈值、风控比例或收益承诺。

详细设计见 `docs/SKILL-DESIGN.md`、`docs/FINANCIAL-DATA-STANDARD.md`、`docs/INVESTMENT-RISK-STANDARD.md` 和 `docs/STRATEGY-ENGINEERING.md`。
