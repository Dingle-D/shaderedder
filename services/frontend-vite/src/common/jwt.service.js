const AUTH_TOKEN = "auth_token";

export const getToken = () => {
  return window.localStorage.getItem(AUTH_TOKEN);
};

export const saveToken = (token_type, token) => {
  window.localStorage.setItem(AUTH_TOKEN, `${token_type} ${token}`);
};

export const destroyToken = () => {
  window.localStorage.removeItem(AUTH_TOKEN);
};

export default {
  getToken,
  saveToken,
  destroyToken
};
