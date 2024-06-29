/* eslint-disable max-len */
import {
  element,
  getCurrentOrientation,
  triggerWhenElementExist
} from '../../../static/helper.js';

document.addEventListener('click', event => {
  if (event.target.closest('.close-button')) {
    window.history.back();
  }
});

element('#profile-top-controls').innerHTML += /* html */`
  <div class="button close-button" id="close-text">Go Back</div>
  <div class="button" id="profile-close-button">Cancel</div>
  <svg class="close-button" id="x-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M13.41,12l6.3-6.29a1,1,0,1,0-1.42-1.42L12,10.59,5.71,4.29A1,1,0,0,0,4.29,5.71L10.59,12l-6.3,6.29a1,1,0,0,0,0,1.42,1,1,0,0,0,1.42,0L12,13.41l6.29,6.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z"/></svg>
`;

const targetElement = element(getCurrentOrientation() === 'portrait' ? '#profile-bottom' : '#profile-top-controls');
const changePasswordTemplate = /* html */`<div class="button" id="change-password">Change password</div>`;
const deleteAccountTemplate = /* html */`<div class="button" id="delete-account-toggle">Delete Account</div>`;

/**
 * Checks if the target element is allowed based on data attributes.
 *
 * @return {boolean} True if the element is allowed, false otherwise.
 */
function isAllowed() {
  if (!targetElement) {
    return false;
  }

  if (!targetElement.hasAttribute('data-user-id') || !targetElement.hasAttribute('data-current-user-id')) {
    return true;
  }

  return targetElement.getAttribute('data-user-id') === targetElement.getAttribute('data-current-user-id');
}

if (isAllowed()) {
  targetElement.insertAdjacentHTML('afterbegin', changePasswordTemplate);
  targetElement.insertAdjacentHTML('afterbegin', deleteAccountTemplate);
}

const deleteAccountToggle = element('#delete-account-toggle');
const profilePictureInput = element('#profile-picture-input');
const profileTopControls = element('#profile-top-controls');
const cancelButton = element('#profile-close-button');
const cameraIcon = element('#camera-icon-container');
const imageInput = element('#profile-picture-input');
const bottomSave = element('#bottom-save-button');
const inputCounter = element('#motto-counter');
const topSave = element('#top-save-button');
const editButton = element('#edit-button');
const usernameInput = element('#username');

const blockElements = [
  deleteAccountToggle,
  cancelButton,
  cameraIcon,
  inputCounter,
  imageInput
];

const hideElements = [
  cancelButton,
  deleteAccountToggle,
  inputCounter
];

const readonlyElements = [profilePictureInput, usernameInput];
const backgroundColorElements = [usernameInput];

if (getCurrentOrientation() === 'landscape') {
  [...profileTopControls.children].forEach(child =>
    child.classList.remove('button')
  );
}

triggerWhenElementExist(editButton, 'click', event => {
  if (getCurrentOrientation() === 'portrait') {
    bottomSave.style.display = 'block';
    topSave.style.display = 'block';
  }

  // Shows some more options when editting
  blockElements.forEach(element => {
    if (element) {
      element.style.display = 'block';
    }
  });

  // Changes the color of the text background into the input
  backgroundColorElements.forEach(element => {
    if (element) {
      element.style.backgroundColor = 'var(--input-background)';
    }
  });

  // Makes the text editable
  readonlyElements.forEach(element => {
    if (element) {
      element.removeAttribute('readonly');
    }
  });

  // hides the edit button
  event.target.style.display = 'none';
});

cancelButton.addEventListener('click', event => {
  if (getCurrentOrientation() === 'portrait') {
    bottomSave.style.display = 'none';
    topSave.style.display = 'none';
  }

  // hides some elements when cancelling edit
  hideElements.forEach(element => {
    if (element) element.style.display = 'none';
  });

  // reverts some elements back to their parents background color
  backgroundColorElements.forEach(element => {
    if (element) element.style.backgroundColor = 'inherit';
  });

  // reverts input elements back to readonly
  readonlyElements.forEach(element => {
    if (element) element.setAttribute('readonly', 'readonly');
  });

  // hides the cancel button and shows the edit button
  event.target.style.display = 'none';
  editButton.style.display = 'block';
});

