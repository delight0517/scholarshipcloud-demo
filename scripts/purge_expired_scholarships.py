#!/usr/bin/env python3
"""
purge_expired_scholarships.py

ScholarshipCloud의 scholarships.json에서 마감일(deadline)이 30일 이상 지난
공고를 "삭제"하되, 실제로는 완전히 버리지 않고 scholarships_archive.json에
옮겨서 데이터를 보존한다(사용자 요청: "지워도 데이터 유지").

동작:
- dist/scholarships.json, docs/scholarships.json 둘 다 동일하게 처리한다
  (두 폴더가 같은 데이터를 미러링하는 정적 사이트 구조이기 때문).
- 각 항목의 deadline(ISO 날짜 문자열)을 기준으로, 오늘 - deadline > 30일이면
  active 목록에서 빼고 archive 목록에 append한다.
- deadline이 없거나 파싱 불가능한 항목은 만료 판단을 하지 않고 그대로 active에
  남긴다(잘못 지우는 것을 방지).
- archive 파일은 append-only로 유지하고, 같은 항목(title+deadline 기준)이
  중복 추가되지 않도록 한다.
- 변경 사항이 있을 때만 파일을 다시 쓰고, 변경 여부를 출력한다(호출부가
  git commit 여부를 판단할 수 있게).

사용법:
  python3 purge_expired_scholarships.py <repo_root>
"""

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

RETENTION_DAYS = 30


def parse_deadline(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value)[:10]).date()
    except (ValueError, TypeError):
        return None


def archive_key(item):
    return (item.get("title", ""), item.get("deadline", ""))


def process_pair(active_path: Path, archive_path: Path, today: date):
    if not active_path.exists():
        return {"path": str(active_path), "skipped": "missing"}

    active_items = json.loads(active_path.read_text(encoding="utf-8"))
    if not isinstance(active_items, list):
        return {"path": str(active_path), "skipped": "not_a_list"}

    archive_items = []
    if archive_path.exists():
        try:
            archive_items = json.loads(archive_path.read_text(encoding="utf-8"))
            if not isinstance(archive_items, list):
                archive_items = []
        except (json.JSONDecodeError, ValueError):
            archive_items = []

    archive_keys = {archive_key(item) for item in archive_items}

    kept = []
    newly_archived = []
    for item in active_items:
        deadline = parse_deadline(item.get("deadline"))
        if deadline is not None and (today - deadline) > timedelta(days=RETENTION_DAYS):
            item_with_meta = dict(item)
            item_with_meta["archivedAt"] = today.isoformat()
            item_with_meta["archivedReason"] = f"deadline_passed_{RETENTION_DAYS}_days"
            key = archive_key(item)
            if key not in archive_keys:
                newly_archived.append(item_with_meta)
                archive_keys.add(key)
            # deadline이 지났고 30일이 넘었으면 active에서는 무조건 제외
            # (이미 archive에 있던 항목이라도 active에는 안 남긴다).
            continue
        kept.append(item)

    changed = len(newly_archived) > 0 or len(kept) != len(active_items)
    if changed:
        active_path.write_text(
            json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        archive_items.extend(newly_archived)
        archive_path.write_text(
            json.dumps(archive_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return {
        "path": str(active_path),
        "kept": len(kept),
        "newly_archived": len(newly_archived),
        "changed": changed,
    }


def main():
    if len(sys.argv) < 2:
        print("usage: purge_expired_scholarships.py <repo_root>")
        sys.exit(1)

    repo_root = Path(sys.argv[1])
    today = date.today()
    results = []
    for sub in ["dist", "docs"]:
        active = repo_root / sub / "scholarships.json"
        archive = repo_root / sub / "scholarships_archive.json"
        results.append(process_pair(active, archive, today))

    print(json.dumps({"today": today.isoformat(), "results": results}, ensure_ascii=False, indent=2))
    any_changed = any(r.get("changed") for r in results)
    sys.exit(0 if not any_changed else 2)  # 2 = changed, caller can check for commit


if __name__ == "__main__":
    main()
