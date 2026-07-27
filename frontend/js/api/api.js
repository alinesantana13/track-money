import { handleUnauthorized } from "../utils/auth-guard.js";
import { getAccessToken } from "../utils/storage.js";

const API_BASE_URL = window.localStorage.getItem("track-money.api-base-url")
  || "http://localhost:8000";

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return null;
  }
  return response.json();
}

export async function apiRequest(path, { redirectOnUnauthorized = true, ...options } = {}) {
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();

  if (!headers.has("Content-Type") && options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && redirectOnUnauthorized) {
    handleUnauthorized();
  }

  const payload = await parseResponse(response);

  if (!response.ok) {
    const errorMessage = payload?.detail || payload?.message || "Nao foi possivel concluir a solicitacao.";
    const error = new Error(errorMessage);
    error.status = response.status;
    throw error;
  }

  return payload;
}
