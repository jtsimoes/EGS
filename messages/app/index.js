const url = require('url');
const express = require('express');
const bodyParser = require('body-parser');
const Pusher = require("pusher");
const mysql = require('mysql2/promise');

// pusher configs
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

// database connection config
const config = {
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'ResellrMessages'
  };

// define userId (while no auth is implemented)
const user = 3;

// GET - responds with the list of conversation of a specific user, defined above
app.get('/messages', async (req, res) => {
    // create database connection
    const connection = await mysql.createConnection(config);

    const filteredConvTable = await filterConvTable(connection);

    res.render('conv', {currentUserId: user, conversationId: -1, filteredConvTable: filteredConvTable});
});

// GET - responds with the list of messages of a specific conversation
app.get('/messages/:conversationId', async (req, res) => {
    // create database connection
    const connection = await mysql.createConnection(config);

    // get the Id of the conversation the user is trying to access
    const conversationId = parseInt(req.params.conversationId);

    // get the conversation the user is trying to access
    var sql = 'SELECT * FROM ConvTable WHERE id = ' + conversationId;
    var [rows, fields] = await connection.execute(sql);

    // check if it is an existing conversation
    if(rows.length == 0) res.redirect('/messages');

    // if so, check if the current user has access to it
    else if(rows[0].userId1 != user && rows[0].userId2 != user) res.redirect('/messages');

    // if so, render the page
    else{

        const filteredConvTable = await filterConvTable(connection);        
        const filteredMsgTable = await filterMsgTable(connection, conversationId);

        res.render('conv', {currentUserId: user, conversationId: conversationId, 
                                filteredConvTable: filteredConvTable, filteredMsgTable: filteredMsgTable});
    }
});

// POST - takes a message and sends it using Pusher
app.post('/messages/:conversationId', async (req, res) => {

    channelName = "chat"+req.params.conversationId;
    
    await pusher.trigger(channelName, "message", {
        userId: user,
        msg: req.body.message
      });

    res.sendStatus(200);
});

async function filterConvTable(connection){
    // get all conversations our user participates in
    const sql = 'SELECT * FROM ConvTable WHERE userId1 = ' + user + ' OR userId2 = ' + user;
    const [rows, fields] = await connection.execute(sql);

    // filter the result
    const filteredConvTable = {};
    
    for (let i = 0; i < rows.length; i++) {
        const convInfo = rows[i];
        if(convInfo.userId1 == user){
            if(!convInfo.userHidden1){
                var newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId2;
                newConvInfo.otherUserName = convInfo.userName2;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convInfo.id] = newConvInfo;
            }
        }

        else if(convInfo.userId2 == user){
            if(!convInfo.userHidden2){
                var newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId1;
                newConvInfo.otherUserName = convInfo.userName1;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convInfo.id] = newConvInfo;
            }
        }
    }

    return filteredConvTable;
}

async function filterMsgTable(connection, conversationId){
    // get all messages from the conversation the user is trying to access
    const sql = 'SELECT * FROM MsgTable WHERE conversationId = ' + conversationId;
    const [rows, fields] = await connection.execute(sql);

    // filter the result
    const filteredMsgTable = {};

    for (let i = 0; i < rows.length; i++) {
        const msgInfo = rows[i];
        var newMsgInfo = {};
        newMsgInfo.senderId = msgInfo.senderId;
        newMsgInfo.timestamp = msgInfo.timestamp;
        newMsgInfo.read = msgInfo.read;
        newMsgInfo.content = msgInfo.content;
        filteredMsgTable[msgInfo.id] = newMsgInfo;
    }

    // order it
    keys = Object.keys(filteredMsgTable);
    for(i = 1; i < keys.length; i++){
        if(keys[i] < keys[i-1]){
            temp = keys[i];
            keys[i] = keys[i-1];
            keys[i-1] = temp;
        }
    }

    return filteredMsgTable;
}

// Start server
app.listen(3000, () => {
    console.log('Server started on port 3000');
});
