// Auth UI Manager
function updateAuthUI() {
    const user = api.getUser();
    const authContainer = document.getElementById('auth-container');
    if (!authContainer) return;

    if (api.isLoggedIn() && user) {
        authContainer.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-outline-light dropdown-toggle" data-bs-toggle="dropdown">
                    👤 ${user.full_name || user.email}
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#" onclick="showSimulations()">Mes simulations</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="#" onclick="logout()">Déconnexion</a></li>
                </ul>
            </div>
        `;
    } else {
        authContainer.innerHTML = `
            <button class="btn btn-outline-light" onclick="showLoginModal()">Connexion</button>
        `;
    }
}

function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
}

function hideLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        await api.login(email, password);
        hideLoginModal();
        updateAuthUI();
        alert('Connexion réussie !');
    } catch (err) {
        alert('Erreur: ' + err.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const fullName = document.getElementById('register-name').value;

    try {
        await api.register(email, password, fullName);
        await api.login(email, password);
        hideLoginModal();
        updateAuthUI();
        alert('Inscription réussie !');
    } catch (err) {
        alert('Erreur: ' + err.message);
    }
}

function logout() {
    api.logout();
    updateAuthUI();
    window.location.reload();
}

async function showSimulations() {
    if (!api.isLoggedIn()) {
        showLoginModal();
        return;
    }
    try {
        const sims = await api.getSimulations();
        console.log('Mes simulations:', sims);
        alert(`${sims.length} simulation(s) sauvegardée(s)`);
    } catch (err) {
        alert('Erreur: ' + err.message);
    }
}

document.addEventListener('DOMContentLoaded', updateAuthUI);
