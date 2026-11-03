---
name: intent-router
description: "当用户提出金融问题、投资研究、行情分析、选股、策略、组合、风险或绩效任务时使用；识别市场与任务意图、判断复杂度并选择唯一主 Skill 和必要辅助 Skills。"
---

# 金融意图识别与路由

## 1. 输入识别

优先识别以下信息；用户没有提供且并非完成任务的必要条件时，不反复追问：
- 任务：解释、分析、比较、筛选、计划、复盘或报告；
- 市场：A 股、港股、美股、基金/ETF 或其他；
- 对象：指数、证券代码、行业、组合或策略；
- 时点：当前、指定交易日、历史区间或财报期间；
- 约束：持有周期、风险承受能力、资金和禁止事项；
- 数据：用户文件、数据源、实时/延迟/历史属性。

证券代码必须与市场/交易所联合确认，避免跨市场代码歧义。

## 2. 路由表

| 意图 | 主 Skill | 辅助 Skill（按需） |
|---|---|---|
| 金融术语、指标基础 | 无，直接回答 | 无 |
| 行情、K 线、财务和宏观数据 | market-data | 对应分析 Skill |
| 宏观、货币政策、利率、汇率 | macro-analysis | market-data、market-analysis |
| 大盘、指数、成交、市场广度 | market-analysis | market-data、macro-analysis |
| 行业板块、概念和轮动 | industry-analysis | market-data、market-analysis |
| 公司研究、财务和估值 | stock-research | market-data、industry-analysis |
| 条件选股和多指标评分 | stock-screening | market-data、industry-analysis |
| 策略规则、回测和参数敏感性 | strategy-analysis | stock-screening、risk-management |
| 基金或 ETF | fund-etf-analysis | market-data、risk-management |
| 持仓和资产配置 | portfolio-management | market-data、risk-management |
| 风险审查 | risk-management | portfolio-management |
| 入场/退出/仓位计划 | trading-plan | risk-management |
| 交易记录和复盘 | trade-journal | portfolio-management |
| 绩效、胜率、回撤 | performance-analysis | trade-journal、risk-management |
| 综合研究报告 | investment-report | 只加载报告所需领域 Skill |

## 3. 任务等级

- S0：概念解释、单一指标定义，无需加载领域 Skill。
- S1：一个明确研究或分析任务，选择一个主 Skill。
- S2：需要多维数据或组合判断，选择一个主 Skill，必要时加载 1-2 个辅助 Skills。
- S3：跨市场、选股到交易、组合整体审查或绩效闭环，按阶段执行并设置质量门禁。

## 4. 路由规则

1. 任意一次任务只指定一个主 Skill；其他 Skills 只能作为辅助能力。
2. 优先遵循用户明确指定的市场、证券、周期和角色模式。
3. 先识别任务，再决定是否需要获取数据；概念问答不调用行情接口。
4. 需要实时或最新数据时，必须先确认工具是否能提供相应市场、时点和延迟属性。
5. 若涉及个人账户数据，必须校验当前用户和账户授权。
6. 标准任务通常不超过 3 个 Skills；复杂任务通过阶段拆分控制加载量。
7. 不因用户提及“全面”就默认加载所有 Skills；按交付目标选取。
8. 不确定证券代码或市场时，标注歧义；确实影响分析时再询问一个最关键问题。

## 5. 输出

仅在有帮助时简要列出任务级别、主 Skill、必要辅助 Skill 和本阶段目标，不展示内部路由推理。