document.getElementById('reset').addEventListener('click', reset);
document.getElementById('showGames').addEventListener('click', showGames);
document.getElementById('newGame').addEventListener('submit', newGame);

showGames();

let actualGame = 0;
let gameStatus = "None";
document.getElementById('status').innerHTML = gameStatus;
document.getElementById('actual').innerHTML = actualGame

for (let i = 0; i < 9; i++) {
    document.getElementById(`p${i}`).addEventListener('click', mark);
}


//Adds new game
function newGame(e) {
    e.preventDefault();
    let title = document.getElementById('title').value;



    if (title != '') {

        //Clear the board
        for (let i = 0; i < 9; i++) {
            document.getElementById(`p${i}`).innerHTML = '-';
        }


        fetch('http://localhost:5000/games', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({ name: title, status: "new", winner: "none" })
            }).then((res) => res.json())
            .then((data) => {
                showGames();
                console.log(data['id']);
                actualGame = data['id'];
                document.getElementById('actual').innerHTML = actualGame
                gameStatus = "Ongoing";
                document.getElementById('status').innerHTML = gameStatus;
            }).catch(error => console.log('Error adding new game: ', error));
    }
}




//Prints all the games
function showGames() {

    fetch('http://127.0.0.1:5000/games', {
            method: 'GET'
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            let output = '<h2>Games</h2>'
            data.forEach((game) => {
                output += `
                    <ul>
                        <li>ID: ${game.id}</li>
                        <li>NAME: ${game.name}</li>
                        <li>STATUS: ${game.status}</li>
                        <li>WINNER: ${game.winner}
                        <li><button onclick="resumeGame(${game.id})" id=${game.id}>Resume</button></li>
                    </ul>
                `;
            });
            document.getElementById('games').innerHTML = output;
        })
}

//Funcion for click event
//Prints move on board, sends it to the server and receives next move
function mark(event) {

    //Check if the place is empty
    if (event.target.innerHTML === "-" && gameStatus != "Finished" /*&& gameStatus == "Ongoing"*/ ) {

        event.target.innerHTML = "X";
        //console.log(event.target.id);
        let id_place = event.target.id[1];
        let move_string = "";

        for (let i = 0; i < 9; i++) {
            if (i == id_place) {
                move_string += '1';
            } else {
                move_string += '0';
            }
        }
        //console.log(move_string);

        //console.log(JSON.stringify({ move: "000000100" }));

        //Send the move as Json and receive next move from server
        //fetch('http://127.0.0.1:5000/games/1/moves', {
        fetch(`http://127.0.0.1:5000/games/${actualGame}/moves`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({ move: move_string })
            })
            .then((res) => res.json())
            .then((data) => {

                console.log(data);
                if (data['moves']) {

                    for (let i = 0; i < 9; i++) {
                        if (data['moves'][i] == '2') {
                            //console.log(i);
                            //Print move on board
                            document.getElementById(`p${i}`).innerHTML = "O";
                        }
                    }
                } else if (data['Message']) {
                    if (data['lastMove']) {
                        for (let i = 0; i < 9; i++) {
                            if (data['lastMove'][i] == '2') {
                                document.getElementById(`p${i}`).innerHTML = "O";
                            }
                        }
                    }
                    showGames()
                    document.getElementById('result').innerHTML = data['Message'];
                    gameStatus = "Finished";
                    document.getElementById('status').innerHTML = gameStatus;
                }
            }).catch(error => console.log('Error adding new move: ', error));;
    }
}


//Delete all the moves and start again
function reset() {

    //Reset moves
    for (let i = 0; i < 9; i++) {
        document.getElementById(`p${i}`).innerHTML = "-";
    }

    //Reset result
    document.getElementById('result').innerHTML = '';

    //Send delete to delete from database
    fetch(`http://127.0.0.1:5000/games/${actualGame}/moves`, {
            method: 'DELETE'
        }).then((res) => res.json())
        .then((data) => {
            console.log("Moves Deleted")
            console.log(data);
        }).catch(error => console.log('Error deleting move: ', error));

}


//Resume Game
function resumeGame(game_id) {
    console.log(game_id);
    fetch(`http://127.0.0.1:5000/games/${game_id}/moves`, {
            method: 'GET'
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);


            for (let i = 0; i < 9; i++) {
                if (data['lastMove'][i] == '1') {
                    //Print move on board
                    document.getElementById(`p${i}`).innerHTML = "X";
                } else if (data['lastMove'][i] == '2') {
                    document.getElementById(`p${i}`).innerHTML = "O";
                } else {
                    document.getElementById(`p${i}`).innerHTML = "-";
                }
            }

            actualGame = data['id'];
            gameStatus = data['status'];
            document.getElementById('status').innerHTML = gameStatus;
            document.getElementById('actual').innerHTML = actualGame
            document.getElementById('result').innerHTML = data['winner'];


        }).catch(error => console.log('Error resuming game: ', error));;

}