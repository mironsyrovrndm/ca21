import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CONTENT_FILE = DATA_DIR / 'content.json'

DEFAULT_CONTENT = {
    'hero_label': 'Бережная и профессиональная поддержка',
    'hero_title': 'Психолог Анна Луиза',
    'hero_text': 'Помогаю вернуть опору, услышать себя и улучшить качество жизни.',
    'hero_button': 'Записаться на консультацию',
    'hero_image': '',
    'about_image': '',
    'about_title': 'Обо мне',
    'about_education': ['Высшее психологическое образование'],
    'products_title': 'Продукты',
    'products': [
        {'badge': 'Индивидуально', 'title': 'Личная консультация', 'text': 'Разбор вашего запроса.', 'meta': '60 минут'}
    ],
    'clients_title': 'Клиентам',
    'clients_subtitle': 'Работаю бережно и в вашем темпе.',
    'clients': [
        {'title': 'Тревога и стресс', 'text': 'Находим устойчивость и способы саморегуляции.'},
    ],
    'supervision_title': 'Супервизия',
    'supervision_subtitle': 'Для начинающих и практикующих специалистов.',
    'supervision': [
        {'title': 'Разовая супервизия', 'price': '5 000 ₽', 'meta': '90 минут', 'bullets': ['Разбор кейса']}
    ],
    'speaker_title': 'Я — спикер',
    'speaker_text': 'Провожу лекции и практические выступления о ментальном здоровье.',
    'speaker_button': 'Оставить заявку',
    'contacts_title': 'Контакты',
    'contacts_text': 'Оставьте заявку, и я свяжусь с вами в ближайшее время.',
    'contacts_phone': '+7 (900) 000-00-00',
    'contacts_email': 'hello@luiza-psy.ru',
    'contacts_telegram': '@luiza_psy',
}


def load_content() -> dict:
    if not CONTENT_FILE.exists():
        return dict(DEFAULT_CONTENT)
    try:
        with CONTENT_FILE.open('r', encoding='utf-8') as fp:
            data = json.load(fp)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONTENT)
    return {**DEFAULT_CONTENT, **data}


def save_content(payload: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with CONTENT_FILE.open('w', encoding='utf-8') as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
