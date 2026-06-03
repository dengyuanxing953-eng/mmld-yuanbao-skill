# Examples · 真实运行示例

本目录收录 `mmld-yuanbao-skill` 的端到端运行示例，用于演示 Skill 从「商户原始信息输入」到「符合腾讯元宝检索机制 + Princeton GEO 策略的内容输出」的完整链路。

## wangyibo-bbq · 王亿博鲜活烧烤（唐家湾海景露台店）

一家珠海唐家湾烧烤店的完整生成案例。

| 文件 | 说明 |
|------|------|
| [`input.md`](wangyibo-bbq/input.md) | 触发 Skill 的原始商户信息 + 解析后的结构化字段 |
| [`wechat_article.md`](wangyibo-bbq/wechat_article.md) | 生成的微信公众号文章（元宝 L1 级检索源） |
| [`tencent_news.txt`](wangyibo-bbq/tencent_news.txt) | 生成的腾讯新闻稿（客观报道体） |
| [`metadata.json`](wangyibo-bbq/metadata.json) | 标题池、关键词布局、摘要、GEO 策略落地记录 |

### 这个示例演示了什么

1. **GEO 三大策略的真实落地**——不是关键词堆砌，而是 Cite Sources / Quotation Addition / Statistics Addition 三条 Princeton 论文证实有效的策略，逐条对应到正文具体位置（见各输出文件末尾的策略落地说明表）。
2. **双平台差异化适配**——同一商户信息，公众号文章走种草笔触，腾讯新闻稿走客观报道体，对应元宝不同检索源的收录调性。
3. **合规预检**——全部输出通过 `references/compliance_checklist.md`，无《广告法》第九条绝对化用语、无伪造数据。

> 注：示例中的商户为演示用例，数据用于展示策略落地形态。实际使用时，第三方凭证与引语必须为真实可核验信息。
