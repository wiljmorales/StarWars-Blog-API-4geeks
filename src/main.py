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
from models import db, User, Planet, Person, Planet_Favorite, FavoritePerson
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/users', methods=['GET'])
def handle_users():

    all_users = User.query.all()

    return jsonify(
        [user.serialize() for user in all_users]
        ), 200

@app.route('/users/<int:user_id>/favorites')
def handle_favorites(user_id):
    favorite_planets = Planet_Favorite.query.filter_by(user_id=user_id)
    favorite_people = FavoritePerson.query.filter_by(user_id=user_id)
    favorites = list(favorite_people) + list(favorite_planets)
    return jsonify(
        [fav.serialize() for fav in favorites]
        ), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_favorite_planet(planet_id):
    if request.method == 'POST':
        body = request.json
        new_favorite = Planet_Favorite(user_id=body['user_id'], planet_id =planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    else:
        # Para que funcione este edpoit hay que usar el id de la tabla planet__favorite
        favorite = Planet_Favorite.query.filter_by(id=planet_id).one_or_none()
        db.session.delete(favorite)
        try:
            db.session.commit()
            return "", 204
        except Exception as error:
            print(error.args)
            return jsonify('Something goes wrong ???????'), 500

@app.route('/favorite/people/<int:person_id>', methods=['POST', 'DELETE'])
def handle_favorite_person(person_id):
    if request.method == 'POST':
        body = request.json
        new_favorite = FavoritePerson(user_id=body['user_id'], person_id =person_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    else:
        # Para que funcione este edpoit hay que usar el id de la tabla favorite_person
        favorite = FavoritePerson.query.filter_by(id=person_id).one_or_none()
        db.session.delete(favorite)
        try:
            db.session.commit()
            return "", 204
        except Exception as error:
            print(error.args)
            return jsonify('Something goes wrong ???????'), 500


@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        all_planets = Planet.query.all()
        return jsonify(
            [planet.serialize() for planet in all_planets]
        ), 200
    else:
        body = request.json
        new_planet = Planet.create(body["name"])
        if new_planet is None:
            return jsonify('Something goes wrong =('), 400
        return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['DELETE', 'GET', 'PUT'])
def handle_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).one_or_none()
    if planet is None:
        return jsonify("Planet not found"), 404
    if request.method == 'GET':
        return jsonify(planet.serialize()),200
    elif request.method == 'DELETE':
        delete = planet.delete()
        if not delete: return jsonify('Something goes wrong ???????'), 500
        return "", 204
    else: 
        body = request.json
        planet.update(body["name"])
        return jsonify(planet.serialize()), 200

@app.route('/people', methods=['GET', 'POST'])
def handle_people():
    if request.method == 'GET':
        people = Person.query.all()
        return jsonify(
            [person.serialize() for person in people]
        ), 200
    else:
        body = request.json
        new_person = Person.create(body["name"])
        if new_person is None:
            return jsonify('Something goes wrong =('), 400
        return jsonify(new_person.serialize()), 201

@app.route('/people/<int:person_id>', methods=['DELETE', 'GET', 'PUT'])
def handle_person(person_id):
    person = Person.query.filter_by(id=person_id).one_or_none()
    if person is None:
        return jsonify("Person not found"), 404
    if request.method == 'GET':
        return jsonify(person.serialize()),200
    elif request.method == 'DELETE':
        delete = person.delete()
        if not delete: return jsonify('Something goes wrong ???????'), 500
        return "", 204
    else: 
        body = request.json
        person.update(body["name"])
        return jsonify(person.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
