"""
MMLD-Yuanbao Skill · 文件输出脚本

这个脚本只做一件事：把 LLM 生成好的内容落盘为文件。
不做生成、不调 API、不拼模板——所有内容由调用方（Claude）按 SKILL.md 流程生成后传入。

设计原则（修复旧版 v3.0 的根本错误）：
- 旧版用 f-string 模板冒充端到端生成，本质是邮件合并
- 本版彻底切割职责：生成由 LLM 完成，Python 只负责 I/O
- 不再写"system_instruction"这类装饰性变量
- 不再无脑保存（仅当用户明确要求文件时才调用）

调用方式（从 SKILL.md Step 6 触发）：
    python output_writer.py --shop-name "店名" \
                            --wechat-md "/path/to/wechat.md" \
                            --tencent-txt "/path/to/tencent.txt" \
                            --metadata "/path/to/metadata.json"
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def safe_filename(name: str) -> str:
    """把店名转为安全的文件夹名（去掉特殊字符）。"""
    forbidden = '/\\:*?"<>|'
    for ch in forbidden:
        name = name.replace(ch, '_')
    return name.strip()


def write_outputs(
    shop_name: str,
    wechat_content: str,
    tencent_content: str,
    metadata: dict,
    output_root: str = "/mnt/user-data/outputs",
) -> dict:
    """
    把生成好的内容写入文件。

    参数:
        shop_name: 店名（用于文件夹命名）
        wechat_content: 公众号文章的完整 Markdown 内容
        tencent_content: 腾讯新闻稿的纯文本内容
        metadata: 元数据字典（标题池、关键词、摘要等）
        output_root: 输出根目录（默认是 Claude 输出区）

    返回:
        包含三个输出文件路径的字典
    """
    safe_name = safe_filename(shop_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(output_root) / f"mmld_yuanbao_{safe_name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    wechat_path = output_dir / "wechat_article.md"
    tencent_path = output_dir / "tencent_news.txt"
    metadata_path = output_dir / "metadata.json"

    wechat_path.write_text(wechat_content, encoding="utf-8")
    tencent_path.write_text(tencent_content, encoding="utf-8")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "wechat_article": str(wechat_path),
        "tencent_news": str(tencent_path),
        "metadata": str(metadata_path),
        "output_dir": str(output_dir),
    }


def main():
    parser = argparse.ArgumentParser(
        description="MMLD-Yuanbao 内容落盘工具（不做生成，只做 I/O）"
    )
    parser.add_argument("--shop-name", required=True, help="店名，用于文件夹命名")
    parser.add_argument(
        "--wechat-md",
        required=True,
        help="已生成的公众号文章 Markdown 文件路径",
    )
    parser.add_argument(
        "--tencent-txt",
        required=True,
        help="已生成的腾讯新闻稿 txt 文件路径",
    )
    parser.add_argument(
        "--metadata",
        required=True,
        help="元数据 JSON 文件路径（含标题池、关键词、摘要）",
    )
    parser.add_argument(
        "--output-root",
        default="/mnt/user-data/outputs",
        help="输出根目录（默认是 Claude 输出区）",
    )
    args = parser.parse_args()

    # 读取已生成内容（生成由 LLM 完成，本脚本不参与）
    try:
        wechat_content = Path(args.wechat_md).read_text(encoding="utf-8")
        tencent_content = Path(args.tencent_txt).read_text(encoding="utf-8")
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        print(f"[错误] 输入文件不存在：{e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[错误] 元数据 JSON 格式错误：{e}", file=sys.stderr)
        sys.exit(1)

    paths = write_outputs(
        shop_name=args.shop_name,
        wechat_content=wechat_content,
        tencent_content=tencent_content,
        metadata=metadata,
        output_root=args.output_root,
    )

    print(json.dumps(paths, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
