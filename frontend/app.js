// ── Configuration ────────────────────────────────────────────
const API_BASE = window.location.origin;
let token = localStorage.getItem("token");
let currentFilter = "all";
let currentPage = 0;
const PAGE_SIZE = 10;

// ── Init ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    if (token) {
        showTasks();
        loadTasks();
    }
});

// ── API Helper ───────────────────────────────────────────────
async function apiCall(endpoint, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(`${API_BASE}${endpoint}`, opts);
    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "Something went wrong");
    }
    return data;
}

// ── Auth ─────────────────────────────────────────────────────
function switchTab(tab) {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((t) => t.classList.remove("active"));

    if (tab === "login") {
        tabs[0].classList.add("active");
        document.getElementById("login-form").classList.remove("hidden");
        document.getElementById("register-form").classList.add("hidden");
    } else {
        tabs[1].classList.add("active");
        document.getElementById("login-form").classList.add("hidden");
        document.getElementById("register-form").classList.remove("hidden");
    }
    hideMessage("auth-message");
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById("reg-username").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;

    try {
        await apiCall("/register", "POST", { username, email, password });
        showMessage("auth-message", "Registration successful. Please login.", "success");
        document.getElementById("register-form").reset();
        setTimeout(() => switchTab("login"), 1000);
    } catch (err) {
        showMessage("auth-message", err.message, "error");
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;

    try {
        const data = await apiCall("/login", "POST", {
            username,
            email: `${username}@login.com`,
            password,
        });
        token = data.access_token;
        localStorage.setItem("token", token);
        localStorage.setItem("username", username);
        showTasks();
        loadTasks();
    } catch (err) {
        showMessage("auth-message", err.message, "error");
    }
}

function logout() {
    token = null;
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    showAuth();
}

// ── View Switching ───────────────────────────────────────────
function showAuth() {
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("tasks-section").classList.add("hidden");
    document.getElementById("user-info").classList.add("hidden");
    hideMessage("auth-message");
}

function showTasks() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("tasks-section").classList.remove("hidden");
    document.getElementById("user-info").classList.remove("hidden");
    const username = localStorage.getItem("username") || "User";
    document.getElementById("username-display").textContent = username;
}

// ── Tasks ────────────────────────────────────────────────────
async function loadTasks() {
    try {
        let endpoint = `/tasks/?skip=${currentPage * PAGE_SIZE}&limit=${PAGE_SIZE}`;
        if (currentFilter === "active") endpoint += "&completed=false";
        else if (currentFilter === "completed") endpoint += "&completed=true";

        const data = await apiCall(endpoint);
        renderTasks(data.tasks);
        renderPagination(data.total);
    } catch (err) {
        if (err.message.includes("credentials")) {
            logout();
        } else {
            showMessage("tasks-message", err.message, "error");
        }
    }
}

function renderTasks(tasks) {
    const list = document.getElementById("task-list");

    if (tasks.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <p>No tasks yet. Add one above.</p>
            </div>
        `;
        return;
    }

    list.innerHTML = tasks
        .map(
            (task) => `
        <div class="task-item ${task.completed ? "completed" : ""}" id="task-${task.id}">
            <div class="task-check ${task.completed ? "checked" : ""}"
                 onclick="toggleTask(${task.id}, ${!task.completed})"></div>
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ""}
            </div>
            <div class="task-actions">
                ${!task.completed ? `<button class="btn btn-complete" onclick="toggleTask(${task.id}, true)">Done</button>` : ""}
                <button class="btn btn-danger" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>
    `
        )
        .join("");
}

function renderPagination(total) {
    const pag = document.getElementById("pagination");
    const totalPages = Math.ceil(total / PAGE_SIZE);

    if (totalPages <= 1) {
        pag.classList.add("hidden");
        return;
    }

    pag.classList.remove("hidden");
    document.getElementById("page-info").textContent = `Page ${currentPage + 1} of ${totalPages}`;
    document.getElementById("prev-btn").disabled = currentPage === 0;
    document.getElementById("next-btn").disabled = currentPage >= totalPages - 1;
}

function changePage(delta) {
    currentPage += delta;
    loadTasks();
}

async function handleCreateTask(e) {
    e.preventDefault();
    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-description").value.trim();

    try {
        await apiCall("/tasks/", "POST", {
            title,
            description: description || null,
        });
        document.getElementById("create-task-form").reset();
        currentPage = 0;
        loadTasks();
    } catch (err) {
        showMessage("tasks-message", err.message, "error");
    }
}

async function toggleTask(id, completed) {
    try {
        await apiCall(`/tasks/${id}`, "PUT", { completed });
        loadTasks();
    } catch (err) {
        showMessage("tasks-message", err.message, "error");
    }
}

async function deleteTask(id) {
    try {
        await apiCall(`/tasks/${id}`, "DELETE");
        loadTasks();
    } catch (err) {
        showMessage("tasks-message", err.message, "error");
    }
}

function filterTasks(filter) {
    currentFilter = filter;
    currentPage = 0;
    document.querySelectorAll(".filter-btn").forEach((btn) => btn.classList.remove("active"));
    event.target.classList.add("active");
    loadTasks();
}

// ── Utilities ────────────────────────────────────────────────
function showMessage(id, text, type) {
    const el = document.getElementById(id);
    el.textContent = text;
    el.className = `message ${type}`;
    el.classList.remove("hidden");
    setTimeout(() => hideMessage(id), 4000);
}

function hideMessage(id) {
    document.getElementById(id).classList.add("hidden");
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
