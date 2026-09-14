from __future__ import annotations

import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from log_activity import append_log

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / ".automation" / "tistory-state.json"
RSS_URL = "https://bini-s2.tistory.com/rss"
KST = ZoneInfo("Asia/Seoul")


def fetch_rss() -> bytes:
    req = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "DesignLogBot/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()


def parse_items(xml_bytes: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(xml_bytes)
    items: list[dict[str, str]] = []
    for node in root.findall(".//item"):
        def text(tag: str) -> str:
            child = node.find(tag)
            return (child.text or "").strip() if child is not None and child.text else ""

        title = text("title")
        link = text("link")
        guid = text("guid") or link
        pub_date = text("pubDate")
        if title and link:
            items.append(
                {
                    "id": guid,
                    "pubDate": pub_date,
                }
            )
    return items


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {
            "initialized": True,
            "started_at": datetime.now(KST).isoformat(timespec="seconds"),
            "seen": [],
        }
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(seen: list[str], started_at: str) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "initialized": True,
        "started_at": started_at,
        "seen": seen[:100],
        "updated_at": datetime.now(KST).isoformat(timespec="seconds"),
    }
    STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def item_datetime(pub_date: str) -> datetime:
    if not pub_date:
        return datetime.now(KST)
    try:
        parsed = parsedate_to_datetime(pub_date)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=KST)
        return parsed.astimezone(KST)
    except (TypeError, ValueError):
        return datetime.now(KST)


def parse_started_at(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=KST)
        return parsed.astimezone(KST)
    except (TypeError, ValueError):
        return datetime.now(KST)


def main() -> None:
    items = parse_items(fetch_rss())
    if not items:
        raise RuntimeError("RSS returned no posts")

    state = load_state()
    started_at_text = state.get("started_at") or datetime.now(KST).isoformat(timespec="seconds")
    started_at = parse_started_at(started_at_text)
    seen = set(state.get("seen", []))
    current_ids = [item["id"] for item in items]

    candidates = [item for item in items if item["id"] not in seen]
    if not seen:
        candidates = [item for item in candidates if item_datetime(item["pubDate"]) >= started_at]

    # 공개 로그에는 RSS의 제목·본문·링크를 복사하지 않는다.
    # 같은 날 여러 글이 발행되어도 비식별 활동 사실 하나만 남긴다.
    days_logged: set[str] = set()
    for item in reversed(candidates):
        when = item_datetime(item["pubDate"])
        day_key = when.strftime("%Y-%m-%d")
        if day_key in days_logged:
            continue
        append_log(
            title="블로그 글 발행",
            category="Blog",
            summary="새 글 발행 활동을 기록함.",
            source="Blog Automation",
            when=when,
        )
        days_logged.add(day_key)

    merged = current_ids + [item_id for item_id in state.get("seen", []) if item_id not in current_ids]
    save_state(merged, started_at_text)
    print(f"synced {len(candidates)} new post(s) with anonymized activity logging")


if __name__ == "__main__":
    main()
