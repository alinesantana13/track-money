import { logoutUser } from "../api/auth.js";

const links = [
  { href: "./dashboard.html", label: "Dashboard", key: "dashboard" },
  { href: "./accounts.html", label: "Contas", key: "accounts" },
  { href: "./plans.html", label: "Planos", key: "plans" },
  { href: "./profile.html", label: "Perfil", key: "profile" },
];

export function renderNavbar(activeKey) {
  const mountPoint = document.getElementById("app-nav");
  if (!mountPoint) {
    return;
  }

  mountPoint.innerHTML = `
    <nav class="nav-card">
      <div class="brand">
        <img src="./assets/logo.svg" alt="Track Money">
        <div>
          <strong>Track Money</strong>
          <p class="muted">Finanças</p>
        </div>
      </div>

      <div class="nav-links">
        ${links
          .map(
            (link) => `
              <a class="nav-link ${link.key === activeKey ? "active" : ""}" href="${link.href}">
                ${link.label}
              </a>
            `,
          )
          .join("")}
      </div>

      <div class="nav-footer">
        <button id="logout-button" class="button secondary" type="button">Sair</button>
      </div>
    </nav>
  `;

  const logoutButton = document.getElementById("logout-button");
  logoutButton?.addEventListener("click", () => {
    logoutUser();
  });
}
