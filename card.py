from flask import Flask
from copy import deepcopy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from Crypto.Random.random import shuffle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# While creating a new game, to initialize a deck just to seed the player's hands for the first move
class Deck:
    def __init__(self):
        # self.g_id=g_id
        self.deck = []
        symbols = ["S", "H", "C", "D"]
        numbers = [str(n) for n in range(2, 11)]
        royals = ["A", "K", "Q", "J"]
        faces = numbers + royals
        deck = [face + symbol for symbol in symbols for face in faces]
        shuffle(deck)
        self.deck = deck


# Player1id and Player2id are included separately here to validate the user and let him reconnect to the same game in case of failure
# Game is included to populate the list-games screen for users to join
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamename = db.Column(db.String, nullable=False)
    no_players = db.Column(db.Integer)
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Game %r>' % self.id


# GameMove is modeling the moves to keep track of game summaries post game completion
class GameMove(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    turn_player_id = db.Column(db.Integer, nullable=False)
    player1_hand = db.Column(db.String)
    player2_hand = db.Column(db.String)
    player1_score = db.Column(db.Integer, nullable=False)
    player2_score = db.Column(db.Integer, nullable=False)
    player_action = db.Column(db.String, nullable=False)
    cards_played = db.Column(db.String)
    cards_bluffed = db.Column(db.String)

    def __repr__(self):
        return '<Move %r>' % self.id
