import makeToastNotification, {element} from '../../../static/helper.js';

/**
 * creates a template div that shows the format of the file
 * @param {string} filename
 * @return {string}
 */
function createIcon(filename) {
  const parts = filename.split('.');
  const format = (parts.length > 1 && parts[0] !== '') ? parts[parts.length - 1] : '';
  const mainClass = 'file-icon-box';

  return /* html */`
    <div class="${mainClass}" data-file-name="${filename}">
      <div class="${mainClass}__logo">${format}</div>
      <div class="${mainClass}__file-name">${filename}</div>
    </div>
  `;
};

const filesArea = element('#main-content-rooms-chat-center-left-files');
const dropFileMessage = element('#main-content-rooms-chat-center-left-info');
const uploadButton = element('#main-content-rooms-chat-center-left-files-upload');

// Prevent default behavior on dragover
filesArea.addEventListener('dragover', event => event.preventDefault());

const filesDropped = {};

filesArea.ondrop = event => {
  event.preventDefault();

  const files = event.dataTransfer.files;

  if (files.length <= 0) {
    return;
  }

  let filesProcessed = 0;

  for (const file of files) {
    if (file.name in filesDropped) {
      makeToastNotification(`${file.name} already exists`);
      continue;
    }

    dropFileMessage.classList.add('hidden');

    const reader = new FileReader();

    reader.onload = event => {
      const base64Data = event.target.result;
      filesArea.innerHTML += createIcon(file.name);
      filesDropped[file.name] = base64Data;

      filesProcessed++;

      if (filesProcessed === files.length) {
        if (Object.keys(filesDropped).length > 0) uploadButton.style.display = 'block';
      }
    };

    reader.readAsDataURL(file);
  }
};
