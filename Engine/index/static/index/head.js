import {element} from '../../../static/helper.js';

window.onclick = event => {
  if (!event.target.id) return;

  const notToggledNotification = !['notification-toggle', 'notification-dark', 'notification-icon'].includes(event.target.id);

  // Hides alerts list if not toggled
  if (event.target.id !== 'main-content-rooms-chat-bottom-right-reminder') {
    const alertsList = element('#main-content-rooms-chat-bottom-right-alerts');

    if (alertsList) {
      alertsList.classList.remove('active');
    }
  }

  // hides notifications if not toggled
  if (notToggledNotification) {
    const notificationList = element('#notification-list');
    if (notificationList) notificationList.classList.remove('active');
  }
};
