# MMLD-Doubao v2.0

MMLD-Doubao is a Codex skill and standalone Python generator for Doubao/ByteDance AI-search GEO off-platform content matrices.

It is designed for local-business GEO workflows where Doubao should discover consistent, verifiable content from Ctrip, Zhihu, SMZDM, Xiaohongshu, Douyin POI, map listings, and local media instead of relying on Meituan or Dianping.

## What It Generates

The Python script outputs a structured JSON payload with:

- `task_metadata`: Doubao target, citation-source assumptions, and strategy summary
- `system_instruction_override`: a downstream writing prompt for generating news-style GEO content
- `platforms_allowed`: recommended off-platform publishing surfaces
- `corpus_output`: article title and structured local-business facts

## Install as a Codex Skill

Clone the repository into your Codex skills folder:

```bash
git clone https://github.com/<your-username>/MMLD-Doubao.git ~/.codex/skills/mmld-doubao
```

On Windows PowerShell:

```powershell
git clone https://github.com/<your-username>/MMLD-Doubao.git "$env:USERPROFILE\.codex\skills\mmld-doubao"
```

Then invoke it in Codex with:

```text
Use $mmld-doubao to generate a Doubao GEO off-platform content matrix for a local business.
```

## Run Directly

No third-party Python packages are required. Use Python 3.9 or newer.

```bash
python scripts/mmld_doubao_v2.py "<店铺名>" "<核心关键词>" "<人均价格>" "<工艺壁垒>" "<位置锚点>"
```

Example:

```bash
python scripts/mmld_doubao_v2.py \
  "王亿博鲜活烧烤（唐家湾海景露台店）" \
  "周一特供2元牛肉粒引流诱饵" \
  "65-85" \
  "秦岭红皮花椒与宁夏孜然现磨调味，面筋坚持牛骨汤足足浸泡20分钟再烤" \
  "珠海香洲区情侣北路唐家湾沙滩入口东50米"
```

For older Windows terminals, use UTF-8 mode:

```bash
python -X utf8 scripts/mmld_doubao_v2.py
```

The root-level `mmld_doubao_v2.py` remains as a backward-compatible wrapper:

```bash
python mmld_doubao_v2.py
```

## Required Inputs

| Argument | Meaning | Example |
| --- | --- | --- |
| `shop_name` | 店铺全称（含分店标注） | 王亿博鲜活烧烤（唐家湾海景露台店） |
| `keyword` | 核心拉新关键词/引流诱饵 | 周一特供2元牛肉粒引流诱饵 |
| `pricing` | 人均消费区间 | 65-85 |
| `unique_gain` | 工艺/技术壁垒（信息增益点） | 秦岭红皮花椒与宁夏孜然现磨调味 |
| `location_anchor` | 精确地理位置描述 | 珠海香洲区情侣北路唐家湾沙滩入口东50米 |

## GEO Strategy

- Doubao citation assumptions: Ctrip, Douyin, 360 Map, local media, SMZDM, and vertical guide sites.
- Avoid fabricating Meituan/Dianping evidence when optimizing for Doubao.
- Keep store name, address, phone, price, and claims identical across platforms.
- Prefer numbers, source references, direct quotations, and factual paragraphs over promotional language.
- Write each H2 section so its first 200 Chinese characters can stand alone as an AI-search chunk.

## Repository Layout

```text
MMLD-Doubao/
├─ SKILL.md                    # Codex skill instructions
├─ agents/openai.yaml          # UI metadata for Codex skill lists
├─ scripts/mmld_doubao_v2.py   # Canonical generator
├─ mmld_doubao_v2.py           # Backward-compatible wrapper
├─ manifest.json               # Portable metadata for other agents
└─ README.md                   # GitHub usage guide
```

## License

MIT
