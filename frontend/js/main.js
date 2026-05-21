// ==================== CONFIGURATION ====================
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api' 
    : 'https://votre-api-dirhami.onrender.com/api';

// ==================== NAVIGATION ====================
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Mettre à jour le lien actif
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-menu a').forEach(link => {
        if (link.getAttribute('href') && link.getAttribute('href').includes(currentPage)) {
            link.classList.add('active');
        }
    });

    // Vérifier l'état de connexion
    updateAuthUI();
});

function updateAuthUI() {
    const token = localStorage.getItem('token');
    const authLinks = document.querySelectorAll('.nav-auth');

    authLinks.forEach(link => {
        if (token) {
            link.innerHTML = `
                <a href="#" class="btn btn-outline" onclick="logout()">
                    <i class="fas fa-sign-out-alt"></i> Déconnexion
                </a>
            `;
        }
    });
}

function logout() {
    localStorage.removeItem('token');
    window.location.reload();
}

// ==================== UTILITAIRES ====================
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', { 
        maximumFractionDigits: 0 
    }).format(amount) + ' DH';
}

function formatPercent(value) {
    return value.toFixed(2) + '%';
}

function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    }
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ${message}</div>`;
    }
}

// ==================== API HELPERS ====================
async function apiGet(endpoint) {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(API_URL + endpoint, { headers });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}

async function apiPost(endpoint, data) {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(API_URL + endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}
