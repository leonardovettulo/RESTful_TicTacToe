# RESTful_TicTacToe
RESTful API for classic game Tic Tac Toe with API Client


REST API developed in Python with SQLAlchemy and Marshmallow
Also included Client in Javascript

# Game
The game is to be played between HUMAN and COMPUTER
• Human chooses ‘X’ and computer ‘O’ to mark their respective cells.
• The game starts with one of the players and the game ends when one of the
players has one whole row/ column/ diagonal filled with his/her respective
character (‘O’ or ‘X’).
• If no one wins, then the game is said to be draw.


## Install principal packages

We need Git to clone the project and PIP to install Python packages:

It is recommended to create a virtual environment before installing flask and all other dependencies

```
pipenv shell
pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
```

NOTE: by default, host and port are 'localhost' and '5000' respectively.


## How to use the application

To use the application you have to run the main module.

```
python main.py
```

Then, you can make queries using a client like Postman. 

Also you can use the client (main.html) - Depending on your machine, you have to install the plugin for Chrome "Allow CORS"

## Definition of REST

 - Create one game
POST - localhost:5000/games

For example you have to send:
```
{
	"name":"Mi juego nuevo",
	"status":"new",
	"winner":"none"
}
```

 - Delete one game

 DELETE - localhost:5000/games/<id>

 - Get all games

GET - localhost:5000/games

For example you will receive:
```
[
  {
    "id": 1,
    "name": "Leo",
    "status": "Finished",
    "winner": "computer_won"
  },
  {
    "id": 2,
    "name": "Leo2",
    "status": "Finished",
    "winner": "human_won"
  }
]
```

 - Get one game
GET - localhost:5000/games/2

For example you will receive:
```
{
    "id": 1,
    "name": "Leo",
    "status": "Finished",
    "winner": "computer_won"
  }
```

 - Update one game
PUT - localhost:5000/games/1

For example you have to send:
```
{
  "name": "game1 UPDATED",
  "status": "new",
  "winner": "none"
}
```

 - Add one move
POST - localhost:5000/games/1

For example you have to send:
```
{
	"move":"000000100"
}
```

 - Delete all moves from one game - For testing
DELETE - localhost:5000/games/<id>/moves


 - Get all moves from a game (used for loading existing games)
GET - localhost:5000/games/<id>/moves