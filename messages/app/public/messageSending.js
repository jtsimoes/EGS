// ------------------------------------
// this script is listening to the pusher channel to update the interface with the message contents
// ------------------------------------

// Enable pusher logging
Pusher.logToConsole = true;

var pusher = new Pusher('0274fca38b4154a8b349', {
  cluster: 'eu'
});

var convId = document.getElementById('chatbox').getAttribute("value");
var channelName = 'chat' + convId;
var channel = pusher.subscribe(channelName);

channel.bind('message', function(data) {
  // Update the UI with the new message
  const message = data.msg;

  // Get the chat window element
  const chatWindow = document.getElementById('chatbox');

  // Create a new message element
  const messageElement = document.createElement('p');
  messageElement.textContent = message;
  messageElement.classList.add('message');

  // Append the message element to the chat window
  chatWindow.appendChild(messageElement);

  // Scroll to the bottom of the chat window
  chatWindow.scrollTop = chatWindow.scrollHeight;
});
  
// ------------------------------------
//this script is listening to the form and posts to /messages without the need for page reloading
// ------------------------------------

const form = document.getElementById('message-form');
const chatbox = document.getElementById('chatbox');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const messageInput = document.getElementById('message-input');
  const message = messageInput.value;

  // Send a POST request to the server with the message data
  var convId = document.getElementById('chatbox').getAttribute("value");
  var path = '/messages/' + convId;
  fetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message
    })
  })
  .then(response => {
    if (response.ok) {
      console.log('Message sent successfully');
    } else {
      console.error('Error sending message');
    }
  })
  .catch(error => {
    console.error('Error sending message', error);
  });

  // Clear the message input field
  messageInput.value = '';
});
