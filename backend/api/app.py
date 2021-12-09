from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
import os

app = Flask(__name__)

# Connect to MongoDB database
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
app.config["MONGO_URI"] = f'mongodb+srv://{db_user}:{db_pass}@cluster0.yfg5a.mongodb.net/playerSentiments?retryWrites=true&w=majority'
mongo = PyMongo(app)
db = mongo.db


@app.route('/players', methods=['GET'])
def get_all_players():
    """ Route to get all player documents. """
    players = db.players.find()
    return dumps(players)


@app.route('/players/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    """ Route to get a specific player document. """
    player = db.players.find({'player_id': player_id})
    return dumps(player)


if __name__ == "__main__":
    app.run(debug=True)

