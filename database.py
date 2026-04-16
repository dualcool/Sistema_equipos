from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    cpu = db.Column(db.String(100))
    ram = db.Column(db.String(20))
    almacenamiento = db.Column(db.String(50))
    sistema_operativo = db.Column(db.String(50))
    ip_address = db.Column(db.String(15))

    # NUEVOS CAMPOS
    impresora = db.Column(db.String(100))
    usuario_encargado = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    oficina = db.Column(db.String(100))

    estado = db.Column(db.String(20), default='Bueno')

    fecha_adquisicion = db.Column(db.Date)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'marca': self.marca,
            'modelo': self.modelo,
            'numero_serie': self.numero_serie,
            'tipo': self.tipo,
            'cpu': self.cpu,
            'ram': self.ram,
            'almacenamiento': self.almacenamiento,
            'sistema_operativo': self.sistema_operativo,
            'ip_address': self.ip_address,
            'impresora': self.impresora,
            'usuario_encargado': self.usuario_encargado,
            'departamento': self.departamento,
            'oficina': self.oficina,
            'estado': self.estado,
            'fecha_adquisicion': self.fecha_adquisicion.isoformat() if self.fecha_adquisicion else None,
            'fecha_alta': self.fecha_alta.strftime('%d/%m/%Y') if self.fecha_alta else None,
            'observaciones': self.observaciones
        }

# LOGIN
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)