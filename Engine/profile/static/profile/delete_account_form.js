import makeToastNotification, {element, triggerWhenElementExist} from '../../../static/helper.js';

const deleteAccountToggle = element('#delete-account-toggle');
const deleteAccountForm = element('#delete-account-form');
const formBackground = element('#form-background');

triggerWhenElementExist(deleteAccountToggle, 'click', () => {
  formBackground.classList.add('active');
  deleteAccountForm.classList.add('active');
});

element('#delete-account-cancel').addEventListener('click', () => {
  formBackground.classList.remove('active');
  deleteAccountForm.classList.remove('active');
});

// delete account form submission
deleteAccountForm.addEventListener('submit', event => {
  event.preventDefault();

  const formData = new FormData(deleteAccountForm);

  fetch('/profile/delete', {
    method: 'POST',
    body: formData
  })
      .then(response => response.json())
      .then(response => {
        if (response.status === 'error') {
          makeToastNotification(response.message);
          deleteAccountForm.reset();
        } else {
          window.location.href = response.url;
        }
      })
      .catch(error => {
        console.log(error);
      });
});
