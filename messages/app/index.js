const url = require('url');
const express = require('express');
const bodyParser = require('body-parser');
const Pusher = require("pusher");
const mariadb = require('mariadb/promise');
const moment = require('moment');
const { connect } = require('http2');

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
const pool = mariadb.createPool({
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'ResellrMessages'
  });

// define userId (while no auth is implemented)
const userNames = ['João Ferreira', 'José Silva', 'Amélia Rodrigues'];
const numSysUsers = 3;
const user = 2;

// GET - responds with the list of conversation of a specific user, defined above
app.get('/messages', async (req, res) => {
    // create database connection
    const connection = await pool.getConnection();

    const filteredConvTable = await filterConvTable(connection);

    connection.end();

    res.render('conv', {currentUserId: user, conversationId: -1, filteredConvTable: filteredConvTable});
});

// POST - adds a new conversation to the database
app.post('/messages', async (req, res) => {
    
    // create database connection
    const connection = await pool.getConnection();

    const otherUserId = Math.floor(1 + Math.random()*(numSysUsers));

    // check if conversation already exists
    var sql = 'SELECT * FROM ConvTable WHERE ( userId1 = ' + user + ' AND userId2 = ' + otherUserId + ' ) '
                                        + 'OR ( userId1 = ' + otherUserId + ' AND userId2 = ' + user + ' )';
    var rows = await connection.query(sql);
    if(rows.length > 0){
        const conversationId = rows[0].id;
        res.redirect('/messages/' + conversationId);
    }
    // if it doesn't, then
    else{
        // add the message to the database
        const convData = {
            userId1: user,
            userName1: userNames[user-1],
            userHidden1: false,
            userId2: otherUserId,
            userName2: userNames[otherUserId-1],
            userHidden2: false,
            lastMessage: null,
        }

        await connection.query('INSERT INTO ConvTable (userId1, userName1, userHidden1, userId2, userName2, userHidden2, lastMessage) VALUES (?, ?, ?, ?, ?, ?, ?)',
                [convData.userId1, convData.userName1, convData.userHidden1, convData.userId2, convData.userName2, convData.userHidden2, convData.lastMessage]);
        
        // get the conversation to get its automatically created id
        var sql = 'SELECT * FROM ConvTable WHERE userId1 = ' + user + ' AND userId2 = ' + otherUserId;
        var rows = await connection.query(sql);

        connection.end();

        // check for any errors during creation
        if(rows.length == 0){
            res.redirect('/messages');
        }
        // if not, redirect to newly created conversation
        else{
            const conversationId = rows[0].id;
            res.redirect('/messages/' + conversationId);
        }
    }
});

// GET - responds with the list of messages of a specific conversation
app.get('/messages/:conversationId', async (req, res) => {
    // create database connection
    const connection = await pool.getConnection();

    // get the Id of the conversation the user is trying to access
    const conversationId = parseInt(req.params.conversationId);

    // get the conversation the user is trying to access
    var sql = 'SELECT * FROM ConvTable WHERE id = ' + conversationId;
    var rows = await connection.query(sql);

    // check if it is an existing conversation
    if(rows.length == 0){
        connection.end();
        res.redirect('/messages');
    }
    // if so, check if the current user has access to it
    else if(rows[0].userId1 != user && rows[0].userId2 != user){
        connection.end();
        res.redirect('/messages');
    }
    // if so, check if the user doesnt have this conversation hidden
    else if((rows[0].userId1 == user && rows[0].userHidden1 == true) ||
                    (rows[0].userId2 == user && rows[0].userHidden2 == true)){
        connection.end();
        res.redirect('/messages');         
    }
    // if so, render the page
    else{
        const filteredConvTable = await filterConvTable(connection);        
        const filteredMsgTable = await filterMsgTable(connection, conversationId);
        connection.end();

        res.render('conv', {currentUserId: user, conversationId: conversationId, 
                                filteredConvTable: filteredConvTable, filteredMsgTable: filteredMsgTable});
    }
});

// POST - takes a message ,sends it using Pusher and adds it to the database
app.post('/messages/:conversationId', async (req, res) => {
    
    channelName = "chat"+req.params.conversationId;
    
    await pusher.trigger(channelName, "message", {
        userId: user,
        msg: req.body.message
      });
    
    // create database connection
    const connection = await pool.getConnection();

    // add the message to the database
    const msgData = {
        conversationId: parseInt(req.params.conversationId),
        senderId: user,
        timestamp: moment().format('YYYY-MM-DD HH:mm:ss'),
        content: req.body.message,
    }

    // UNCOMMENT THIS TO MAKE INSERTS INTO DATABASE
    //await connection.query('INSERT INTO MsgTable (conversationId, senderId, timestamp, content) VALUES (?, ?, ?, ?)',
    //                                    [msgData.conversationId, msgData.senderId, msgData.timestamp, msgData.content]);
    
    connection.end();

    res.sendStatus(200);
});

// DELETE - deletes a conversation (hides it from a user's view)
app.delete('/messages/:conversationId', async (req, res) => {

    const conversationId = parseInt(req.body.conversationId);

    // create database connection
    const connection = await pool.getConnection();
    
    // get the conversation the user is trying to access
    var sql = 'SELECT * FROM ConvTable WHERE id = ' + conversationId;
    var rows = await connection.query(sql);

    // check if it is an existing conversation
    if(rows.length == 0){
        connection.end();
        res.redirect('/messages');
    }
    // if so, check if the current user has access to it
    else if(rows[0].userId1 != user && rows[0].userId2 != user){
        connection.end();
        res.redirect('/messages');
    }
    // if so, delete the conversation (hide it for this user's view)
    else{
        const convInfo = rows[0];
        if(convInfo.userId1 == user){
            await connection.query('UPDATE ConvTable SET userHidden1 = true WHERE id = ?', [conversationId]);
        }
        else if(convInfo.userId2 == user){
            await connection.query('UPDATE ConvTable SET userHidden2 = true WHERE id = ?', [conversationId]);
        }
        connection.end();
        res.redirect('/messages');
    }
});

async function filterConvTable(connection){
    // get all conversations our user participates in
    const sql = 'SELECT * FROM ConvTable WHERE userId1 = ' + user + ' OR userId2 = ' + user;
    const rows = await connection.query(sql);

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
    const rows = await connection.query(sql);

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
