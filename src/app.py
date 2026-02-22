import os
from importlib import import_module
from flask import Blueprint, Flask, send_from_directory
from werkzeug.security import generate_password_hash

from extensions import init_extensions
from models import User
from extensions import db


def ensure_default_admin() -> None:
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password_hash=generate_password_hash('admin99'))
        db.session.add(admin)
        db.session.commit()


def create_app() -> Flask:
    _app = Flask(__name__, static_folder='static')

    # 1. Загружаем конфиг
    _app.config.from_pyfile("settings.py")
    _app.config.from_envvar("FLASK_SETTINGS")

    return _app


app = create_app()

with app.app_context():
    init_extensions(app)
    ensure_default_admin()
    for name in ['main', 'admin']:
        try:
            mod = import_module(f"src.blueprints.{name}.routes")
            for item in vars(mod).values():
                if isinstance(item, Blueprint):
                    app.register_blueprint(item)
                    break
        except Exception as e:
            print(f"Error loading {name}: {e}")


# === РОУТ ДЛЯ КАРТИНОК ===
# Отдает файлы из папки /uploads (которая в конфиге)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
