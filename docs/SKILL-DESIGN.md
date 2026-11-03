# AI 金融助手 Skills 设计规范

## 1. 设计目标

建立统一 Agent + 16 个金融 Skills 的结构。主控 Agent 负责意图与编排，专项 Skills 负责单一金融专业能力。所有技能作为同一个 AI 金融助手的能力模块，不拆分成独立主 Agent 或独立插件。

## 2. Skills 清单

| Skill | 职责 |
|---|---|
| ai-invest-workflow | 唯一金融主控工作流 |
| intent-router | 意图分类和路由 |
| market-data | 金融数据需求与质量校验 |
| macro-analysis | 宏观分析 |
| market-analysis | 市场分析 |
| industry-analysis | 行业/板块研究 |
| stock-research | 个股基本面与估值研究 |
| stock-screening | 指标选股 |
| strategy-analysis | 策略状态机、回测和参数分析 |
| fund-etf-analysis | 基金 ETF 研究 |
| portfolio-management | 个人组合分析 |
| risk-management | 投资风险 |
| trading-plan | 条件性交易计划 |
| trade-journal | 交易记录和复盘 |
| performance-analysis | 投资绩效 |
| investment-report | 投资研究报告 |

## 3. 目录约束

每个 Skill 目录必须包含一个根级 SKILL.md。可选 references/scripts/assets/agents 子目录。名称采用小写 kebab-case，Front Matter 的 name 必须与目录名一致。

## 4. 职责边界

- Agent：主控、路由、上下文、阶段和质量门禁。
- Intent Router：意图、市场和任务等级。
- market-data：数据获取和质量验证，不绑定供应商。
- 研究 Skills：解释数据和形成研究判断。
- screening/strategy：规则化筛选、状态机和策略验证。
- portfolio/risk：账户范围内的资产和风险分析。
- trading-plan：输出计划，不等于提交订单。
- trade-journal/performance：个人记录与绩效，严格隔离。
- investment-report：证据汇总和报告交付。

## 5. 每个 Skill 最低内容

触发描述、职责边界、输入与数据要求、执行步骤、计算/分析约束、风险和异常处理、输出结构、协作关系或参考资料。

## 6. 业务配置外置

市场、股票池、指标、权重、策略参数、风险限额和绩效口径放入 config/。未配置值不能被当作默认安全阈值。配置需要版本、生效时间和审计记录。

## 7. 数据与金融安全

所有行情结论保留来源与时间；财务数据需区分报告期和披露日；收益/回测需统一复权、现金流、成本和样本口径；个人资产与记录按授权隔离；真实交易能力与分析能力分离。
