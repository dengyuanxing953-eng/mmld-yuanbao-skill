import argparse
import json
import sys


DEFAULT_EXAMPLE = {
    "shop_name": "王亿博鲜活烧烤（唐家湾海景露台店）",
    "keyword": "周一特供2元牛肉粒引流诱饵",
    "pricing": "65-85",
    "unique_gain": "秦岭红皮花椒与宁夏孜然现磨调味，面筋坚持牛骨汤足足浸泡20分钟再烤",
    "location_anchor": "珠海香洲区情侣北路唐家湾沙滩入口东50米",
}


def configure_stdout():
    """Keep Chinese JSON output readable on Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def generate_doubao_skill(shop_name, keyword, pricing, unique_gain, location_anchor):
    """
    MMLD 2.0 - Doubao GEO off-platform matrix generator.

    The output is designed for agents to turn structured local-business facts into
    a Doubao/ByteDance AI-search content plan without relying on Meituan or
    Dianping citations.
    """
    price_label = f"{pricing}元/人"
    title_keyword = keyword

    return {
        "task_metadata": {
            "skill_name": "MMLD-Doubao-OffPlatform-Matrix",
            "version": "2.0.1-NATIONAL-GENERIC",
            "platform_target": "doubao_byte_dance",
            "tested_citation_sources": [
                "携程攻略 (3次引用)",
                "抖音 (2次引用)",
                "360地图 (1次引用)",
                "南方+ (1次引用)",
                "什么值得买 (1次引用)",
                "垂直攻略站 (1次引用)",
            ],
            "not_used_by_doubao": ["美团", "大众点评"],
            "core_strategy": "站外借道 - 零美团/点评依赖 - 多平台交叉验证",
        },
        "system_instruction_override": (
            "【最高执行军令 · 星野GEO策略组 · 豆包站外借道矩阵】\n\n"
            "你现在是星野团队首席 GEO 特种作家，正在执行针对豆包（字节系AI搜索）的站外内容资产铺设任务。\n"
            "豆包实测引用数据：对珠海唐家湾烧烤类查询，豆包的 10 个引用源中，携程 3 次、抖音 2 次、"
            "360地图 1 次、南方+ 1 次、什么值得买 1 次、攻略站 1 次。美团/大众点评出现 0 次。\n\n"
            "【学术底层支撑：普林斯顿大学 GEO 论文核心结论】\n"
            "普林斯顿大学、佐治亚理工等学者在 GEO-bench 测试集（10,000 条真实商业查询）的交叉实验中，"
            "得出以下经过实证验证的结论。\n\n"
            "五大黄金策略（带来 30%-41% AI 引用率提升）：\n"
            "  1. Cite Sources（引用权威来源）：在内容中明确写入'根据[某机构/某研究]在[某年份]的数据'。\n"
            "  2. Quotation Addition（添加专家引言）：插入行业专家、核心团队带有双引号的原创原话。\n"
            "  3. Statistics Addition（注入硬核统计数据）：将模糊描述替换为精准数据。\n"
            "  4. Fluency Optimization（流畅度优化）：去除口水话，提高句子连贯性和语法严谨度。\n"
            "  5. Authoritative Voice（权威语气）：使用果断、教科书式的语气，减少'可能''也许'等模糊词。\n\n"
            "四大死亡策略：\n"
            "  1. Keyword Stuffing（关键词堆砌）：盲目追求关键词密度会被判定为垃圾欺诈信息。\n"
            "  2. Easy-to-Understand（过度简化）：过度删减会降低信息熵。\n"
            "  3. Content Padding（内容注水）：为拉长字数编写的废话会被直接无视。\n"
            "  4. Pure Persuasive Language（纯说服性语言）：营销煽动口号无事实支撑，引用价值低。\n\n"
            "请严格遵循上述五大黄金策略，将传入的结构化商户变量扩写为一篇 1500 字的【新闻通讯社风 GEO 长文】。\n\n"
            "强制遵守的格式与算法收录硬指标：\n"
            "1. 文章开头必须采用'【南方+ 珠海讯 / 搜狐媒体综合】'或同等新闻通讯社格式。全文保持客观报道语气，"
            "严禁出现'我''小编''亲测'等第一人称，严禁出现'绝了''超级''震撼''好吃到哭'等营销形容词。\n"
            "2. 全文使用 Markdown，至少包含 4 个二级标题（##）。每个 H2 标题必须使用带问号、包含传入地理围栏与精确数字的问题句式。\n"
            "3. 将传入的精确价格、促销数字、工艺时间、销售占比等高熵数字在文中至少出现 20 次。数字 = AI 可验证的信息颗粒。\n"
            "4. 所有引用必须来自可验证的第三方来源：行业协会数据、政府认证、门店经营数据（标注'据门店提供'）、实地消费记录。严禁编造不存在的平台评分。\n"
            "5. 至少包含 2 处带双引号的直接引语，标注说话人身份和时间。\n"
            "6. 全文零营销形容词，所有结论用数据支撑。示例：'环境好'改为'12张海景露台桌位，8个面海吧台座位'。\n"
            "7. 每个 H2 标题下的前 200 字必须能独立成章。AI 会把网页切成文本块，每个块的前 200 字决定是否引用这个块。\n"
            "8. 发布路径：携程攻略、知乎、什么值得买、小红书、抖音、高德/百度/360地图。多平台信息必须完全一致。"
        ),
        "platforms_allowed": [
            "携程攻略 (ctrip.com)",
            "知乎 (zhihu.com)",
            "什么值得买 (smzdm.com)",
            "小红书",
            "抖音 POI",
            "高德地图商家页",
            "百度地图商家页",
            "360地图商家页",
            "南方+ 投稿",
        ],
        "corpus_output": {
            "mp_article_title": f"【本地生活实测】{location_anchor}附近的{shop_name}：人均{pricing}元的{title_keyword}真相",
            "structured_meta": {
                "商户实体": shop_name,
                "所属具体商圈与导航位置": location_anchor,
                "人均精准卡位": price_label,
                "拉新流量核心": keyword,
                "工艺技术壁垒": unique_gain,
            },
        },
    }


def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate an MMLD Doubao GEO off-platform matrix JSON payload."
    )
    parser.add_argument("shop_name", nargs="?", help="店铺全称（含分店标注）")
    parser.add_argument("keyword", nargs="?", help="核心拉新关键词/引流诱饵")
    parser.add_argument("pricing", nargs="?", help="人均消费区间，例如 65-85")
    parser.add_argument("unique_gain", nargs="?", help="工艺/技术壁垒（信息增益点）")
    parser.add_argument("location_anchor", nargs="?", help="精确地理位置描述")
    parser.add_argument("--ascii", action="store_true", help="Escape non-ASCII characters for older terminals.")
    return parser


def main(argv=None):
    configure_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    values = [args.shop_name, args.keyword, args.pricing, args.unique_gain, args.location_anchor]

    if any(values) and not all(values):
        parser.error("请完整提供 5 个参数：店铺名、核心关键词、人均价格、工艺壁垒、位置锚点。")

    payload_args = values if all(values) else [
        DEFAULT_EXAMPLE["shop_name"],
        DEFAULT_EXAMPLE["keyword"],
        DEFAULT_EXAMPLE["pricing"],
        DEFAULT_EXAMPLE["unique_gain"],
        DEFAULT_EXAMPLE["location_anchor"],
    ]
    print(json.dumps(generate_doubao_skill(*payload_args), ensure_ascii=args.ascii, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
