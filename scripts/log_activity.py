from __future__ import annotations

import hashlib
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
ROOT = Path(__file__).resolve().parents[1]


def _clean_inline(value: str) -> str:
    return " ".join((value or "").strip().split())


def append_log(
    *,
    title: str,
    category: str = "Work",
    summary: str = "",
    details: str = "",
    link: str = "",
    source: str = "Manual",
    when: datetime | None = None,
) -> tuple[bool, Path]:
    when = when or datetime.now(KST)
    if when.tzinfo is None:
        when = when.replace(tzinfo=KST)
    when = when.astimezone(KST)

    title = _clean_inline(title)
    category = _clean_inline(category) or "Work"
    summary = _clean_inline(summary)
    source = _clean_inline(source) or "Manual"
    link = (link or "").strip()
    details = (details or "").strip()

    if not title:
        raise ValueError("title is required")

    fingerprint_raw = f"{source}|{title}|{link}".encode("utf-8")
    fingerprint = hashlib.sha1(fingerprint_raw).hexdigest()[:12]
    marker = f"<!-- log:{fingerprint} -->"

    log_path = ROOT / "logs" / f"{when:%Y}" / f"{when:%m}" / f"{when:%Y-%m-%d}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        if marker in existing:
            return False, log_path
    else:
        existing = (
            f"# {when:%Y-%m-%d} Work Log\n\n"
            "> 디자인·UX/UI·웹·AI·블로그 작업의 핵심만 짧게 기록합니다. "
            "세부 프로젝트 내용은 해당 저장소에 남깁니다.\n"
        )

    block = [
        "",
        f"## {when:%H:%M} · {title}",
        "",
        f"`{category}` · `{source}`",
        "",
    ]

    if summary:
        block.append(summary)
        block.append("")

    if details:
        block.extend(["### Notes", "", details, ""])

    if link:
        block.extend([f"→ [Related link]({link})", ""])

    block.append(marker)
    block.append("")

    log_path.write_text(existing.rstrip() + "\n" + "\n".join(block), encoding="utf-8")
    return True, log_path


def main() -> None:
    changed, path = append_log(
        title=os.environ.get("LOG_TITLE", ""),
        category=os.environ.get("LOG_CATEGORY", "Work"),
        summary=os.environ.get("LOG_SUMMARY", ""),
        details=os.environ.get("LOG_DETAILS", ""),
        link=os.environ.get("LOG_LINK", ""),
        source=os.environ.get("LOG_SOURCE", "GitHub Action"),
    )
    print(f"{'updated' if changed else 'skipped duplicate'}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
