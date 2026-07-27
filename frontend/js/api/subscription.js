import { apiRequest } from "./api.js";

export async function listPlans() {
  return apiRequest("/subscription/plans");
}

export async function getCurrentSubscription() {
  return apiRequest("/subscription/user");
}

export async function selectPlan(planId) {
  return apiRequest("/subscription/select-plan", {
    method: "POST",
    body: JSON.stringify({ plan_id: planId }),
  });
}
