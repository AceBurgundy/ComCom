import {element, triggerWhenElementsExist} from '../../../static/helper.js';

const infoToggle = element('#main-content-rooms-chat-top-right-info');
const infoIcon = element('#info');

const backButton = element('#main-content-rooms-chat_info-top-members-close');
const info = element('#main-content-rooms-chat_info');
const chat = element('#main-content-rooms-chat');

// When user clicks on the "Info" text
// This also assume that user is in landscape mode as this icon only shows on landscape
infoToggle.onclick = () => {
  info.classList.toggle('active');
  chat.style.width = info.classList.contains('active') ? '60%' : '80%';
};

// When user clicks on the info icon
// This also assume that user is in portrait mode as this icon only shows on portrait
triggerWhenElementsExist([infoIcon, backButton], 'click', () => {
  info.classList.toggle('portrait-active');
  backButton.classList.toggle('active');
});
