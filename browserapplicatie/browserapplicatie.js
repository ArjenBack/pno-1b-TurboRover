let socket = undefined;

    function connect_socket() {
        // Close any existing sockets
        disconnect_socket();

        socket = new WebSocket("ws://192.168.4.1:80/connect-websocket");

        // Connection opened
        socket.addEventListener("open", (event) => {
            document.getElementById("status").textContent = "Status: Connected";
        });

        socket.addEventListener("close", (event) => {
            socket = undefined;
            document.getElementById("status").textContent = "Status: Disconnected";
        });

        socket.addEventListener("message", (event) => {
            console.log(event.data)
        });

        socket.addEventListener("error", (event) => {
            socket = undefined;
            document.getElementById("status").textContent = "Status: Disconnected";
        });
    }

    function disconnect_socket() {
        if(socket != undefined) {
            socket.close();
        }
    }

    function sendCommand(command) {
        if(socket != undefined) {
            socket.send(command)
        } else {
            alert("Not connected to the PICO")
        }
    }



const startingMinutes = 5
let time = startingMinutes * 60

const countdownEl =  document.getElementById('countdown')
let timerInterval;
function updateCountdown() {
    const minutes = Math.floor(time/60);
    let seconds = time % 60;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    countdownEl.innerHTML = `${minutes}: ${seconds}`;
    if (time > 0) {
        time--;
    } else {
        clearInterval(timerInterval); // Stop at 0
        countdownEl.innerHTML = "Time's Up!";
    }
}

function startTimer() {
    if (!timerInterval) { // Prevent multiple intervals
        timerInterval = setInterval(updateCountdown, 1000);
    }
}

function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null; // Reset interval variable
}

function resetTimer() {
    stopTimer();
    time = startingMinutes * 60; // Reset time
    countdownEl.innerHTML = "5:00"; // Reset display
}