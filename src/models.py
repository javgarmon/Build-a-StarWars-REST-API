from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favoritos = db.relationship('Favoritos', backref='user', lazy=True)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    favoritos = db.relationship('Favoritos', backref='personajes', lazy=True)

    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "genero": self.genero,
            "peso": self.peso,
        }

class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    habitantes = db.Column(db.Integer, nullable=False)
    periodo_orbital = db.Column(db.Integer, nullable=False)
    diametro = db.Column(db.Integer, nullable=False)
    favoritos = db.relationship('Favoritos', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "habitantes": self.habitantes,
            "periodo_orbital": self.periodo_orbital,
            "diametro": self.diametro,
        }

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=True)
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=True)

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id,
        }