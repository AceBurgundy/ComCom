import {element} from '../../../static/helper.js';
import {socket} from '../../../static/socket.js';

const toggle = element('#main-content-rooms-chat-bottom-right-reminder');
const alerts = element('#main-content-rooms-chat-bottom-right-alerts');
const chatList = element('#main-content-rooms-chat-center-right');

toggle.onclick = () => alerts.classList.toggle('active');

const createMessage = message => chatList.innerHTML = /* html */`<li>${message}</li>` + chatList.innerHTML;

alerts.onclick = event => {
  const roomCode = event.target.parentElement.dataset.roomCode;
  const message = event.target.innerHTML;

  socket.emit('new-alert', {
    roomCode,
    message
  });
};

socket.on('alert', message => createMessage(message));
