import os, redis
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

load_dotenv()

# Variables de entorno rutas de microservicios
CATALOGO_SERVICE_URL = os.getenv('CATALOGO_SERVICE_URL')
INVENTARIO_SERVICE_URL = os.getenv('INVENTARIO_SERVICE_URL')
PAGOS_SERVICE_URL = os.getenv('PAGOS_SERVICE_URL')
COMPRAS_SERVICE_URL = os.getenv('COMPRAS_SERVICE_URL')
MAIN_COMMERCE_COMPRA_URL = os.getenv('MAIN-COMMERCE-COMPRA_URL')

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

    redis_client = redis.StrictRedis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        db=os.getenv('REDIS_DB'),
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
    )
    app.redis_client = redis_client

    #Registro de blueprints
    from app.routes.pagos_routes import pagos_bp
    app.register_blueprint(pagos_bp, url_prefix='/api/pagos')
    from app.routes.catalogo_route import catalogo_bp
    app.register_blueprint(catalogo_bp, url_prefix='/api/catalogo')
    from app.routes.compras_route import compras_bp
    app.register_blueprint(compras_bp, url_prefix='/api/compras')
    from app.routes.inventario_route import inventario_bp
    app.register_blueprint(inventario_bp, url_prefix='/api/inventario')
    from app.routes.registrar_compra_route import registrar_compra_bp
    app.register_blueprint(registrar_compra_bp, url_prefix='/api/compra')

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({"status": "Error", "detail": str(error)}), 400

    return app