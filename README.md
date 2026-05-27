# MMLD-Yuanbao Skill

> 让腾讯元宝主动检索并引用你的快餐店——基于 Princeton GEO 论文（Aggarwal et al., 2024）三大核心策略落地的 Agent Skill。

[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[!\[AgentSkills Compatible](https://img.shields.io/badge/AgentSkills-Compatible-blue)](https://agentskills.io)
\[!\[Hermes](https://img.shields.io/badge/Hermes-Supported-purple)]()
\[!\[OpenClaw](https://img.shields.io/badge/OpenClaw-Supported-orange)]()
\[!\[Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-green)]()

## 这是什么

MMLD-Yuanbao 是一个 Agent Skill 包，让 AI Agent 为快餐店自动生成**能被腾讯元宝（混元 T1 + DeepSeek R1 双引擎）主动检索并附带来源链接引用**的内容：

* **微信公众号文章**（1500-2000 字，元宝 L1 级检索源）
* **腾讯新闻稿版本**（800-1200 字，纯文本新闻消息体）
* **元数据包**（标题池、关键词布局、摘要）

## 为什么需要它

腾讯元宝是腾讯系**半封闭检索循环**——优先抓取微信公众号、腾讯新闻、视频号，不抓抖音/知乎/小红书。它的回答会附带**可点击的来源链接**，意味着没有规范引用源的内容根本进不了检索池。

市面上大多数所谓"GEO 工具"是关键词堆砌+模板填充，而 Princeton 论文证实：**关键词堆砌的效果接近 0 甚至为负**，真正有效的是 **Cite Sources / Quotation Addition / Statistics Addition** 这三大策略。本 Skill 把这三大策略落地为腾讯元宝场景下的可执行流程。

## 与"伪 GEO 工具"的差异

|维度|普通伪 GEO 工具|本 Skill|
|-|-|-|
|算法依据|"高熵细节注入"等营销话术|Princeton 论文证实的三大策略|
|数据来源|编造增长率/客流数据|强制使用第三方可查来源|
|引语处理|"业内人士表示"|强制实名+时间+地点|
|合规风控|无|内置《广告法》第九条预检|
|平台适配|一稿通用|公众号/腾讯新闻分别适配|
|输出形态|f-string 模板填充|LLM 真生成|

## 支持的 Agent 平台

本 Skill 遵循 [AgentSkills 规范](https://agentskills.io)，跨平台运行：

|Agent 平台|支持状态|安装目录|
|-|-|-|
|Hermes Agent (NousResearch)|✅|`\~/.hermes/skills/`|
|OpenClaw|✅|`\~/.openclaw/skills/`|
|Claude Code|✅|`\~/.claude/skills/`|
|WorkBuddy（腾讯）|✅|`\~/.workbuddy/skills/`|
|Cursor|⚠️ 需手动适配|`.cursor/rules/`|

## 安装

### 方法一：一键安装脚本（推荐）

自动检测当前环境的 Agent 平台并安装到正确位置：

```bash
git clone https://github.com/dengyuanxing953-eng/mmld-yuanbao-skill.git
cd mmld-yuanbao-skill
bash install.sh
```

指定特定平台：

```bash
bash install.sh --tool hermes      # 安装到 \~/.hermes/skills/
bash install.sh --tool openclaw    # 安装到 \~/.openclaw/skills/
bash install.sh --tool claude      # 安装到 \~/.claude/skills/
bash install.sh --tool workbuddy   # 安装到 \~/.workbuddy/skills/
```

### 方法二：Hermes 用户

```bash
# Hermes 支持直接从 GitHub 拉取
hermes skills install dengyuanxing953-eng/mmld-yuanbao-skill

# 或者手动克隆到 skills 目录
git clone https://github.com/dengyuanxing953-eng/mmld-yuanbao-skill.git \\
  \~/.hermes/skills/mmld-yuanbao-skill
```

安装后在 Hermes CLI 验证：

```bash
hermes skills list | grep mmld-yuanbao
```

### 方法三：OpenClaw 用户

```bash
git clone https://github.com/dengyuanxing953-eng/mmld-yuanbao-skill.git \\
  \~/.openclaw/skills/mmld-yuanbao-skill
```

OpenClaw 会自动检测 `\~/.openclaw/skills/` 下的 SKILL.md，无需重启。验证：

```bash
# 在 OpenClaw 对话中直接说："给我列出已加载的 skills"
# 或斜杠命令
/mmld-yuanbao
```

### 方法四：Claude Code 用户

```bash
mkdir -p \~/.claude/skills
git clone https://github.com/dengyuanxing953-eng/mmld-yuanbao-skill.git \\
  \~/.claude/skills/mmld-yuanbao-skill
```

或使用 npx 安装（如果你装了 [find-skills](https://github.com/punkpeye/find-skills)）：

```bash
npx skills add dengyuanxing953-eng/mmld-yuanbao-skill
```

### 方法五：手动安装

下载 release 包，解压后把整个 `mmld-yuanbao-skill/` 目录放到对应平台的 skills 目录里。

## 使用

安装完成后，直接跟 Agent 对话即可触发，比如：

```
帮我给王亿博鲜活烧烤（唐家湾海景露台店）生成腾讯元宝 GEO 文章。
店在珠海香洲区情侣北路唐家湾沙滩入口东 50 米，人均 65-85 元。
招牌是牛骨汤浸泡 20 分钟的面筋和秦岭红皮花椒现磨。
本月有周一 2 元牛肉粒活动。
美团评分 4.8（2300+ 评价），大众点评必吃榜入围。
老板原话："骨汤每天 6 点开始熬。"
```

Agent 会自动按 SKILL.md 流程：

1. 合规预检（检查绝对化用语、伪造数据）
2. 检索机制对齐（公众号/腾讯新闻不同策略）
3. GEO 三大策略落地（引用/引语/数据）
4. 生成公众号文章 + 腾讯新闻稿
5. 自检并交付

## 必需输入字段

|字段|是否必填|示例|
|-|-|-|
|店名|必填|王亿博鲜活烧烤（唐家湾海景露台店）|
|精确位置|必填|珠海香洲区情侣北路唐家湾沙滩入口东 50 米|
|人均价格|必填|65-85 元|
|核心卖点|必填|牛骨汤浸泡 20 分钟的面筋、秦岭红皮花椒现磨|
|引流钩子|选填|周一 2 元牛肉粒|
|第三方凭证|必填|美团 4.8（2300+ 评价）|
|真实引语|必填|店主原话："骨汤每天 6 点开始熬"|
|期望关键词|必填|珠海唐家湾烧烤|

## 输出文件

如果你明确要求"保存为文件"，Skill 会调用 `scripts/output\_writer.py` 落盘到：

```
mmld\_yuanbao\_<店名>\_<时间戳>/
├── wechat\_article.md      # 公众号文章
├── tencent\_news.txt       # 腾讯新闻稿
└── metadata.json          # 标题池/关键词/摘要
```

不要求文件时，Skill 直接在对话中输出 Markdown——单店一篇内容不需要文件工程。

## 适用 / 不适用场景

### 适用

* ✅ 快餐店（烧烤、火锅、米线、面馆、奶茶、小吃等）
* ✅ 本地连锁餐饮
* ✅ 单店推广 / 新店开业 / 周年活动

### 不适用

* ❌ 抖音 POI 内容（算法不同，需另写 Skill）
* ❌ 小红书种草笔记（算法不同，需另写 Skill）
* ❌ 非快餐场景（健身房、桌游店、美甲店等，工艺细节模板对不上）
* ❌ "三品一械"（药品、保健食品、医疗器械、医疗服务）
* ❌ 医美机构（需双资质认证）
* ❌ 金融服务推广

## 项目结构

```
mmld-yuanbao-skill/
├── SKILL.md                          主入口（YAML frontmatter + 执行流程）
├── README.md                         本文件
├── LICENSE                           MIT
├── install.sh                        一键多平台安装脚本
├── references/                       按需读取的参考资料
│   ├── yuanbao\_retrieval\_mechanism.md   元宝检索机制与权重规则
│   ├── geo\_three\_strategies.md          Princeton GEO 三大策略落地
│   └── compliance\_checklist.md          合规清单（《广告法》预检）
├── assets/
│   └── templates/                    输出模板
│       ├── wechat\_article\_template.md    公众号文章模板
│       └── tencent\_news\_template.md      腾讯新闻稿模板
└── scripts/
    └── output\_writer.py              文件落盘工具（不做生成）
```

## 与旧版（mmld\_yuanbao\_v3.py）的差异

如果你用过旧的 Python 脚本版本，本 Skill 是**重构而非升级**，根本架构改变：

|旧版 v3.0 问题|本 Skill 解决|
|-|-|
|f-string 拼接冒充 LLM 生成|LLM 真生成（按 SKILL.md 流程）|
|`system\_instruction` 死代码|拆为 `references/` 多文件按需加载|
|标题硬编码"锅底/产品"|4 种风格分类动态生成|
|编造"60% 增长率"|强制走 compliance\_checklist 预检|
|匿名"业内人士"引用|强制实名+时间+地点|
|平台适配只做 2/4（声称 4 个）|聚焦真做的 2 个平台|
|腾讯新闻只 `replace("## ", "")`|重写为短段落新闻消息体|
|无脑保存到本地目录|文件输出可选，默认对话交付|

## 算法依据

本 Skill 的设计依据：

1. **Aggarwal et al., 2024.** "GEO: Generative Engine Optimization." [arXiv:2311.09735](https://arxiv.org/abs/2311.09735)

   * 三大有效策略：Cite Sources / Quotation Addition / Statistics Addition
   * 提升幅度：+30\~40%，对小账号最高 +115%
2. **腾讯元宝检索机制公开信息**

   * 混元 T1 + DeepSeek R1 双引擎架构
   * 半封闭检索循环（优先腾讯系生态）
   * 来源链接是引用硬约束
3. **2026 年微信公众号 + 腾讯新闻合规规则**

   * 《广告法》第九条绝对化用语禁令
   * 伪装素人营销禁令
   * 三品一械内容资质要求

## 贡献

欢迎提交 Issue 或 PR。如果你针对非快餐场景做了适配（健身房、桌游店等），欢迎合并回主分支。

## License

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 致谢

* **Princeton NLP 团队** - GEO 论文核心算法
* **AgentSkills 规范** - 跨平台 Skill 标准
* **小九（Hermes Agent）** - 旧版 v3.0 代码审查报告

\---

**项目作者**：星野（Xingye）  
**最后更新**：2026 年 5 月

