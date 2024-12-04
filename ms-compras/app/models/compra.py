from app import db
import datetime
import pytz

class Compra(db.Model):
    __tablename__ = 'compras'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False)
    direccion_envio = db.Column(db.String(128), nullable=False)