const url = require('url');
const express = require('express');
const bodyParser = require('body-parser');
const Pusher = require("pusher");
const mysql = require('mysql2/promise');

const pusher = new Pusher({
  appId: "1567075",
  key: "0274fca38b4154a8b349",
  secret: "f32b7d250a91403f7c8b",
  cluster: "eu",
  useTLS: true
});

const app = express();

app.use(express.json());
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

const config = {
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'ResellrMessages'
  };

// define userId (while no auth is implemented)
const user = 2;

// GET - responds with the list of conversation of a specific user, defined above
app.get('/messages', async (req, res) => {
    const filteredConvTable = {};

    const connection = await mysql.createConnection(config);

    const sql = 'SELECT * FROM ConvTable WHERE userId1 = ' + user + ' OR userId2 = ' + user;
    const [rows, fields] = await connection.execute(sql);

    for (let i = 0; i < rows.length; i++) {
        const convInfo = rows[i];
        if(convInfo.userId1 == user){
            if(!convInfo.userHidden1){
                newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId2;
                newConvInfo.otherUserName = convInfo.userName2;
                newConvInfo.otherUserPicture = convInfo.userPicture2;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convInfo.id] = newConvInfo;
            }
        }

        else if(convInfo.userId2 == user){
            if(!convInfo.userHidden2){
                newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId1;
                newConvInfo.otherUserName = convInfo.userName1;
                newConvInfo.otherUserPicture = convInfo.userPicture1;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convInfo.id] = newConvInfo;
            }
        }
    }

    res.render('index', {filteredConvTable: filteredConvTable});
});

// GET - responds with the list of messages of a specific conversation
app.get('/messages/:conversationId', async (req, res) => {
    const conversationId = parseInt(req.params.conversationId);
    const filteredMsgTable = {};

    const connection = await mysql.createConnection(config);

    const sql = 'SELECT * FROM MsgTable WHERE conversationId = ' + conversationId;
    const [rows, fields] = await connection.execute(sql);

    for (let i = 0; i < rows.length; i++) {
        const msgInfo = rows[i];
        newMsgInfo = {};
        newMsgInfo.senderId = msgInfo.senderId;
        newMsgInfo.timestamp = msgInfo.timestamp;
        newMsgInfo.read = msgInfo.read;
        newMsgInfo.content = msgInfo.content;
        filteredMsgTable[msgInfo.id] = newMsgInfo;
    }

    keys = Object.keys(filteredMsgTable);
    for(i = 1; i < keys.length; i++){
        if(keys[i] < keys[i-1]){
            temp = keys[i];
            keys[i] = keys[i-1];
            keys[i-1] = temp;
        }
    }
    
    res.render('conv', {conversationId: conversationId, filteredMsgTable: filteredMsgTable});
});

// POST - takes a message and sends it using Pusher
app.post('/messages/:conversationId', async (req, res) => {

    channelName = "chat"+req.params.conversationId;
    
    await pusher.trigger(channelName, "message", {
        msg: req.body.message
      });

    res.sendStatus(200);
});

// Start server
app.listen(3000, () => {
    console.log('Server started on port 3000');
});
