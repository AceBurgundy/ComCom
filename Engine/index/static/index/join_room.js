import makeToastNotification, {element, triggerWhenElementExist} from '../../../static/helper.js';

triggerWhenElementExist('#room-options-join', 'submit', event => {
  event.preventDefault();

  const roomCode = element('#room-options-join-input');
  const csrfInput = element('#csrf_token');
  const code = roomCode.value.trim();

  if (roomCode.value === '') {
    makeToastNotification('Code cannot be empty');
    return;
  }

  // Regular expressions for the valid formats
  const patternWithDashes = /^[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{3}$/i;
  const patternWithoutDashes = /^[A-Z0-9]{9}$/i;

  // Check if the code matches either of the patterns
  if (!patternWithDashes.test(code) && !patternWithoutDashes.test(code)) {
    makeToastNotification('Only XXX-XXX-XXX or XXXXXXXXX format is accepted');
    return;
  }

  const formData = new FormData();
  formData.append('csrf_token', csrfInput.value);
  formData.append('code', roomCode.value);

  fetch('/room/join', {
    method: 'POST',
    body: formData
  })
      .then(response => response.json())
      .then(response => {
        if (response.status === 'success') {
          makeToastNotification(response.message);
        /* Do something */
        } else {
          makeToastNotification(response.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
});
