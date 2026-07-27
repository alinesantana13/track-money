import { fetchUserProfile } from "../api/auth.js";
import { getCurrentSubscription } from "../api/subscription.js";
import { renderNavbar } from "../components/navbar.js";
import { showToast } from "../components/toast.js";
import { formatPlanPrice } from "../utils/formatters.js";
import { requireAuth } from "../utils/auth-guard.js";

requireAuth();
renderNavbar("profile");

const profileDetails = document.getElementById("profile-details");
const profilePlan = document.getElementById("profile-plan");

async function loadProfile() {
  try {
    const [profile, subscription] = await Promise.all([
      fetchUserProfile(),
      getCurrentSubscription(),
    ]);

    profileDetails.innerHTML = `
      <div>
        <dt>Nome</dt>
        <dd>${profile.name}</dd>
      </div>
      <div>
        <dt>Email</dt>
        <dd>${profile.email}</dd>
      </div>
    `;

    const activePlan = subscription.plans.find((plan) => plan.active);
    profilePlan.innerHTML = activePlan
      ? `
        <article class="card-item">
          <strong>${activePlan.name}</strong>
          <small>${formatPlanPrice(activePlan)}</small>
        </article>
      `
      : `<div class="empty-state">Nenhum plano ativo selecionado.</div>`;
  } catch (error) {
    showToast(error.message, "error");
  }
}

loadProfile();
