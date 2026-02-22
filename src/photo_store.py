import os
from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
PHOTO_ROOT = DATA_DIR / 'photos'


def _category_dir(category: str) -> Path:
    directory = PHOTO_ROOT / category
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_photo(category: str, file_storage) -> str:
    filename = secure_filename(file_storage.filename or '')
    ext = Path(filename).suffix.lower()
    photo_id = f'{uuid4().hex}{ext}'
    directory = _category_dir(category)
    file_storage.save(directory / photo_id)
    return photo_id


def list_photo_ids(category: str) -> list[str]:
    directory = _category_dir(category)
    return sorted([name for name in os.listdir(directory) if (directory / name).is_file()])


def delete_photo(photo_id: str, category: str) -> None:
    path = _category_dir(category) / photo_id
    if path.exists():
        path.unlink()
