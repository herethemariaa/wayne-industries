const API_BASE = "http://localhost:5000/api";

// Mapeamento dos módulos
const MODULES = {
  weapons: {
    endpoint: "weapons",
    fields: ["name", "category"],
    labels: { name: "Nome", category: "Categoria" }
  },
  vehicles: {
    endpoint: "vehicles",
    fields: ["model", "plate"],
    labels: { model: "Modelo", plate: "Placa" }
  },
  items: {
    endpoint: "items",
    fields: ["name", "category", "quantity"],
    labels: { name: "Nome", category: "Categoria", quantity: "Qtd" }
  }
};

// Descobre o módulo pela tag <body data-module="">
const moduleName = document.body.dataset.module;
const moduleConfig = MODULES[moduleName];

if (!moduleConfig) {
  console.error("Módulo inválido:", moduleName);
}

// Seletores
const cardsContainer = document.querySelector(".cards");
const createBtn = document.querySelector(".btn-create");
const searchInput = document.querySelector(".search-box input");

// Renderiza cards dinamicamente
function renderData(data) {
  cardsContainer.innerHTML = "";
  data.forEach(item => {
    const card = document.createElement("div");
    card.classList.add("card");

    let html = "";
    moduleConfig.fields.forEach(field => {
      html += `<p><strong>${moduleConfig.labels[field]}:</strong> ${item[field]}</p>`;
    });

    card.innerHTML = `
      <h2>${item[moduleConfig.fields[0]]}</h2>
      ${html}
      <div class="img-box"></div>
      <span class="edit" data-id="${item.id}">✏️</span>
      <span class="delete" data-id="${item.id}">🗑️</span>
    `;

    cardsContainer.appendChild(card);
  });

  document.querySelectorAll(".edit").forEach(btn =>
    btn.addEventListener("click", e => editItem(e.target.dataset.id))
  );
  document.querySelectorAll(".delete").forEach(btn =>
    btn.addEventListener("click", e => deleteItem(e.target.dataset.id))
  );
}

// Buscar
async function fetchData() {
  const res = await fetch(`${API_BASE}/${moduleConfig.endpoint}`, { credentials: "include" });
  const data = await res.json();
  renderData(data);
}

// Criar
async function createItem() {
  let obj = {};
  for (let field of moduleConfig.fields) {
    const value = prompt(`${moduleConfig.labels[field]}:`);
    if (!value) return;
    obj[field] = value;
  }

  await fetch(`${API_BASE}/${moduleConfig.endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(obj)
  });
  fetchData();
}

// Editar
async function editItem(id) {
  let obj = {};
  for (let field of moduleConfig.fields) {
    const value = prompt(`Novo ${moduleConfig.labels[field]}:`);
    if (!value) return;
    obj[field] = value;
  }

  await fetch(`${API_BASE}/${moduleConfig.endpoint}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(obj)
  });
  fetchData();
}

// Deletar
async function deleteItem(id) {
  if (!confirm("Deseja deletar este item?")) return;

  await fetch(`${API_BASE}/${moduleConfig.endpoint}/${id}`, {
    method: "DELETE",
    credentials: "include"
  });
  fetchData();
}

// Filtro
searchInput.addEventListener("input", async () => {
  const query = searchInput.value.toLowerCase();
  const res = await fetch(`${API_BASE}/${moduleConfig.endpoint}`, { credentials: "include" });
  const data = await res.json();
  const filtered = data.filter(item =>
    moduleConfig.fields.some(f => item[f]?.toString().toLowerCase().includes(query))
  );
  renderData(filtered);
});

createBtn.addEventListener("click", createItem);

// Inicializar
fetchData();
