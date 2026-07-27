const ACCESS_TOKEN_KEY = "track-money.access-token";
const FLASH_MESSAGE_KEY = "track-money.flash-message";

export function setAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function hasAccessToken() {
  return Boolean(getAccessToken());
}

export function setFlashMessage(message, type = "info") {
  localStorage.setItem(
    FLASH_MESSAGE_KEY,
    JSON.stringify({ message, type, createdAt: Date.now() }),
  );
}

export function consumeFlashMessage() {
  const payload = localStorage.getItem(FLASH_MESSAGE_KEY);
  if (!payload) {
    return null;
  }

  localStorage.removeItem(FLASH_MESSAGE_KEY);
  return JSON.parse(payload);
}
