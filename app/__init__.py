from flask import Flask
from .db import db, migrate
from .models.planet import Planet
from .models.moon import Moon
from .routes.routes import bp as planets_bp
from .routes.moon_routes import bp as moons_bp
import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if test_config:
        app.config.update(test_config)
        
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(planets_bp)
    app.register_blueprint(moons_bp)

    return app
