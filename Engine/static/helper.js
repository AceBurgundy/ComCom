/**
 * Selects the first HTML element that matches the given selector.
 *
 * @function element
 * @param {string} selector - The selector used for document.querySelector
 * @return {HTMLElement} The first HTML element that matches the given class name, or null if no elements match.
 */
export const element = selector => document.querySelector(selector);

/**
 * Selects the a list of HTML elements that matches the given selector.
 *
 * @function element
 * @param {string} selector - The selector used for document.querySelector
 * @return {HTMLElement} The first HTML element that matches the given class name, or null if no elements match.
 */
export const elements = selector => document.querySelectorAll(selector);

/**
 * Adds a character counter to an input field and updates a corresponding counter element.
 * @param {string} inputId - The id of the input field.
 * @param {string} counterId - The id of the counter element.
 * @param {number|null} restriction - The character limit (null for no limit).
 */
export const counter = (inputId, counterId, restriction) => {
  const inputElement = element(`#${inputId}`);
  const counterElement = element(`#${counterId}`);

  triggerWhenElementExist(inputElement, 'click', () => {
    if (restriction === null || inputElement.value.length <= restriction) {
      counterElement.children[0].textContent = inputElement.value.length;
    }
  });

  window.addEventListener('load', () => {
    if (counterElement) counterElement.children[0].textContent = inputElement.value.length;
  }
  );
};

/**
 * Toggles the visibility of eye icons in a form.
 * @param {string} eyesContainerId - The id of the container for eye icons.
 * @param {string} inputId - The id of the input field.
 * @param {string} eyeId - The id of the eye icon (open).
 * @param {string} eyeSlashId - The id of the eye icon (close).
 */
export const eyeToggle = (eyesContainerId, inputId, eyeId, eyeSlashId) => {
  eyesContainerId.addEventListener('click', () => {
    const typeIsText = inputId.getAttribute('type') === 'text';

    inputId.setAttribute('type', typeIsText ? 'password' : 'text');
    eyeSlashId.style.display = typeIsText ? 'block' : 'none';
    eyeId.style.display = typeIsText ? 'none' : 'block';
  });
};

/**
 * Creates a toast notification element and appends it to the flashes container.
 * @param {string} message - The message content of the notification.
 */
export default function makeToastNotification(message) {
  const flashes = element('.flashes');

  if (message === '') {
    return;
  }

  Array(flashes.children).forEach(child => {
    if (child.textContent === message) {
      return;
    }

    const newToast = document.createElement('li');
    newToast.classList.add('message');
    newToast.textContent = message;

    flashes.append(newToast);
    newToast.classList.toggle('active');

    setTimeout(() => {
      newToast.classList.remove('active');
      setTimeout(() => newToast.remove(), 500);
    }, 2000);
  });
}

/**
 * Automatically adjusts the height of a given HTML element to match its scroll height.
 *
 * @function autoResize
 * @param {HTMLElement} element - The HTML element whose height needs to be adjusted.
 */
export const autoResize = element => {
  element.style.height = 'auto';
  element.style.height = element.scrollHeight + 'px';
};

/**
 * @return {String} the current orientation of the window
 */
export const getCurrentOrientation = () => window.matchMedia('(orientation: portrait)').matches ? 'portrait' : 'landscape';

/**
 * Attaches an event listener to an element specified by a selector or HTML element.
 *
 * @param {string|Element} elementOrSelector - A string representing the selector (ID or class name) or an HTML element.
 * @param {string} eventType - The type of event to listen for (e.g., 'click', 'mouseover').
 * @param {Function} callback - The function to execute when the event occurs.
 *
 * @example
 * // Attaches a click event to an element with ID 'myElement'
 * triggerWhenElementExist('#myElement', 'click', function() {
 *     console.log('Element clicked!');
 * });
 *
 * @example
 * // Attaches a click event to an HTML element
 * const someElement = document.getElementById('some-element');
 * triggerWhenElementExist(someElement, 'click', function() {
 *     console.log('Element clicked!');
 * });
 */
export const triggerWhenElementExist = (elementOrSelector, eventType, callback) => {
  const isHTMLElement = elementOrSelector instanceof Element;
  const element = isHTMLElement ? elementOrSelector : document.querySelector(elementOrSelector);

  if (!element) {
    return;
  }

  element.addEventListener(eventType, callback);
};

/**
 * Attaches an event listener to multiple elements specified by an array of selectors or HTML elements.
 *
 * @param {Array<string|Element>} elementsOrSelectors - An array of strings representing selectors (ID or class name) or HTML elements.
 * @param {string} eventType - The type of event to listen for (e.g., 'click', 'mouseover').
 * @param {Function} callback - The function to execute when the event occurs.
 *
 * @example
 * // Attaches a click event to elements with IDs or class names
 * triggerWhenElementsExist(['#myElement', '.myClass'], 'click', function() {
 *     console.log('Element clicked!');
 * });
 *
 * @example
 * // Attaches a click event to HTML elements
 * const someElement = document.getElementById('some-element');
 * const anotherElement = document.querySelector('.another-element');
 * triggerWhenElementsExist([someElement, anotherElement], 'click', function() {
 *     console.log('Element clicked!');
 * });
 */
export const triggerWhenElementsExist = (elementsOrSelectors, eventType, callback) => {
  elementsOrSelectors.forEach(item =>
    triggerWhenElementExist(item, eventType, callback)
  );
};

export const allowedToFetch = () => {
  const noNotif = ['/login', '/register'];
  return !noNotif.includes(window.location.pathname);
};

export const isLoggedIn = async () => {
  try {
    const response = await fetch('/is_logged_in');
    const data = await response.json();

    return data.logged_in;
  } catch (error) {
    console.error(error);
  }
};
