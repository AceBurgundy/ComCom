import makeToastNotification, {element, eyeToggle, triggerWhenElementExist} from '../../../static/helper.js';

// new password
const newPasswordForm = element('#new-password-modal');
const formBackground = element('#form-background');

triggerWhenElementExist('#change-password', 'click', () => {
  formBackground.classList.add('active');
  newPasswordForm.classList.add('active');
});

triggerWhenElementExist('#new-password-close-button', 'click', () => {
  formBackground.classList.remove('active');
  newPasswordForm.classList.remove('active');
});

eyeToggle(
    element('#verify-eyes-icon-container'),
    element('#old-password-input'),
    element('#verify-eye'),
    element('#verify-eye-off')
);

eyeToggle(
    element('#new-password-eyes-icon-container'),
    element('#new-password-input'),
    element('#new-password-eye'),
    element('#new-password-eye-off')
);

eyeToggle(
    element('#delete-verify-eyes-icon-container'),
    element('#delete-account-password-input'),
    element('#delete-verify-eye'),
    element('#delete-verify-eye-off')
);

element('#new-password-update-button').addEventListener('click', event => {
  event.preventDefault();

  const oldPassword = element('#old-password-input').value;
  const newPassword = element('#new-password-input').value;

  fetch('/change-password', {
    method: 'POST',
    body: JSON.stringify({oldPassword, newPassword}),
    headers: {
      'Content-Type': 'application/json'
    }
  })
      .then(response => response.json())
      .then(response => {
        if (response.status === 'success') {
          makeToastNotification(response.message);
          newPasswordForm.classList.remove('active');
          formBackground.classList.remove('active');
        } else {
          makeToastNotification(response.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
});
