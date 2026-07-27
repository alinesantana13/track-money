import { getCurrentSubscription, listPlans, selectPlan } from "../api/subscription.js";
import { renderNavbar } from "../components/navbar.js";
import { showToast } from "../components/toast.js";
import { formatPlanPrice } from "../utils/formatters.js";
import { requireAuth } from "../utils/auth-guard.js";

requireAuth();
renderNavbar("plans");

const currentPlanElement = document.getElementById("current-plan");
const plansList = document.getElementById("plans-list");

async function renderCurrentPlan() {
  const subscription = await getCurrentSubscription();
  const activePlan = subscription.plans.find((plan) => plan.active);

  currentPlanElement.innerHTML = activePlan
    ? `
      <article class="card-item">
        <strong>${activePlan.name}</strong>
        <small>${formatPlanPrice(activePlan)}</small>
        <span class="badge success">Ativo</span>
      </article>
    `
    : `<div class="empty-state">Selecione um plano para liberar limites de contas.</div>`;
}

async function renderPlans() {
  const plans = await listPlans();
  plansList.innerHTML = plans
    .map(
      (plan) => `
        <article class="panel plan-card">
          <div>
            <span class="eyebrow">${plan.is_free ? "Entrada" : "Plano pago"}</span>
            <h3>${plan.name}</h3>
            <p class="price">${formatPlanPrice(plan)}</p>
            ${plan.is_free
              ? ""
              : '<p class="muted">Contratacao e pagamento disponiveis em breve.</p>'}
          </div>
          <button
            class="button ${plan.is_free ? "primary" : "secondary dark"}"
            type="button"
            data-plan-id="${plan.id}"
            data-plan-name="${plan.name}"
            data-plan-price="${formatPlanPrice(plan)}"
            data-plan-is-free="${plan.is_free}"
          >
            ${plan.is_free ? "Selecionar" : "Tenho interesse"}
          </button>
        </article>
      `,
    )
    .join("");

  plansList.querySelectorAll("[data-plan-id]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.dataset.planIsFree === "false") {
        showToast(
          `${button.dataset.planName} custa ${button.dataset.planPrice}. A contratacao estara disponivel em breve.`,
          "info",
        );
        return;
      }

      try {
        await selectPlan(Number(button.dataset.planId));
        showToast("Plano atualizado com sucesso.", "success");
        await renderCurrentPlan();
      } catch (error) {
        showToast(error.message, "error");
      }
    });
  });
}

Promise.all([renderCurrentPlan(), renderPlans()]).catch((error) => {
  showToast(error.message, "error");
});
