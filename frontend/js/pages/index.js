import { consumeFlashMessage, hasAccessToken } from "../utils/storage.js";
import { showToast } from "../components/toast.js";

const flashMessage = consumeFlashMessage();
if (flashMessage) {
  showToast(flashMessage.message, flashMessage.type);
}

window.setTimeout(() => {
  window.location.href = hasAccessToken() ? "./dashboard.html" : "./login.html";
}, 1200);
