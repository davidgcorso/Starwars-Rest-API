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
from models import db, Users, People, Planets, Planets_favorites, People_favorites


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
def root():
    return generate_sitemap(app)

@app.route("/users", methods=['GET'])
def get_users():
    users = Users.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    users = Users.query.get(user_id)
    return jsonify(users.serialize()), 200

@app.route("/users/<int:user_id>/favorites", methods=['GET'])
def get_user_favorites(user_id):
    people_favorites = People_favorites.query.all()
    people_favorites = list(map(lambda people_favorites: people_favorites.serialize(), people_favorites))
    planets_favorites = Planets_favorites.query.all()
    planets_favorites = list(map(lambda planets_favorites: planets_favorites.serialize(), planets_favorites))
    return jsonify(planets_favorites,people_favorites), 200

"""@app.route("/users/<int:user_id>/favorites", methods=['GET'])
def get_user_favorites(user_id):

    user = Users.query.get(user_id)
    user = user.get_people()
    user = user.get_planets()

    return jsonify({
        "people": user.people,
        "planets": user.planets,
    }), 200"""

@app.route("/users", methods=['POST'])
def create_user():
    user = Users()
    user.username = request.json.get('username')
    user.email = request.json.get('email')
    user.password = request.json.get('password')
    user.save()
    
    return jsonify(user.serialize()), 201

@app.route("/users/<int:user_id>/favorites_planets", methods=['POST'])
def create_favorite_planet(user_id):
    planets_favorites = Planets_favorites()
    planets_favorites.user_id = user_id
    planets_favorites.planets_id = request.json.get('planets_id')
    planets_favorites.save()
    
    return jsonify(planets_favorites.serialize()), 201

@app.route("/users/<int:user_id>/favorites_people/<int:people_favorites_id>", methods=['DELETE'])
def delete_favorite_people(user_id, favorite_people_id):
    people_favorites = People_favorites.query.get(people_favorites_id)
    people_favorites.delete()

    return jsonify(people_favorites.serialize()), 201

@app.route("/users/<int:user_id>/favorites_planets/<int:favorite_planet_id>", methods=['DELETE'])
def delete_favorite_planet(user_id, favorite_planet_id):
    favorite_planet = FavoritePlanet.query.get(favorite_planet_id)
    favorite_planet.delete()

    return jsonify(favorite_planet.serialize()), 201

@app.route('/people', methods=["GET"])
def getPeople():
    people = People.query.all()
    people = list(map(lambda person: person.serialize(), people))
    return jsonify(people), 200

@app.route("/people/<int:people_id>", methods = ["GET"])
def get_People(people_id):
    people = People.query.get(people_id)
    
    if people:
        return jsonify(people.serialize())

    return jsonify({"message": "People not found"}, 404)

"""@app.route("/users/<int:user_id>/favorites_people", methods=['POST'])
def create_favorite_person(user_id):
    people_favorites = People_favorites()
    people_favorites.user_id = user_id
    people_favorites.person_id = request.json.get('person_id')
    people_favorites.save()
    
    return jsonify(favorite_people.serialize()), 201"""

@app.route("/users/<int:user_id>/favorites_people", methods=['POST'])
def create_favorite_people(user_id):
    people_favorites = People_favorites()
    people_favorites.user_id = user_id
    people_favorites.people_id = request.json.get('people_id')
    people_favorites.save()
    
    return jsonify(people_favorites.serialize()), 201

@app.route("/people", methods=['POST'])
def createPerson():
    people = People()
    people.name = request.json.get('name')
    people.gender = request.json.get('gender')
    people.birth_year = request.json.get('birth_year')
    people.height = request.json.get('height')
    people.hair_color = request.json.get('hair_color')
    people.eye_color = request.json.get('eye_color')
  
    people.save()
    
    return jsonify(people.serialize()), 201


@app.route("/planets", methods=['GET'])
def getPlanets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route("/planets/<int:planet_id>", methods = ["GET"])
def getPlanet(planet_id):
    planet = Planets.query.get(planet_id)
    
    if planet:
        return jsonify(planet.serialize())

    return jsonify({"message": "Planet not found"}), 404

@app.route("/planets", methods=['POST'])
def createPlanet():
    planet = Planets()
    planet.name = request.json.get('name')
    planet.climate = request.json.get('climate')
    planet.terrain = request.json.get('terrain')
    planet.population = request.json.get('population')
    planet.gravity = request.json.get('gravity')
    planet.orbital_period = request.json.get('orbital_period')
   
    planet.save()
    
    return jsonify(planet.serialize()), 201


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
