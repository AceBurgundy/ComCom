import {allowedToFetch, isLoggedIn} from '../../../static/helper.js';
import {socket} from '../../../static/socket.js';
import {updateNotifications} from './notification.js';

socket.on('connect', async () => {
  console.log('socket started');
  const allowed = allowedToFetch();
  const loggedIn = await isLoggedIn();

  if (allowed && loggedIn) {
    await updateNotifications();
  }
});

socket.on('update_notification', async () => {
  const loggedIn = await isLoggedIn();

  if (loggedIn) {
    await updateNotifications();
  }
});
