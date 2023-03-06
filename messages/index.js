const url = require('url');
const express = require('express');
const app = express();

// define userId (while no auth is implemented)
const user = 2;

// conversation table in the database
const ConvTable = {
    1:{
        userId1 : 1,
        userName1 : 'João Ferreira',
        userPicture1 : 'NA',
        userHidden1 : false,
        userId2 : 2,
        userName2 : 'José Silva',
        userPicture2 : 'NA',
        userHidden2 : false,
        lastMessage : "Claro que sim!"
    },
    2:{ userId1 : 3,
        userName1 : 'Amélia Rodrigues',
        userPicture1 : 'NA',
        userHidden1 : false,
        userId2 : 1,
        userName2 : 'João Ferreira',
        userPicture2 : 'NA',
        userHidden2 : true,
        lastMessage : "Até breve!"
    },
    3:{
        userId1 : 2,
        userName1 : 'José Silva',
        userPicture1 : 'NA',
        userHidden1 : false,
        userId2 : 3,
        userName2 : 'Amélia Rodrigues',
        userPicture2 : 'NA',
        userHidden2 : false,
        lastMessage : "Como está?"
    }
}

// message table in the database
const MsgTable = {
    1:{
        conversationId: 1,
        senderId: 1,
        timestamp: "2023-02-27T10:30:00.000Z",
        read: true,
        content: "Bom dia, tudo bem?"
    },
    2:{
        conversationId: 1,
        senderId: 1,
        timestamp: "2023-02-27T11:05:00.000Z",
        read: true,
        content: "Estaria disposto a negociar o preço do artigo?"
    },
    3:{
        conversationId: 1,
        senderId: 2,
        timestamp: "2023-02-27T11:15:00.000Z",
        read: false,
        content: "Claro que sim!"
    },
    4:{
        conversationId: 2,
        senderId: 3,
        timestamp: "2023-03-04T14:50:00.000Z",
        read: true,
        content: "Boa tarde, estou interessado neste artigo!"
    },
    5:{
        conversationId: 2,
        senderId: 1,
        timestamp: "2023-03-04T14:57:00.000Z",
        read: true,
        content: "Ainda bem! Será possível discutir noutro local?"
    },
    6:{
        conversationId: 2,
        senderId: 3,
        timestamp: "2023-03-04T15:20:00.000Z",
        read: true,
        content: "Até breve!"
    },
    8:{
        conversationId: 3,
        senderId: 2,
        timestamp: "2023-03-05T17:30:00.000Z",
        read: false,
        content: "Boa tarde, o meu nome é José Silva."
    },
    9:{
        conversationId: 3,
        senderId: 2,
        timestamp: "2023-03-05T18:20:00.000Z",
        read: false,
        content: "Como está?"
    }
}

// GET - responds with the list of conversation of a specific user, defined above
app.get('/messages', (req, res) => {
    const filteredConvTable = {};
    Object.entries(ConvTable).forEach(([convId, convInfo]) => {

        if(convInfo.userId1 == user){
            if(!convInfo.userHidden1){
                newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId2;
                newConvInfo.otherUserName = convInfo.userName2;
                newConvInfo.otherUserPicture = convInfo.userPicture2;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convId] = newConvInfo;
            }
        }

        else if(convInfo.userId2 == user){
            if(!convInfo.userHidden2){
                newConvInfo = {}
                newConvInfo.otherUserId = convInfo.userId1;
                newConvInfo.otherUserName = convInfo.userName1;
                newConvInfo.otherUserPicture = convInfo.userPicture1;
                newConvInfo.lastMessage = convInfo.lastMessage;
                filteredConvTable[convId] = newConvInfo;
            }
        }

    });
    res.send(filteredConvTable);
});

// GET - responds with the list of messages of a specific conversation
app.get('/messages/:conversationId', (req, res) => {
    const conversationId = parseInt(req.params.conversationId);
    const filteredMsgTable = {};
    Object.entries(MsgTable).forEach(([msgId, msgInfo]) => {

        if(msgInfo.conversationId == conversationId){
            newMsgInfo = {};
            newMsgInfo.senderId = msgInfo.senderId;
            newMsgInfo.timestamp = msgInfo.timestamp;
            newMsgInfo.read = msgInfo.read;
            newMsgInfo.content = msgInfo.content;
            filteredMsgTable[msgId] = newMsgInfo;
        }

    });
    
    keys = Object.keys(filteredMsgTable);
    for(i = 1; i < keys.length; i++){
        if(keys[i] < keys[i-1]){
            temp = keys[i];
            keys[i] = keys[i-1];
            keys[i-1] = temp;
        }
    }
    res.send(filteredMsgTable);
});

// Start server
app.listen(3000, () => {
    console.log('Server started on port 3000');
});
