import { apiRequest } from "./api.js";

export async function listBankAccounts() {
  return apiRequest("/movement/bank-accounts");
}

export async function createBankAccount(payload) {
  return apiRequest("/movement/bank-accounts", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
