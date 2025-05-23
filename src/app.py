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
from models import db, User, Favorite, Character, Planet, Vehicle
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    data = [c.serialize() for c in characters]
    return jsonify(data), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    character = Character.query.get(people_id)
    if character:
        return jsonify(character.serialize()), 200
    return jsonify({'msj': 'No se encontro al personaje'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    data = [p.serialize() for p in planets]
    return jsonify(data), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({'msj': 'No se encontro el planeta'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [u.serialize() for u in users]
    return jsonify(data), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favs = Favorite.query.all()
    data = [f.serialize() for f in favs]
    return jsonify(data), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def favorite_person(people_id):
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({'msj': 'El id del usuario es requerido'}), 400
    character = Character.query.get(people_id)
    if not character:
        return jsonify({'msj': 'El personaje no fue encontrado y nomastrabajos'}), 404
    
    fav = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def favorite_planet(planet_id):
    user_id = request.json.get('user_id')
        
    if not user_id:
        return jsonify({'msj': 'El id del usuario es requerido'}), 400
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'msj': 'El planeta no fue encontrado y quiero vacaciones'}), 404
    
    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    user_id = request.json.get('planet_id')

    if not user_id:
        return jsonify({'msj': 'El id del usuario no concuerda'}), 400
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({'msj': 'El planeta no fue encontrado'}), 400
    
    db.session.delete(fav)
    db.session.commit()
    return '', 204

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    user_id = request.json.get('people_id')

    if not user_id:
        return jsonify({'msj': 'El id del usuario no concuerda'}), 400
    fav = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not fav:
        return jsonify({'msj': 'El personaje no fue encontrado'}), 400
    
    db.session.delete(fav)
    db.session.commit()
    return '', 204
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
