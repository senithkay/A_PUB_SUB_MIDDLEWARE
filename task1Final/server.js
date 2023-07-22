const express = require("express");
const WebSocket = require("ws");
const app = express();
const serverPort = 3000;
const webSocketPort = process.argv[2] || 8080;
const wss = new WebSocket.Server({ port: webSocketPort });

const users = [];
app.use(express.json());

wss.on("connection", (ws) => {
  users.push(ws);
  ws.on("message", (message) => {
    console.log(JSON.parse(message)["message"]);
  });
});

app.listen(serverPort, () => {
  console.log(`Server running on port ${webSocketPort}`);
});
