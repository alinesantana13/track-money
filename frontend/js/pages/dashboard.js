import { fetchUserProfile } from "../api/auth.js";
import { listBankAccounts } from "../api/movement.js";
import { getCurrentSubscription } from "../api/subscription.js";
import { renderNavbar } from "../components/navbar.js";
import { showToast } from "../components/toast.js";
import { formatCurrency } from "../utils/formatters.js";
import { requireAuth } from "../utils/auth-guard.js";

requireAuth();
renderNavbar("dashboard");

const welcomeTitle = document.getElementById("welcome-title");
const activePlan = document.getElementById("active-plan");
const accountsCount = document.getElementById("accounts-count");
const totalBalance = document.getElementById("total-balance");
const accountsPreview = document.getElementById("accounts-preview");

async function loadDashboard() {
  try {
    const [profile, subscription, accounts] = await Promise.all([
      fetchUserProfile(),
      getCurrentSubscription(),
      listBankAccounts(),
    ]);

    welcomeTitle.textContent = `Ola, ${profile.name}`;
    const currentPlan = subscription.plans.find((plan) => plan.active);
    activePlan.textContent = currentPlan ? currentPlan.name : "Sem plano ativo";
    accountsCount.textContent = String(accounts.length);
    totalBalance.textContent = formatCurrency(
      accounts.reduce((total, account) => total + account.balance, 0),
    );

    if (!accounts.length) {
      accountsPreview.innerHTML = `<div class="empty-state">Nenhuma conta cadastrada ainda.</div>`;
      return;
    }

    accountsPreview.innerHTML = accounts
      .slice(0, 3)
      .map(
        (account) => `
          <article class="card-item">
            <strong>${account.name}</strong>
            <small>${account.bank_name} - ${account.account_number}</small>
            <p>${formatCurrency(account.balance)}</p>
          </article>
        `,
      )
      .join("");
  } catch (error) {
    showToast(error.message, "error");
  }
}

loadDashboard();
