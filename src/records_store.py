import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
RECORDS_FILE = DATA_DIR / 'records.json'


def load_records() -> list[dict]:
    if not RECORDS_FILE.exists():
        return []
    try:
        with RECORDS_FILE.open('r', encoding='utf-8') as fp:
            data = json.load(fp)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_records(records: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with RECORDS_FILE.open('w', encoding='utf-8') as fp:
        json.dump(records, fp, ensure_ascii=False, indent=2)


def add_record(record: dict) -> None:
    records = load_records()
    next_id = max((int(item.get('id', 0)) for item in records), default=0) + 1
    records.append({'id': str(next_id), **record})
    _save_records(records)


def update_record_status(record_id: str, status: str) -> None:
    records = load_records()
    for record in records:
        if str(record.get('id')) == str(record_id):
            record['status'] = status
            break
    _save_records(records)
