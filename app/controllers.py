from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from app.models import *


###### CREATE/UPDATE/SHOW/DELETE GAMES

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


#Delete one game
@app.route('/games/<id>', methods=['DELETE'])
def delete_game(id):
    #print(id, file=sys.stderr)

    #Delete children (moves)
    moves_delete = Detail.query.filter(Detail.id_game == id).all()
    result = details_schema.dump(moves_delete)
    num_rows_deleted = db.session.query(Detail).filter(Detail.id_game == id).delete()
    db.session.commit()

    
    game_delete = Game.query.get(id)
    db.session.delete(game_delete)
    db.session.commit()


    return game_schema.jsonify(game_delete)



####GET STATUS
#Get Status
@app.route('/games/<id>/moves', methods=['GET'])
def get_game_status(id):

    board = ['0','0','0','0','0','0','0','0','0']

    game_detail = Game.query.get(id)

    all_moves = Detail.query.filter(Detail.id_game == id).all()
    results = details_schema.dump(all_moves)
    for result in results:
        result_list = list(result['moves'])
        for i in range(len(result_list)):
            if(result_list[i] == '1'):
                board[i] = result_list[i]
            elif(result_list[i] == '2'):
                board[i] = result_list[i]


    board_string = ''.join(board)

    print(game_detail.status, file=sys.stderr)
    return jsonify({"id":game_detail.id,"name":game_detail.name, "status":game_detail.status,"winner":game_detail.winner,"lastMove":board_string})



###### CREATE AND DELETE MOVES IN ONE GAME


#Add a move
@app.route('/games/<id>/moves', methods=['POST'])
def add_move(id):
    move = request.json['move']
    id_game = id
      
    #Check if game exists, if not return message
    game_exists = Game.query.filter_by(id=id).first()
    #print(game_exists, file=sys.stderr)
    if(game_exists is None):
        return jsonify({"Message":"Game does not exist."})


    #TODO_Check if move is valid
    #We need to check here if the string is 9 chars and with 8 zeros and 1 one


    #Check if the move is valid
    """
    #Check if there are moves in the game
    move_exists = Detail.query.filter(Detail.id_game == id).first()
    #print(move_exists, file=sys.stderr)
    if(move_exists is None):
        return jsonify({"Message":"There are no moves"})
    """



    board = ['0','0','0','0','0','0','0','0','0']
    board_1 = ['0','0','0','0','0','0','0','0','0']
    board_2 = ['0','0','0','0','0','0','0','0','0']

    move_counter = 0

    all_moves = Detail.query.filter(Detail.id_game == id).all()
    results = details_schema.dump(all_moves)
    for result in results:
        move_counter += 1
        if (move_counter == 9):
            #end_game('draw')
            # Save in database the result
            return jsonify({"Message":"It's a draw"})
        result_list = list(result['moves'])
        for i in range(len(result_list)):
            if(result_list[i] == '1'):
                board[i] = result_list[i]
                board_1[i] = '1'
            elif(result_list[i] == '2'):
                board[i] = result_list[i]
                board_2[i] = '1'


    #TODO_Check if position is not occupied
    #We need a check here to check if the move is in an empty space


    #Insert move into database
    new_move = Detail(move, id_game)
    db.session.add(new_move)
    db.session.commit()

    
    #Insert move into board
    move_list = list(move)

    for i in range(len(move_list)):
        if(move_list[i]!='0'):
            board[i]=move_list[i]
            board_1[i]='1'
            #x = i #this is move position

    #Check if if user won

    if((board_1[0]=='1' and board_1[1]=='1' and board_1[2]=='1') or
    (board_1[3]=='1' and board_1[4]=='1' and board_1[5]=='1') or
    (board_1[6]=='1' and board_1[7]=='1' and board_1[8]=='1') or
    (board_1[0]=='1' and board_1[3]=='1' and board_1[6]=='1') or
    (board_1[1]=='1' and board_1[4]=='1' and board_1[7]=='1') or
    (board_1[2]=='1' and board_1[5]=='1' and board_1[8]=='1') or
    (board_1[0]=='1' and board_1[4]=='1' and board_1[8]=='1') or
    (board_1[6]=='1' and board_1[4]=='1' and board_1[2]=='1')):
        end_game("human_won",id_game)
        return jsonify({"Message":"You WON"})

    #Make next move (There is not much logic here, computer is a bit dumb)
    temp_move = ['0','0','0','0','0','0','0','0','0']

    if(board[4]=='0'):
        board[4]='2'
        board_2[4]='1'
        temp_move[4] = '2'
    elif(board[0]=='0'):
        board[0]='2'
        board_2[0]='1'
        temp_move[0] = '2'
    elif(board[2]=='0'):
        board[2]='2'
        board_2[2]='1'
        temp_move[2] = '2'
    elif(board[6]=='0'):
        board[6]='2'
        board_2[6]='1'
        temp_move[6] = '2'
    elif(board[8]=='0'):
        board[8]='2'
        board_2[8]='1'
        temp_move[8] = '2'
    else:
        for i in range(len(board)):
            if(board[i]=='0'):
                board[i]='2'
                board_2[i]='1'
                temp_move[i] = '2'
                break


    new_move_temp = ''.join(temp_move)
    print(new_move, file=sys.stderr)

    #Add next move to database
    new_move = Detail(new_move_temp, id_game)
    db.session.add(new_move)
    db.session.commit()

    #Check if computer won

    if((board_2[0]=='1' and board_2[1]=='1' and board_2[2]=='1') or
    (board_2[3]=='1' and board_2[4]=='1' and board_2[5]=='1') or
    (board_2[6]=='1' and board_2[7]=='1' and board_2[8]=='1') or
    (board_2[0]=='1' and board_2[3]=='1' and board_2[6]=='1') or
    (board_2[1]=='1' and board_2[4]=='1' and board_2[7]=='1') or
    (board_2[2]=='1' and board_2[5]=='1' and board_2[8]=='1') or
    (board_2[0]=='1' and board_2[4]=='1' and board_2[8]=='1') or
    (board_2[6]=='1' and board_2[4]=='1' and board_2[2]=='1')):
        end_game("computer_won",id_game)
        return jsonify({"Message":"Computer WON", "lastMove":new_move_temp})

#Return next move
    
    print(board)
    print(board_1)
    print(board_2)

    return detail_schema.jsonify(new_move)


#Delete moves
@app.route('/games/<id>/moves', methods=['DELETE'])
def delete_moves(id):

    moves_delete = Detail.query.filter(Detail.id_game == id).all()
    result = details_schema.dump(moves_delete)

    num_rows_deleted = db.session.query(Detail).filter(Detail.id_game == id).delete()
    db.session.commit()

    return jsonify(result)



def end_game(winner,id_game):
    game = Game.query.get(id_game)
    game.status = "Finished"
    game.winner = winner
    db.session.commit()

    print(winner, file=sys.stderr)
    return True


