const express = require("express");
const WebSocket = require("ws");
const app = express();
const serverPort = process.argv[2] || 3000;
const webSocketPort = 8080;
const wss = new WebSocket.Server({ port: webSocketPort });

const subscribers = [];
const publishers = [];
const topics = {};
let userID = 0;

app.use(express.json());

app.post("/subscriber", (req, res) => {
  subscribers[userID] = {
    session: "",
  };
  userID++;
  res.json({
    id: userID - 1,
    type: 0,
    socketPort: webSocketPort,
  });
});

app.post("/publisher", (req, res) => {
  publishers[userID] = {
    session: "",
  };
  userID++;

  res.json({
    id: userID - 1,
    type: 1,
    socketPort: webSocketPort,
  });
});

wss.on("connection", (ws) => {
  console.log("client connected");
  ws.on("message", (message) => {
    const body = JSON.parse(message.toString());
    if (body.conf === 1) {
      //this is configuration

      if (body.auth.type === 0) {
        subscribers[body.auth.id].session = ws;
        console.log("subscriber configured");
      }
    } else if (body.conf === 0) {
      //this is message pass
      if (body.auth.type === 1) {
        subscribers.forEach((subscriber) => {
          subscriber.session.send(body.message);
        });
      }
    } else {
      console.log("wrong message type");
    }
  });
});

app.listen(serverPort, () => {
  console.log(`Server running on port ${serverPort}`);
});
