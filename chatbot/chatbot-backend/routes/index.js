//from https://github.com/tyleroneil72/chat-bot/blob/main/backend/routes/index.js
// routes/index.js
const express = require("express");
const { handleMessage } = require("./messageController");

const router = express.Router();

router.post("/message", handleMessage);

module.exports = router;
