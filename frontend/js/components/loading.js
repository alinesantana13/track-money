export function setButtonLoading(button, isLoading, label = "Salvar") {
  if (!button) {
    return;
  }

  button.disabled = isLoading;
  button.textContent = isLoading ? "Carregando..." : label;
}
