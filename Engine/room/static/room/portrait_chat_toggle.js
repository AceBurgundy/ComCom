import {element, getCurrentOrientation} from '../../../static/helper.js';

// All the code here will only work here on landscape as peopleIcon
// is only present in landscape
const peopleIcon = element('#people');
const chat = element('#main-content-rooms-chat');
const roomList = element('#main-content-rooms-list');

/**
 * Hides and unhides the room list
 */
function toggleRoomList() {
  chat.classList.toggle('portrait-active');
  roomList.classList.toggle('portrait-active');
}

if (getCurrentOrientation() === 'portrait') {
  toggleRoomList();
}

peopleIcon.onclick = () => toggleRoomList();

// clicking on a room list item
roomList.onclick = event => {
  const itemClassName = 'main-content-rooms-list__item';
  const notRoomItem = !event.target.classList.contains(itemClassName);


  if (notRoomItem) return;

  const clickedItemCode = event.target.dataset.code;
  const currenctChatCode = chat.dataset.code;

  if (clickedItemCode === currenctChatCode) {
    toggleRoomList();
    return;
  }

  // fetch clicked room item code
  // swap data in the chat div before showing it again with toggleRoomList()
};
