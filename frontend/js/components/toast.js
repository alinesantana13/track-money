export function showToast(message, type = "info") {
  const root = document.getElementById("toast-root");
  if (!root) {
    return;
  }

  const element = document.createElement("div");
  element.className = `toast ${type}`;
  element.textContent = message;
  root.appendChild(element);

  window.setTimeout(() => {
    element.remove();
  }, 3500);
}
