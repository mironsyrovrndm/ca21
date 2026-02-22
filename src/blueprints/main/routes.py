from pathlib import Path

from flask import Blueprint, abort, render_template, request, send_from_directory, session

from src.content_store import load_content
from src.records_store import add_record
from src.photo_store import list_photo_ids

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/main-static')

PHOTO_ROOT = Path(__file__).resolve().parents[3] / 'data' / 'photos'


@main_bp.route('/')
@main_bp.route('/<lang>/')
def index(lang='ru'):
    session['lang'] = lang
    return render_template('main/index.j2', content=load_content(), gallery_images=list_photo_ids('uploads'), submitted=False)


@main_bp.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    telegram = request.form.get('telegram', '').strip()
    complaint = request.form.get('complaint', '').strip()
    if name and phone and complaint:
        add_record(
            {
                'date': 'Новая заявка',
                'name': name,
                'phone': phone,
                'telegram': telegram,
                'complaint': complaint,
                'status': 'Новая',
            }
        )
    return render_template('main/index.j2', content=load_content(), gallery_images=list_photo_ids('uploads'), submitted=True)


@main_bp.route('/media/<category>/<path:photo_id>')
def media(category, photo_id):
    if category not in {'hero', 'about', 'uploads'}:
        abort(404)
    category_dir = PHOTO_ROOT / category
    file_path = category_dir / photo_id
    if not file_path.exists():
        abort(404)
    return send_from_directory(category_dir, photo_id)
