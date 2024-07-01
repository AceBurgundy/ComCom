import makeToastNotification, {element, isCurrentUser} from '../../../static/helper.js';
import {socket} from '../../../static/socket.js';

const chatList = element('#main-content-rooms-chat-center');
const sendButton = element('#main-content-rooms-chat-bottom-right-input-send');
const messageInput = element('#main-content-rooms-chat-bottom-right-input');

/**
 * Inserts new message template into the chat list
 * @param {object} messageObject - received from flask socket-io 'received-message' route
 * @param {Integer} messageObject.senderId - The id of the sender
 * @param {Integer} messageObject.senderUsername - The username of the sender
 * @param {String} messageObject.text - The content of the message
 * @returns {Promise<void>}
 */
async function createMessage(messageObject) {
  const isSender = await isCurrentUser(messageObject.senderId);
  let newMessage = /* html */`
  <tr class="main-content-room-chat-center__row sender">
    <td class="main-content-room-chat-center__row__left"></td>
    <td class="main-content-room-chat-center__row__right">
        <p class="main-content-room-chat-center__row__right__sender">${ messageObject.senderUsername }</p>
        <p class="main-content-room-chat-center__row__right__text">${ messageObject.text }</p>
    </td>
  </tr>`;

  if (!isSender) {
    newMessage = /* html */`
      <tr class="main-content-room-chat-center__row sender">
        <td class="main-content-room-chat-center__row__left">
          <p class="main-content-room-chat-center__row__left__sender">${ messageObject.senderUsername }</p>
          <p class="main-content-room-chat-center__row__left__text">${ messageObject.text }</p>
        </td>
        <td class="main-content-room-chat-center__row__right"></td>
      </tr>`;
    }
  ;

  chatList.innerHTML = chatList.innerHTML + newMessage;
  messageInput.value = '';
};

// Handles sending messages back to the server
function sendMessage() {
  const message = messageInput.value.trim();

  if (message === '') {
    makeToastNotification('Message cannot be empty');
    return;
  }

  const roomCode = sendButton.dataset.roomCode;

  socket.emit('send-message', {
    roomCode,
    message
  });
}

// Sent using send button
sendButton.onclick = () => sendMessage();

// Sent using enter button
messageInput.onkeyup = event => {
  if (event.key != 'Enter') {
    return;
  }

  sendMessage();
};

// Displays message
socket.on('received-message', async message => await createMessage(message));
