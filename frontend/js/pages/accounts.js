import { createBankAccount, listBankAccounts } from "../api/movement.js";
import { renderNavbar } from "../components/navbar.js";
import { setButtonLoading } from "../components/loading.js";
import { showToast } from "../components/toast.js";
import { requireAuth } from "../utils/auth-guard.js";
import { formatCurrency } from "../utils/formatters.js";
import { requireNonNegativeNumber, requireText } from "../utils/validators.js";

requireAuth();
renderNavbar("accounts");

const form = document.getElementById("account-form");
const formError = document.getElementById("form-error");
const submitButton = document.getElementById("submit-button");
const accountsList = document.getElementById("accounts-list");

async function renderAccounts() {
  const accounts = await listBankAccounts();
  if (!accounts.length) {
    accountsList.innerHTML = `<div class="empty-state">Nenhuma conta cadastrada ainda.</div>`;
    return;
  }

  accountsList.innerHTML = accounts
    .map(
      (account) => `
        <article class="card-item">
          <strong>${account.name}</strong>
          <small>${account.bank_name} - ${account.account_number}</small>
          <p>${formatCurrency(account.balance)}</p>
          <span class="badge ${account.status === "active" ? "success" : "warning"}">
            ${account.status}
          </span>
        </article>
      `,
    )
    .join("");
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;
  setButtonLoading(submitButton, true, "Salvar conta");

  try {
    const payload = {
      name: requireText(document.getElementById("name").value, "Nome da conta", 24),
      bank_name: requireText(document.getElementById("bank-name").value, "Banco", 24),
      account_number: requireText(document.getElementById("account-number").value, "Numero da conta", 24),
      initial_balance: requireNonNegativeNumber(
        document.getElementById("initial-balance").value,
        "Saldo inicial",
      ),
    };

    await createBankAccount(payload);
    form.reset();
    document.getElementById("initial-balance").value = "0";
    showToast("Conta criada com sucesso.", "success");
    await renderAccounts();
  } catch (error) {
    formError.textContent = error.message;
    formError.hidden = false;
  } finally {
    setButtonLoading(submitButton, false, "Salvar conta");
  }
});

renderAccounts().catch((error) => {
  showToast(error.message, "error");
});
