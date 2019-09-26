from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
import sys

#Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

#Model declaration
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    winner = db.Column(db.String(100), nullable=False)
    details = db.relationship('Detail', backref='game',lazy = True)

    def __init__(self, name, status, winner):
        self.name = name
        self.status = status
        self.winner = winner


class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moves = db.Column(db.String(255), nullable=False)
    id_game = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __init__(self, moves, id_game):
        self.moves = moves
        self.id_game = id_game


#Schema
class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'winner')
        #model = Game

class DetailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'moves', 'id_game')
        #table = Detail.__table__


#Init Schema
game_schema = GameSchema()
games_schema = GameSchema(many=True)


detail_schema = DetailSchema()
details_schema = DetailSchema(many=True)


"""
@app.route('/')
def get():
    return jsonify({"message":"test"})
"""
######GAMES

#Create a game
@app.route('/games', methods=['POST'])
def add_game():
    name = request.json['name']
    status = request.json['status']
    winner = request.json['winner']

    new_game = Game(name, status, winner)
    db.session.add(new_game)
    db.session.commit()
    
    return game_schema.jsonify(new_game)


#Show all games
@app.route('/games', methods=['GET'])
def get_games():
    all_games = Game.query.all()
    result = games_schema.dump(all_games)
    return jsonify(result)


#Show one game
@app.route('/games/<id>', methods=['GET'])
def get_game_detail(id):
    game_detail = Game.query.get(id)
    #result = games_schema.dump(all_games)
    return game_schema.jsonify(game_detail)


#Update a game
@app.route('/games/<id>', methods=['PUT'])
def update_game(id):
    game = Game.query.get(id)

    name = request.json['name']
    status = request.json['status']
    winner = request.json['winner']

    game.name = name
    game.status = status
    game.winner = winner

    db.session.commit()
    
    return game_schema.jsonify(game)



#Run Server
if __name__ == '__main__':
    app.run(debug=True)


