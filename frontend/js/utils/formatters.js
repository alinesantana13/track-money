export function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(value || 0));
}

export function formatPlanPrice(plan) {
  if (plan.is_free) {
    return "Gratuito";
  }
  return `${formatCurrency(plan.price)}/mes`;
}
