from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
LOG_ROOT = ROOT / "logs"
START = "<!-- LOG_INDEX_START -->"
END = "<!-- LOG_INDEX_END -->"


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def main() -> None:
    entries: list[tuple[str, str, str]] = []
    for path in LOG_ROOT.rglob("*.md"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not match:
            continue
        date = match.group(1)
        title = first_heading(path)
        rel = path.relative_to(ROOT).as_posix()
        entries.append((date, path.name, f"- `{date[5:]}` [{title}](./{rel})"))

    entries.sort(key=lambda item: (item[0], item[1]), reverse=True)
    body = "\n".join(item[2] for item in entries[:15])

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise RuntimeError("README log index markers are missing")

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    replacement = f"{START}\n{body}\n{END}"
    README.write_text(pattern.sub(replacement, text), encoding="utf-8")
    print(f"README index rebuilt with {min(len(entries), 15)} entries")


if __name__ == "__main__":
    main()
