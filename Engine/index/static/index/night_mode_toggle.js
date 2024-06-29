import makeToastNotification, {element, triggerWhenElementExist} from '../../../static/helper.js';

/**
 * Sets the mode of the application to either "Night" or "Day".
 *
 * @param {string} mode - The mode to set ("Night" or "Day").
 *
 * @example
 * // Set the mode to "Night"
 * setMode("Night");
 *
 * @example
 * // Set the mode to "Day"
 * setMode("Day");
 */
function setMode(mode) {
  if (mode === 'Night') {
    element('html').classList.add('night');
  }

  if (mode === 'Day') {
    element('html').classList.remove('night');
  }

  fetch('/night-mode', {
    method: 'POST',
    body: JSON.stringify({mode: mode}),
    headers: {
      'Content-Type': 'application/json'
    }
  })
      .then(response => response.json())
      .then(response => {
        if (response.status === true) {
          makeToastNotification(mode);
        } else {
          makeToastNotification(response.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
};

const nightToggle = element('#night-toggle');
const sunOffIcon = element('#sun-off');
const sunIcon = element('#sun');

triggerWhenElementExist(nightToggle, 'click', () => {
  const night = element('html').classList.contains('night');

  night ? setMode('Day') : setMode('Night');
  nightToggle.textContent = night ? 'Day' : 'Night';
});

triggerWhenElementExist(sunIcon, 'click', () => {
  setMode('Night');
  sunOffIcon.style.display = 'none';
  sunIcon.style.display = 'block';
});

triggerWhenElementExist(sunOffIcon, 'click', () => {
  setMode('Day');
  sunIcon.style.display = 'none';
  sunOffIcon.style.display = 'block';
});
