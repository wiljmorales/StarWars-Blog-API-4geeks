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
from models import db, User, Planet
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

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

@app.route('/planets/<int:planet_id>', methods=['DELETE', 'GET', 'PATCH'])
def handle_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).one_or_none()
    if planet is None:
        return jsonify("Planet not found"), 404
    if request.method == 'GET':
        return jsonify(planet.serialize()),200
    elif request.method == 'DELETE':
        delete = planet.delete()
        if not delete: return jsonify('Something goes wrong 🤕️'), 500
        return "", 204
    else: 
        body = request.json
        planet.update(body["name"])
        return jsonify(planet.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
