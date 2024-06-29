const baseURL = 'http://127.0.0.1:5000/';
const socket = io.connect(baseURL);

export {
  baseURL,
  socket
};