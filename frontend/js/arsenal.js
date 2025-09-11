const API_BASE = "http://127.0.0.1:5000/api";

// Configuração dos módulos
const MODULES = {
  weapons: { endpoint: "weapons", fields: ["name", "category"], labels: { name: "Nome", category: "Categoria" } },
  vehicles: { endpoint: "vehicles", fields: ["model", "plate"], labels: { model: "Modelo", plate: "Placa" } },
  items: { endpoint: "items", fields: ["name", "category", "quantity"], labels: { name: "Nome", category: "Categoria", quantity: "Qtd" } }
};

// Seletores
const moduleTitleEl = document.getElementById("module-title");
const cardsContainer = document.querySelector(".cards");
const createBtn = document.querySelector(".btn-create");
const searchInput = document.querySelector(".search-box input");
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modal-title");
const modalForm = document.getElementById("modal-form");
const saveBtn = document.getElementById("save-btn");
const cancelBtn = document.getElementById("cancel-btn");
const navBtns = document.querySelectorAll(".nav-btn");
let editId = null;

// Pega o módulo atual
function getModule() { return MODULES[document.body.dataset.module]; }

// Abrir modal
function openModal(item=null) {
  modal.classList.remove("hidden");
  modalForm.innerHTML = "";
  const module = getModule();

  module.fields.forEach(f => {
    const input = document.createElement("input");
    input.name = f;
    input.placeholder = module.labels[f];
    input.value = item ? item[f] : '';
    modalForm.appendChild(input);
  });

  modalTitle.textContent = item ? `Editar ${moduleTitleEl.textContent}` : `Cadastrar ${moduleTitleEl.textContent}`;
  editId = item ? item.id : null;
}

// Fechar modal
function closeModal() {
  modal.classList.add("hidden");
  editId = null;
  modalForm.innerHTML = "";
}

// Salvar (criar ou editar)
saveBtn.onclick = async () => {
  const obj = {};
  modalForm.querySelectorAll("input").forEach(i => obj[i.name] = i.value);
  const module = getModule();

  if (editId) {
    await fetch(`${API_BASE}/${module.endpoint}/${editId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(obj)
    });
  } else {
    await fetch(`${API_BASE}/${module.endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(obj)
    });
  }

  await fetchData();
  closeModal();
}

// Cancelar
cancelBtn.onclick = closeModal;

// Renderiza cards
function renderData(data) {
  cardsContainer.innerHTML = "";
  const module = getModule();

  data.forEach(item => {
    const card = document.createElement("div");
    card.classList.add("card");

    let html = "";
    module.fields.forEach(f => html += `<p><strong>${module.labels[f]}:</strong> ${item[f]}</p>`);

    card.innerHTML = `<h2>${item[module.fields[0]]}</h2>${html}<span class="edit" data-id="${item.id}">✏️</span><span class="delete" data-id="${item.id}">🗑️</span>`;
    cardsContainer.appendChild(card);
  });

  document.querySelectorAll(".edit").forEach(btn => {
    btn.onclick = e => {
      const item = data.find(d => d.id == e.target.dataset.id);
      openModal(item);
    }
  });

  document.querySelectorAll(".delete").forEach(btn => {
    btn.onclick = e => deleteItem(e.target.dataset.id);
  });
}

// Buscar dados
async function fetchData() {
  const module = getModule();
  const res = await fetch(`${API_BASE}/${module.endpoint}`, { credentials: "include" });
  const data = await res.json();
  renderData(data);
}

// Deletar item
async function deleteItem(id) {
  if (!confirm("Deseja deletar este item?")) return;
  const module = getModule();
  await fetch(`${API_BASE}/${module.endpoint}/${id}`, { method: "DELETE", credentials: "include" });
  fetchData();
}

// Filtro de busca
searchInput.addEventListener("input", async () => {
  const module = getModule();
  const query = searchInput.value.toLowerCase();
  const res = await fetch(`${API_BASE}/${module.endpoint}`, { credentials: "include" });
  const data = await res.json();
  const filtered = data.filter(item => module.fields.some(f => item[f]?.toString().toLowerCase().includes(query)));
  renderData(filtered);
});

// Criar item
createBtn.onclick = () => openModal();

// Navegação módulos
navBtns.forEach(btn => {
  btn.onclick = () => {
    navBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    document.body.dataset.module = btn.dataset.module;
    moduleTitleEl.textContent = btn.textContent.replace(/[^\w\s]/g, '');
    fetchData();
  }
});
const logoutBtn = document.querySelector(".logout");

logoutBtn.addEventListener("click", () => {

    localStorage.clear(); 

    window.location.href = "login.html"; 
});
// Inicializar
fetchData();
