---

name: speech-front-end-daily
description: 语音前端论文速递（专注音频信号处理：增强、降噪、波束形成、DOA、AEC等），生成可视化网页日报
-------------------------------------------------------------

# 🎙️ 语音前端论文速递 Skill（工程增强版）

## 🎯 目标

获取近 30 天 arXiv 最新**音频前端处理论文**，精读并生成**结构化网页日报（HTML）**。

---

## 🧭 第一步：获取论文列表

### 数据源（必须使用）

1. [https://arxiv.org/list/cs.SD/new](https://arxiv.org/list/cs.SD/new)
2. [https://arxiv.org/list/eess.AS/new](https://arxiv.org/list/eess.AS/new)

提取：

* 当天所有 arXiv ID
* 合并去重

---

### 🔍 补充策略（论文不足时）

如果当天 < 5 篇，向前扩展 7 天：

关键词：

* speech enhancement
* noise suppression
* beamforming microphone array
* sound source localization DOA
* acoustic echo cancellation AEC
* dereverberation speech
* target speaker extraction
* speech separation

---

## 🚨 第二步：严格过滤（核心规则）

### ✅ 只保留（必须满足之一）

* Speech Enhancement
* Noise Suppression
* Beamforming
* DOA / Localization
* Acoustic Echo Cancellation (AEC)
* Dereverberation
* Howling Suppression
* Target Speaker Extraction

---

### ❌ 强制剔除

* ASR / TTS / Speech LLM
* 多模态（音频+视觉）
* 音乐生成
* 纯理论声学（无算法）
* 数据集论文（无方法）

---

## 📖 第三步：精读论文

### 读取策略

优先：
[https://arxiv.org/html/](https://arxiv.org/html/)<ID>v1

fallback：
PDF

---

### 📌 输出结构（每篇论文）

## [序号] 论文标题

**arXiv ID**:
**方向**:
**作者**:
**机构**:
**发布日期**:
**论文链接**:
**PDF**:
**代码**:
**Demo**:

### 📌 简介

（解决什么问题 + 核心贡献）

### 🔧 技术方案

**模型架构**

* 输入输出形式
* 网络结构（Conv / Transformer / UNet / MVDR等）
* 是否结合传统信号处理

**核心创新**

* 相比已有方法的本质区别
* 是否具备工程落地价值

**训练策略**

* loss 设计
* 数据集与增强方式
* 是否真实录音


---
## 📊 第四步：实验指标信息抽取（必须执行）

### ⚠️ 本步骤目标：
不是解释指标，而是从论文中提取“具体实验结果数据”用于对比分析

### 🧾 抽取内容（每篇论文必须包含）
1️⃣ 数据集信息
使用的数据集名称（如：DNS, WHAM!, LibriSpeech, AEC-Challenge 等）
是否真实录音（real-recorded）或模拟数据（simulated）
是否包含噪声 / 混响 / 多说话人等场景说明
2️⃣ 核心指标数值（必须结构化提取）

### 根据论文任务类型，提取对应指标：

🎯 Speech Enhancement / Noise Suppression

提取：

PESQ（具体数值 + 提升量）
STOI / ESTOI
SI-SDR / SDR
DNSMOS（如有）

示例格式：

PESQ: 2.45 → 3.12 (+0.67)
STOI: 0.91 → 0.95

🎯 Beamforming

提取：

PESQ / STOI / SI-SDR
Array Gain（如有）
Noise Reduction
🎯 DOA / Localization

提取：

MAE（单位：°）
Accuracy（如为分类任务）
🎯 AEC

提取：

ERLE（dB） ⭐ 必须
PESQ / STOI
双讲（double-talk）表现（如有定量指标）
🎯 Dereverberation

提取：

SRMR
PESQ / STOI / SI-SDR
🎯 Speech Separation / Target Speaker Extraction

提取：

SI-SDR improvement（SI-SDRi） ⭐ 必须
SDR
PESQ
🎯 ASR 相关（如论文提供）

提取：

WER（Word Error Rate）
CER（Character Error Rate）

必须记录：

WER: 18.2% → 12.5% (↓5.7%)

3️⃣ Baseline 对比（必须）

必须明确：

对比方法名称（如：DCCRN, Conv-TasNet, MVDR 等）
是否为：
传统方法
深度学习方法
SOTA 方法
4️⃣ 最优结果（Top-line Result）

提取论文中：

最优模型（best model）
对应全部指标
5️⃣ 是否开源
是否提供代码（GitHub）
是否提供 demo（音频）
📦 输出格式（必须统一）

在每篇论文中新增一节：

📊 实验结果（结构化）

Dataset: DNS / WHAM! / AEC-Challenge

Baseline: DCCRN / Conv-TasNet

Results:

PESQ: 2.45 → 3.12 (+0.67)
STOI: 0.91 → 0.95
SI-SDR: 10.2 dB → 15.8 dB (+5.6 dB)

Best Model: Proposed-Net-Large

ASR (optional):

WER: 18.2% → 12.5%
🚨 强制要求
❗ 不允许：
只写“显著提升”“优于 baseline”
不写具体数值
不写对比方法
✅ 必须做到：
至少 2 个指标数值
至少 1 个 baseline 对比
明确提升幅度（+x.xx / ↓x.xx）
🧠 进阶（用于后续自动分析）

建议额外记录：

是否 SOTA（论文是否声明）
是否多数据集验证
是否真实场景测试
⭐ 与评分联动（更新）

评分时必须考虑：

是否提供完整实验指标
是否有强 baseline
是否跨数据集验证

### ⭐ 评分：X/10

理由：创新性 + 实验充分性 + 工程价值

---

## ⭐ 评分标准（偏工程）

9-10：工程突破（可落地产品级）
7-8：有明显改进
5-6：常规优化
3-4：偏学术，工程价值弱
1-2：不推荐

## 🌐 第五步：生成网页（HTML）

### 输出文件路径

/tmp/speech_daily_YYYYMMDD.html

---

### 页面结构要求

必须包含以下内容：

#### 1️⃣ 总览区

* 总论文数
* 各方向统计（SE / AEC / Beamforming 等）

#### 2️⃣ 分类展示

按方向分块：

* Beamforming
* Speech Enhancement
* Noise Suppression
* AEC
* DOA
* Dereverberation
* Target Speaker Extraction

---

#### 3️⃣ 卡片式论文展示

每篇论文使用卡片结构，包含：

* 标题（可点击 arXiv 链接）
* 标签（方向）
* 简介
* 技术方案（可折叠）
* 实验结果
* 评分

---

### HTML 示例结构

<div class="paper-card">
  <h2>🎧 Paper Title</h2>

<span class="tag">Beamforming</span>

  <p><b>简介：</b>论文简介...</p>

  <details>
    <summary>🔧 技术方案</summary>
    <p>详细技术内容...</p>
  </details>

  <p>📊 PESQ: 3.21 ↑</p>

  <p class="score">⭐ 8/10</p>
</div>

---

### 🎨 样式要求（必须）

* 深色模式（默认）
* 卡片式 UI
* 支持折叠（details 标签）
* 不同方向使用不同颜色标签
* 页面简洁、可读性强

---

## ⚙️ 第六步：写文件

必须执行：

1. 将完整 HTML 写入文件：

/tmp/speech_daily_YYYYMMDD.html

2. 返回该路径给用户

---

## 📦 可选增强（推荐）

* 标题点击跳转 arXiv
* GitHub 按钮（如有代码）
* Demo 音频播放（audio 标签）
* 按评分排序

---

## 🚨 注意事项

* 宁缺毋滥（建议最多 20 篇）
* 必须人工判断是否属于“音频前端”
* 优先工程价值（不是论文堆砌）

---

## 🧠 输出风格

* 中文
* 专家视角（偏工程）
* 信息密集，避免废话

---

## ✅ 最终输出

1️⃣ 网页路径

./tmp/speech_daily_YYYYMMDD.html

2️⃣ 简短总结

* 今日研究趋势
* 是否有值得重点关注的论文

---

