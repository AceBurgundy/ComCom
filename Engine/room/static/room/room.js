import makeToastNotification, {isLoggedIn} from '../../../static/helper.js';
import {socket} from '../../../static/socket.js';

window.onload = async () => {
  const loggedIn = await isLoggedIn();
  const path = window.location.pathname.substring(1).split('/');
  /**
     * path must look something like this to proceed
     * [room, <str: room_code>, open]
     */
  const inRoom = path[0] === 'room' && path[2] === 'open';

  if (!loggedIn || !inRoom) {
    return;
  }

  socket.emit('join', {
    room: path[1]
  });

  socket.on('left', message => makeToastNotification(message));
  socket.on('joined', message => makeToastNotification(message));
};

socket.on('message', message => makeToastNotification(message));
