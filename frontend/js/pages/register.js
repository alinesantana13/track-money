import { loginUser, registerUser } from "../api/auth.js";
import { setButtonLoading } from "../components/loading.js";
import { showToast } from "../components/toast.js";
import { redirectIfAuthenticated } from "../utils/auth-guard.js";
import { requireEmail, requirePassword, requireText } from "../utils/validators.js";

redirectIfAuthenticated();

const form = document.getElementById("register-form");
const formError = document.getElementById("form-error");
const submitButton = document.getElementById("submit-button");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;
  setButtonLoading(submitButton, true, "Cadastrar");

  try {
    const payload = {
      name: requireText(document.getElementById("name").value, "Nome", 128),
      email: requireEmail(document.getElementById("email").value),
      password: requirePassword(document.getElementById("password").value),
    };

    await registerUser(payload);
    await loginUser(payload.email, payload.password);
    showToast("Conta criada com sucesso.", "success");
    window.location.href = "./dashboard.html";
  } catch (error) {
    formError.textContent = error.message;
    formError.hidden = false;
  } finally {
    setButtonLoading(submitButton, false, "Cadastrar");
  }
});
