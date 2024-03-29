"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

################# GET #######################

# OBTENER INFO DE TODOS LOS USUARIOS
@app.route('/user', methods=['GET'])
def get_all_users():
    # Declaración de las Querys
    users_query = User.query.all()
    results = list(map(lambda item: item.serialize(), users_query))
    response_body = {
        "msg": "GET /user = ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER INFO DE UN SOLO USUARIO
@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user_query = User.query.filter_by(id=user_id).first()
    response_body = {
        "msg": "GET /user = ok",
        "results": user_query.serialize()
    }
    return jsonify(response_body), 200

# OBTENER INFO PERSONAJES
@app.route('/personajes', methods=['GET'])
def info_personajes():
    # Declaración de las Querys
    personajes_query = Personajes.query.all()
    results = list(map(lambda item: item.serialize(), personajes_query))
    response_body = {
        "msg": "GET /personajes = ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER INFO DE UN SOLO PERSONAJE
@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def get_info_personaje(personajes_id):
    # Declaración de las Querys
    personaje_query = Personajes.query.filter_by(id=personajes_id).first()
    response_body = {
        "msg": "GET /personaje = ok",
        "results": personaje_query.serialize()
    }
    return jsonify(response_body), 200


# OBTENER INFO PLANETAS
@app.route('/planetas', methods=['GET'])
def info_planetas():
    # Declaración de las Querys
    planetas_query = Planetas.query.all()
    results = list(map(lambda item: item.serialize(), planetas_query))
    response_body = {
        "msg": "GET /planetas = ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER INFO DE UN SOLO PLANETA
@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_info_planeta(planetas_id):
    # Declaración de las Querys
    planeta_query = Planetas.query.filter_by(id=planetas_id).first()
    response_body = {
        "msg": "GET /planeta = ok",
        "results": planeta_query.serialize()
    }
    return jsonify(response_body), 200

# OBTENER FAVORTIOS
@app.route('/favoritos', methods=['GET'])
def get_favortios():
    # Declaración de las Querys
    favoritos_query = Favoritos.query.all()
    results = list(map(lambda item: item.serialize(),favoritos_query))
    response_body = {
        "msg": "GET /favortios = ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER UN FAVORITO
@app.route('/favoritos/<int:favoritos_id>', methods=['GET'])
def get_one_favorito(favoritos_id):
    # Declaración de las Querys
    favorito_query = Favoritos.query.filter_by(id=favoritos_id).all()
    results = list(map(lambda item: item.serialize(), favorito_query))
    response_body = {
        "msg": "GET /favorito = ok",
        "results": results
    }
    return jsonify(response_body), 200



################# POST #######################


# CREAR NUEVO USUARIO
@app.route('/user', methods=['POST'])
def crear_usuario():
    request_body = request.json
    user_query = User.query.filter_by(email=request_body["email"]).first()
    if user_query is None:
        user = User(email=request_body["email"], password=request_body["password"], nombre=request_body["nombre"])
        db.session.add(user)
        db.session.commit()
        response_body = {
            "msg": "POST /crear usuario = ok",
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"El usuario ya existe"}), 400

# CREAR NUEVO PERSONAJE
@app.route('/personajes', methods=['POST'])
def crear_personaje():
    request_body = request.json
    personaje_query = Personajes.query.filter_by(nombre=request_body["nombre"]).first()
    if personaje_query is None:
        personaje = Personajes(nombre=request_body["nombre"], altura=request_body["altura"], genero=request_body["genero"], peso=request_body["peso"])
        db.session.add(personaje)
        db.session.commit()
        response_body = {
            "msg": "POST /crear personaje = ok",
            "result": personaje.serialize()
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"El personaje ya existe"}), 400

# CREAR NUEVO PLANETA 
@app.route('/planetas', methods=['POST'])
def crear_planeta():
    request_body = request.json
    planeta_query = Planetas.query.filter_by(nombre=request_body["nombre"]).first()
    if planeta_query is None:
        planeta = Planetas(nombre=request_body["nombre"], habitantes=request_body["habitantes"], periodo_orbital=request_body["periodo_orbital"], diametro=request_body["diametro"])
        db.session.add(planeta)
        db.session.commit()
        response_body = {
            "msg": "POST /crear planeta = ok",
            "result": planeta.serialize()
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"El planeta ya existe"}), 400

#AÑADIR PLANETA FAVORITO
@app.route('/favoritos/planetas/<int:planetas_id>', methods=['POST'])
def crear_planeta_favorito(planetas_id):
    request_body = request.json
    planeta_fav = Favoritos(user_id=request_body["user_id"], planetas_id=planetas_id)
    db.session.add(planeta_fav)
    db.session.commit()
    response_body = {
            "msg": "Planeta añadido a favoritos",
        }

    return jsonify(response_body), 200

#AÑADIR PERSONAJE FAVORITO
@app.route('/favoritos/personajes/<int:personajes_id>', methods=['POST'])
def crear_personaje_favorito(personajes_id):
    request_body = request.json
    personaje_fav = Favoritos(user_id=request_body["user_id"], personajes_id=personajes_id)
    db.session.add(personaje_fav)
    db.session.commit()
    response_body = {
            "msg": "El personaje fue añadido a favortiso",
        }

    return jsonify(response_body), 200



############################################  DELETE ##############################################################

# ELIMINAR UN PERSONAJE
@app.route('/personajes/<int:position>', methods=['DELETE'])
def delete_personajes(position):
    personajes_query = Personajes.query.filter_by(id=position).first()
    if personajes_query is None : 
        response_body = {
            "msg": "el personaje no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(personajes_query)
        db.session.commit()
        
        response_body = {
                "msg": "el personaje fue eliminado",
                "result": personajes_query.serialize()
            }
        return  jsonify(response_body), 200

# ELIMINAR UN PERSONAJE FAVORITO DE UN USUARIO
@app.route('/favoritos/personajes/<int:position>', methods=['DELETE'])
def borrar_personaje_favorito(position):
    request_body = request.json
    personaje_query = Favoritos.query.filter_by(user_id=request_body["user_id"], personajes_id=position).first()
    if personaje_query is None : 
        response_body = {
            "msg": "el personaje no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(personaje_query)
        db.session.commit()
        response_body = {
                "msg": "el personaje fue eliminado",
                "result": personaje_query.serialize()
            }
        return  jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
