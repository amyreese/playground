$(document).ready(function() {
	var websocket = new WebSocket("ws://localhost:9000/");

	websocket.onmessage = function(event) {
		console.log("Message received: " + event.data);
	}

	websocket.onopen = function(event) {
		console.log("Connection open: " + event.data);
		websocket.send("test message");
	}
});
