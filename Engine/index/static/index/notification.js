import makeToastNotification, {element, triggerWhenElementExist, triggerWhenElementsExist} from '../../../static/helper.js';

const notificationList = element('#notification-list');

triggerWhenElementsExist([
  '#notification-toggle',
  '#notification-list-close',
  '#notification-dark',
  '#notification-icon'
], 'click', () => {
  notificationList.classList.toggle('active');
});

/**
 * Asynchronously fetches notifications from the server and logs them to the console.
 * If an error occurs during the fetch operation, it logs the error to the console.
 *
 * Summary
 * - Fetch notifications from the server.
 * - Convert the response to JSON.
 * - Select the current list of notifications on the client.
 * - Compare the IDs of current notifications with the new ones received from the server.
 * - Remove notifications from the client that no longer exist on the server.
 * - Add new notifications to the client that are not already displayed.
 * - Handle any potential errors during this process.
 *
 * @async
 * @function updateNotifications
 * @return {Promise<void>} A promise that resolves when the notifications have been fetched and logged, or rejects if an error occurs.
 */
export const updateNotifications = async () => {
  fetch('/notifications')
      .then(response => response.json())
      .then(newNotificationObjects => {
        const notificationParentElement = element('#notification-list');
        const notificationParentElementIds = Array.from(notificationParentElement.children).map(item => item.dataset.id);
        const newNotificationObjectsIds = Array.from(newNotificationObjects).map(notification => notification.id);

        const removedNotificationsIds = [];

        // Removes newNotificationObjects already removed from database but still in the client side
        Array.from(notificationParentElement.children).forEach(notificationElement => {
          const id = notificationElement.dataset.id;
          const idInNewNotifications = newNotificationObjectsIds.includes(id);

          if (idInNewNotifications) {
            return;
          }

          notificationElement.remove();
          removedNotificationsIds.push(id);
        });

        // The filtered version of notificationParentElementIds which doesn't contain elements removed from the previous loop
        const filteredNotificationParentElementIds = notificationParentElementIds.filter(id => !removedNotificationsIds.includes(id));

        // Adds the new notification only if that notification doesn't currently exist
        newNotificationObjects.forEach(notification => {
          const notificationExists = filteredNotificationParentElementIds.includes(notification.id);

          if (!notificationExists) {
            notificationParentElement.innerHTML += makeNewNotification(notification);
          }
        });
      })
      .catch(error => {
        console.log(error);
      });
};

/**
 * Creates an HTML string for a new notification list item.
 * Depending on the type of the notification, it includes either confirmation buttons or a message.
 *
 * @function makeNewNotification
 * @param {object} notification - The notification object.
 * @param {string} notification.id - The id of the notification.
 * @param {string} notification.title - The title of the notification.
 * @param {string} notification.message - The message content of the notification.
 * @param {string} notification.type - The type of the notification. If the type is 'Confirm', confirmation buttons are included.
 * @param {string} notification.roomId - The id of the room the notification is for.
 * @return {string} An HTML string representing the notification list item.
 */
export const makeNewNotification = notification => {
  return /* html */`
    <li class="notification-list__item" data-id="${notification.id}" data-type="${notification.type}" data-room-id="${notification.roomId}">
      ${
        notification.type === 'join' ? /* html */`
          <p class="notification-list__item__message">${notification.message}</p>

          <div class="notification-list__item__buttons">
            <button class="notification-list__item__buttons__approve">Approve</button>
            <button class="notification-list__item__buttons__deny">Deny</button>
          </div>
        ` : /* html */`
          <p class="notification-list__item__message">${notification.message}</p>
        `
}
    </li>
  `;
};

triggerWhenElementExist('#notification-list', 'click', event => {
  if (event.target.tagName !== 'BUTTON') return;
  const isApprove = event.target.classList.contains('notification-list__item__buttons__approve');
  const isDeny = event.target.classList.contains('notification-list__item__buttons__deny');

  if (isApprove || isDeny) {
    const notification = event.target.parentElement.parentElement;

    if (notification.dataset.type === 'join') {
      const formData = new FormData();
      formData.append('notification_id', notification.dataset.id);
      formData.append('notification_room_id', notification.dataset.roomId);

      fetch(`/room/join/${isApprove ? 'accept' : 'decline'}`, {
        method: 'POST',
        body: formData
      })
          .then(response => response.json())
          .then(response => {
            if (response.status === 'success') {
              makeToastNotification(response.message);

              if (isApprove) {
                const currentPathArray = window.location.pathname.split('');
                const onRoomsPage = currentPathArray.includes('room') && currentPathArray.includes('open');

                if (onRoomsPage) {
                  window.location.href = response.redirect_link;
                } else {
                  makeToastNotification(`Open 'huddle' icon to go back to your rooms`);
                }
              }
            } else {
              console.log(response);
              makeToastNotification(response.message);
            }
          })
          .catch(error => {
            console.log(error);
          });
    }
  }
});

