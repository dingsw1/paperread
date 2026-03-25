# BACKLOG

- [x] 项目初始化与文档：添加 README、SKILL.md，完善 AGENTS.md 的遵循
- [x] 实现 beamforming 过滤的上下文检查，确保仅在音频上下文存在时纳入 Beamforming
- [x] 完整实现 8 篇论文的抓取、过滤、读取、HTML 生成流程，并接入 LLM 评测
- [ ] 增强实验信息抽取：从全文/章节中提取更细粒度的指标（PESQ/STOI/SISDR/DNSMOS 等等）
- [ ] 增加单元测试覆盖 Beamforming 边界场景（有/无音频上下文）
- [ ] 增加对全文评测的可选开关（仅摘要、全文、两者对比）
- [ ] 将 8 篇论文与数据集跨数据集对比表加入 HTML
- [ ] 引入 PR 模板和代码审查检查清单
- [ ] 引入自动化 CI（lint、测试、静态分析）

- [ ] 发布流水线：生成 CHANGELOG、RELEASE-NOTE、PR 描述
