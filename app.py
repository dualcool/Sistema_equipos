from flask import Flask, render_template, request, jsonify, session, redirect
from database import db, Equipo, Usuario
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_segura'

# 🔥 BASE DE DATOS DINÁMICA (IMPORTANTE)
database_url = os.getenv('DATABASE_URL')

if database_url:
    # Render usa postgres, a veces viene con postgres://
    database_url = database_url.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 🔥 CREAR TABLAS Y ADMIN
with app.app_context():
    db.create_all()

    if Usuario.query.count() == 0:
        admin = Usuario(username='admin')
        admin.set_password('1234')
        db.session.add(admin)
        db.session.commit()

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()

        if user and user.check_password(request.form['password']):
            session['user'] = user.username
            return redirect('/')
        else:
            return "Credenciales incorrectas"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# PROTECCIÓN
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    equipos = Equipo.query.order_by(Equipo.id.desc()).all()
    return render_template('index.html', equipos=[e.to_dict() for e in equipos])

# API
@app.route('/api/equipos')
def api_equipos():
    return jsonify([e.to_dict() for e in Equipo.query.all()])

@app.route('/api/equipo', methods=['POST'])
def crear():
    data = request.json

    equipo = Equipo(**{
        k: v for k, v in data.items()
        if k in Equipo.__table__.columns.keys()
    })

    db.session.add(equipo)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/equipo/<int:id>', methods=['GET'])
def obtener(id):
    return jsonify(Equipo.query.get_or_404(id).to_dict())

@app.route('/api/equipo/<int:id>', methods=['PUT'])
def actualizar(id):
    equipo = Equipo.query.get_or_404(id)
    data = request.json

    for k, v in data.items():
        if hasattr(equipo, k):
            setattr(equipo, k, v)

    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/equipo/<int:id>', methods=['DELETE'])
def eliminar(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return jsonify({'success': True})

# 🔥 IMPORTANTE PARA RENDER
if __name__ == '__main__':
    app.run()