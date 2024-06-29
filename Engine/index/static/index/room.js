import {allowedToFetch, element} from '../../../static/helper.js';

const roomsContainer = element('#room-posts');
const objectIsEmpty = object_ => JSON.stringify(object_) === '{}';

try {
  if (allowedToFetch()) {
    const rooms = await fetch('/room');
    const response = await rooms.json();
    const isEmpty = objectIsEmpty(response);

    const roomTemplate = (code, title, description) => /* html */ `
      <a class="room-post" href="${code}">
        <h2 class="room-post__title">${title}</h2>
        <p class="room-post__description">${description}</p>
      </a>
    `;

    if (!isEmpty) {
      Object.entries(response).forEach(([code, {title, description}]) => {
        if (!roomsContainer) return;
        roomsContainer.innerHTML += roomTemplate(code, title, description);
      });
    }
  }
} catch (error) {
  console.log(error);
}
