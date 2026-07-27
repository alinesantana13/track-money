import { loginUser } from "../api/auth.js";
import { setButtonLoading } from "../components/loading.js";
import { showToast } from "../components/toast.js";
import { redirectIfAuthenticated } from "../utils/auth-guard.js";
import { consumeFlashMessage } from "../utils/storage.js";
import { requireEmail, requirePassword } from "../utils/validators.js";

redirectIfAuthenticated();

const flashMessage = consumeFlashMessage();
if (flashMessage) {
  showToast(flashMessage.message, flashMessage.type);
}

const form = document.getElementById("login-form");
const formError = document.getElementById("form-error");
const submitButton = document.getElementById("submit-button");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;
  setButtonLoading(submitButton, true, "Entrar");

  try {
    const email = requireEmail(document.getElementById("email").value);
    const password = requirePassword(document.getElementById("password").value);
    await loginUser(email, password);
    showToast("Login realizado com sucesso.", "success");
    window.location.href = "./dashboard.html";
  } catch (error) {
    formError.textContent = error.status === 401
      ? "Email ou senha incorretos."
      : error.message;
    formError.hidden = false;
  } finally {
    setButtonLoading(submitButton, false, "Entrar");
  }
});
