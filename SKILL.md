---
name: mmld-doubao
description: Generate Doubao/ByteDance AI-search GEO off-platform content matrices for local businesses, including structured JSON prompts, platform deployment guidance, and article inputs. Use when the user wants MMLD Doubao GEO strategy, local-business AI search optimization, or a reusable content-generation workflow for Doubao without relying on Meituan/Dianping.
---

# MMLD Doubao

## Purpose

Use this skill to create a Doubao-focused GEO off-platform matrix for a local business. The workflow produces a structured JSON payload containing strategy metadata, a system-level writing prompt, allowed distribution platforms, and business facts that another agent can expand into a 1500-word news-style GEO article.

## Required Inputs

Collect these five values before generating the payload:

| Field | Meaning | Example |
| --- | --- | --- |
| `shop_name` | Full business name, including branch label | 王亿博鲜活烧烤（唐家湾海景露台店） |
| `keyword` | Core acquisition keyword or traffic hook | 周一特供2元牛肉粒引流诱饵 |
| `pricing` | Per-person price range | 65-85 |
| `unique_gain` | Craft, process, supply-chain, or technical differentiation | 秦岭红皮花椒与宁夏孜然现磨调味 |
| `location_anchor` | Precise geographic anchor | 珠海香洲区情侣北路唐家湾沙滩入口东50米 |

## Workflow

1. Validate that all five input values are concrete and consistent across platforms.
2. Run `scripts/mmld_doubao_v2.py` from the skill folder to produce the JSON payload:

```bash
python scripts/mmld_doubao_v2.py "<店铺名>" "<核心关键词>" "<人均价格>" "<工艺壁垒>" "<位置锚点>"
```

3. Use `system_instruction_override` as the controlling instruction for the content-writing agent.
4. Use `corpus_output.structured_meta` as the user/business facts for the writing agent.
5. Expand the material into a 1500-word news-agency-style GEO article.
6. Deploy consistent facts across Ctrip, Zhihu, SMZDM, Xiaohongshu, Douyin POI, and map business pages.

## Strategy Rules

- Treat Meituan and Dianping as non-primary sources for Doubao GEO. Do not fabricate Meituan/Dianping ratings or reviews.
- Favor third-party, verifiable sources such as travel guides, map listings, short-video POI pages, local media, industry data, government certifications, and merchant-provided operating data that is clearly labeled.
- Keep store name, address, phone number, price, and key claims identical across every platform.
- Write in a factual news style. Avoid first person, hype adjectives, keyword stuffing, and padded claims.
- Include precise numbers, direct quotations, and source-style references so each paragraph has citation value for AI search.
- Make each H2 section independently useful in its first 200 Chinese characters because AI retrieval systems may chunk the article.

## Output Contract

The script returns JSON with these top-level keys:

- `task_metadata`: Skill version, platform target, tested citation source assumptions, and strategy summary.
- `system_instruction_override`: The high-priority writing instruction for the downstream agent.
- `platforms_allowed`: Recommended off-platform distribution surfaces.
- `corpus_output`: Article title and structured business facts.

## Portability Notes

The script has no third-party Python dependencies. Use Python 3.9 or newer. On Windows terminals with encoding issues, run:

```bash
python -X utf8 scripts/mmld_doubao_v2.py
```
