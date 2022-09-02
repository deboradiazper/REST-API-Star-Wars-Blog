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
from models import db, User, Characters, Planets, Favourites 
import json
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




#lista characters
@app.route('/characters', methods=['GET'])
def handle_characters():
        characters = Characters.query.all()
        data = [character.serialize() for character in characters]

        return jsonify(data), 200


#single characters
@app.route('/characters/<int:id>', methods=['GET'])
def handle_singlecharacters(id):
        characters_id = Characters.query.get(id)

        return jsonify(characters.serialize()), 200


#listar planetas
@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    data = [planet.serialize() for planet in planets]

    return jsonify(data), 200


#id planetas
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_singleplanets(id):
    planets_id = Planets.query.all(id)

    return jsonify(planets.serialize()), 200


#usuarios
@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    data = [user.serialize() for user in users]

    return jsonify(data), 200
    

#favoritos usuarios
@app.route('/favourites', methods=['GET'])
def handle_favourites():
    favourites = Favourites.query.all()
    data = [favourites.serialize() for favourite in favourites]

    return jsonify(data), 200


@app.route('/favourites/<int:id>', methods=['GET'])
def handle_signlefavourites(id):
    favourites = Favourites.query.all(id)
    
    return jsonify(favourites.serialize()), 200


#añadir character y planet favoritos
@app.route('/user/<int:id>', methods=['POST'])
def add_favourites(id):
    data = request.json
    favourites = Favourites(user_id=data.get('user_id'), character_id=data.get('characters_id'), planets_id=('planets_id'))
    db.session.add(favourites)
    db.session.commit()
    
    return jsonify({"message": "everything went ok :)"}), 200


#eliminar favoritos
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_favourites(id):
    data = request.json
    favourites = Favourites(character_id=data.get('characters_id'), planets_id=('planets_id'))
    db.session.delete(favourites)
    db.session.commit()

    return jsonify({"message": "favourite removed"}), 200

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
