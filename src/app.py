import os
from importlib import import_module
from types import ModuleType
from flask import Flask, send_from_directory
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




def _import_blueprint_module(name: str) -> ModuleType:
    errors: list[str] = []
    for module_path in (f"src.blueprints.{name}.routes", f"blueprints.{name}.routes"):
        try:
            return import_module(module_path)
        except Exception as exc:
            errors.append(f"{module_path}: {exc}")
    raise RuntimeError('; '.join(errors))

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
            bp_module = _import_blueprint_module(name)
            blueprint = getattr(bp_module, f"{name}_bp", None)
            if blueprint is None:
                raise RuntimeError(f"Blueprint object '{name}_bp' not found")
            app.register_blueprint(blueprint)
        except Exception as e:
            print(f"Error loading {name}: {e}")


# === РОУТ ДЛЯ КАРТИНОК ===
# Отдает файлы из папки /uploads (которая в конфиге)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
