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

var userId = document.getElementById('userid').getAttribute("value");

channel.bind('message', function(data) {
  // Update the UI with the new message

  const message = data.msg;

  const user = data.userId;

  // Get the chat window element
  const chatWindow = document.getElementById('chatbox');

  var messageElement;
  if(user == userId){
    messageElement = receiverMessage(message);
  }
  else{
    messageElement = senderMessage(message);
  }

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

// ------------------------------------
//this script is listening to the form and posts to /messages without the need for page reloading
// ------------------------------------

const deleteForm = document.getElementById('delete-conv');
deleteForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const url = deleteForm.getAttribute('action');
  fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({conversationId: convId})
  })
  .then(response => {
    if(response.ok) {
      console.log('Delete request successful');
    } else {
      console.log('Delete request failed');
    }
    window.location.href = '/messages';
  })
  .catch(error => {
    console.log('Error:', error);
  });
});

// create a receiver message HTML element
function receiverMessage(msg){
  // create the outer div element
  const messageElement = document.createElement('div');
  messageElement.classList.add('media', 'w-50', 'ml-auto', 'mb-3');

  // create the first inner div element
  const innerDiv1 = document.createElement('div');
  innerDiv1.classList.add('media-body');

  // create the second inner div element
  const innerDiv2 = document.createElement('div');
  innerDiv2.classList.add('bg-primary', 'rounded', 'py-2', 'px-3', 'mb-2');

  // create the paragraph element inside the second inner div
  const pElement = document.createElement('p');
  pElement.classList.add('text-small', 'mb-0', 'text-white');
  pElement.textContent = msg;

  // append the paragraph element to the second inner div
  innerDiv2.appendChild(pElement);

  // create the second paragraph element inside the media-body div
  const pElement2 = document.createElement('p');
  pElement2.classList.add('small', 'text-muted');
  pElement2.textContent = '12:00 PM | Aug 13';

  // append the second inner div and the second paragraph element to the media-body div
  innerDiv1.appendChild(innerDiv2);
  innerDiv1.appendChild(pElement2);

  // append the media-body div to the outer div
  messageElement.appendChild(innerDiv1);

  return messageElement;
}

// create a sender message HTML element
function senderMessage(msg){
  // create the outer div element
  const messageElement = document.createElement('div');
  messageElement.classList.add('media', 'w-50', 'mb-3');

  // create the image element
  let img = document.createElement("img");
  img.src = "https://bootstrapious.com/i/snippets/sn-chat/avatar.svg";
  img.alt = "user";
  img.width = "50";
  img.classList.add("rounded-circle");

  // create the first inner div element
  const innerDiv1 = document.createElement('div');
  innerDiv1.classList.add('media-body', 'ml-3');

  // create the second inner div element
  const innerDiv2 = document.createElement('div');
  innerDiv2.classList.add('bg-light', 'rounded', 'py-2', 'px-3', 'mb-2');

  // create the paragraph element inside the second inner div
  const pElement1 = document.createElement('p');
  pElement1.classList.add('text-small', 'mb-0', 'text-muted');

  // append the paragraph element to the second inner div
  innerDiv2.appendChild(pElement1);

  // create the paragraph element inside the first inner div
  // create the paragraph element inside the second inner div
  const pElement2 = document.createElement('p');
  pElement2.classList.add('small', 'text-muted');
  pElement2.textContent = msg;

  // append the second inner div and the second paragraph element to the media-body div
  innerDiv1.appendChild(innerDiv2);
  innerDiv1.appendChild(pElement2)

  // append the media-body div to the outer div
  messageElement.appendChild(img);
  messageElement.appendChild(innerDiv1);

  return messageElement;
}