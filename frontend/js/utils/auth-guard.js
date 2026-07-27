import { clearAccessToken, hasAccessToken, setFlashMessage } from "./storage.js";

export function requireAuth() {
  if (!hasAccessToken()) {
    window.location.href = "./login.html";
  }
}

export function redirectIfAuthenticated() {
  if (hasAccessToken()) {
    window.location.href = "./dashboard.html";
  }
}

export function handleUnauthorized() {
  clearAccessToken();
  setFlashMessage("Sessao expirada. Faca login novamente.", "error");
  window.location.href = "./login.html";
}
