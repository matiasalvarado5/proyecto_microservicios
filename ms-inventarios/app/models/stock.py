from app import db

class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key = True)
    producto_id = db.Column(db.Integer, nullable = False)
    fecha_transaccion = db.Column(db.DateTime, nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    entrada_salida = db.Column(db.Integer, nullable = False)