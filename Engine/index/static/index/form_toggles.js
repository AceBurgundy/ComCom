import {element, triggerWhenElementExist, triggerWhenElementsExist} from '../../../static/helper.js';

const formXButton = element('#create-room__close-box');
const formBackground = element('#form-background');
const createRoomForm = element('#create-room');

/**
 * Activates a form by adding the 'active' class to its background and form elements.
 */
function openForm() {
  formBackground.classList.add('active');
  createRoomForm.classList.add('active');
}

triggerWhenElementsExist([
  '#room-buttons__create-button', // Toggle form
  '#room-options-new', // Create room toggle form
  '#main-content-rooms-list-create'// Room list toggle form
], 'click', () => openForm());

triggerWhenElementExist(formXButton, 'click', () => {
  formBackground.classList.remove('active');
  createRoomForm.classList.remove('active');
});
