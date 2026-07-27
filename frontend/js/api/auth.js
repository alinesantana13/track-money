import { apiRequest } from "./api.js";
import { clearAccessToken, setAccessToken, setFlashMessage } from "../utils/storage.js";

export async function registerUser(payload) {
  return apiRequest("/users", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loginUser(email, password) {
  const body = new URLSearchParams({
    username: email,
    password,
  });
  const response = await apiRequest("/users/token", {
    method: "POST",
    redirectOnUnauthorized: false,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
  setAccessToken(response.access_token);
  return response;
}

export async function fetchUserProfile() {
  return apiRequest("/users/profile");
}

export function logoutUser() {
  clearAccessToken();
  setFlashMessage("Logout realizado com sucesso.", "success");
  window.location.href = "./login.html";
}
