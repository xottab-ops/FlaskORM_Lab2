from flask import Flask
from app.extensions import db, ma
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///structure.db"
    app.json.ensure_ascii = False
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        from app.models import Country, City, Building, TypeBuilding

        db.create_all()

    from app.routes.buildings import building_bp

    app.register_blueprint(building_bp, url_prefix="/structures/api/v1")

    return app
