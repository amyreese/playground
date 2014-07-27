$(document).ready(function() {
	var websocket = new WebSocket("ws://localhost:9000");

	websocket.onopen = function(event) {
		console.log("Connection open: " + event.data);
		websocket.send("test message");
	}

	websocket.onclose = function(event) {
		console.log("Connection closed");
	}

	websocket.onerror = function(event) {
		console.error("Error: " + event.data);
	}

	websocket.onmessage = function(event) {
		console.log("Message received: " + event.data);
	}

	var heartbeat = function() {
		websocket.send("heartbeat");
	}
	setInterval(heartbeat, 5000);

});
