import os
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_REDIS_HOST' : os.getenv('REDIS_HOST'),
        'CACHE_REDIS_PORT' : os.getenv('REDIS_PORT'),
        'CACHE_REDIS_DB' : os.getenv('REDIS_DB'),
        'CACHE_REDIS_PASSWORD' : os.getenv('REDIS_PASSWORD'), 
        'CACHE_KEY_PREFIX': 'main-commerce_'
    })

    from app.routes.catalogo_routes import catalogo_bp
    app.register_blueprint(catalogo_bp, url_prefix='/api/catalogo')

    return app
