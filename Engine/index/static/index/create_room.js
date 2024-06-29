import makeToastNotification, {counter, element, triggerWhenElementExist} from '../../../static/helper.js';

// Add room form submission
counter('create-room__body', 'motto-counter', 3000);

triggerWhenElementExist('#create-room', 'submit', event => {
  event.preventDefault();

  const csrfInput = element('#csrf_token');
  const titleInput = element('#create-room__title');
  const bodyInput = element('#create-room__body');

  if (titleInput.value === '' || bodyInput.value === '') {
    makeToastNotification('Fields Cannot be empty');
    return;
  }

  if (bodyInput.value.length > 750) {
    makeToastNotification('Content cannot be greater than 750');
    return;
  }

  if (titleInput.value.length > 100) {
    makeToastNotification('Title cannot be greater than 100');
    return;
  }

  const formData = new FormData();
  formData.append('csrf_token', csrfInput.value);
  formData.append('title', titleInput.value);
  formData.append('body', bodyInput.value);

  titleInput.value = '';
  bodyInput.value = '';

  fetch('/room/create', {
    method: 'POST',
    body: formData
  })
      .then(response => response.json())
      .then(response => {
        if (!response.status) return;
        if (response.status == 'success') {
          window.location.href = response.link;
        } else {
          makeToastNotification(response.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
});
