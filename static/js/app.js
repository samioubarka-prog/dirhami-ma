// ========== AUTH ==========
let currentUser = null;
let authToken = localStorage.getItem('dirhami_token');

function showLogin() {
    const modal = document.getElementById('auth-modal');
    const form = document.getElementById('auth-form');

    form.innerHTML = `
        <div class="auth-form">
            <h2>Connexion</h2>
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="login-email" required placeholder="votre@email.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="login-password" required placeholder="••••••••">
                </div>
                <button type="submit" class="btn btn-primary btn-lg">Se connecter</button>
            </form>
            <p class="auth-switch">
                Pas encore de compte ? <a onclick="showRegister()">S'inscrire</a>
            </p>
        </div>
    `;

    modal.classList.add('active');
}

function showRegister() {
    const modal = document.getElementById('auth-modal');
    const form = document.getElementById('auth-form');

    form.innerHTML = `
        <div class="auth-form">
            <h2>Inscription</h2>
            <form onsubmit="handleRegister(event)">
                <div class="form-group">
                    <label>Nom complet</label>
                    <input type="text" id="reg-name" required placeholder="Votre nom">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="reg-email" required placeholder="votre@email.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="reg-password" required placeholder="Min. 8 caracteres" minlength="8">
                </div>
                <div class="form-group">
                    <label>Telephone (optionnel)</label>
                    <input type="tel" id="reg-phone" placeholder="+212 6XX XXX XXX">
                </div>
                <div class="form-group">
                    <label>Ville (optionnel)</label>
                    <input type="text" id="reg-city" placeholder="Casablanca">
                </div>
                <button type="submit" class="btn btn-primary btn-lg">Creer mon compte</button>
            </form>
            <p class="auth-switch">
                Deja un compte ? <a onclick="showLogin()">Se connecter</a>
            </p>
        </div>
    `;

    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('auth-modal').classList.remove('active');
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const res = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('dirhami_token', data.access_token);
            authToken = data.access_token;
            closeModal();
            checkAuth();
            alert('Connexion reussie !');
        } else {
            alert('Email ou mot de passe incorrect.');
        }
    } catch (e) {
        alert('Erreur de connexion.');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const data = {
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value,
        full_name: document.getElementById('reg-name').value,
        phone: document.getElementById('reg-phone').value || null,
        city: document.getElementById('reg-city').value || null
    };

    try {
        const res = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        if (res.ok) {
            const result = await res.json();
            localStorage.setItem('dirhami_token', result.access_token);
            authToken = result.access_token;
            closeModal();
            checkAuth();
            alert('Compte cree avec succes !');
        } else {
            const err = await res.json();
            alert(err.detail || 'Erreur lors de l'inscription.');
        }
    } catch (e) {
        alert('Erreur de connexion.');
    }
}

function logout() {
    localStorage.removeItem('dirhami_token');
    authToken = null;
    currentUser = null;
    checkAuth();
    window.location.reload();
}

async function checkAuth() {
    const token = localStorage.getItem('dirhami_token');
    if (!token) {
        document.getElementById('nav-actions').style.display = 'flex';
        document.getElementById('nav-user').style.display = 'none';
        return;
    }

    try {
        const res = await fetch('/api/auth/me', {
            headers: {'Authorization': 'Bearer ' + token}
        });

        if (res.ok) {
            const user = await res.json();
            currentUser = user;
            document.getElementById('nav-actions').style.display = 'none';
            document.getElementById('nav-user').style.display = 'flex';
            document.getElementById('user-name').textContent = user.full_name;
        } else {
            localStorage.removeItem('dirhami_token');
        }
    } catch (e) {
        console.error('Auth check error:', e);
    }
}

// ========== MOBILE MENU ==========
function toggleMenu() {
    const nav = document.getElementById('nav-links');
    nav.classList.toggle('mobile-active');
}

// ========== LOAD ARTICLES ON HOMEPAGE ==========
async function loadHomeArticles() {
    const grid = document.getElementById('articles-grid');
    if (!grid) return;

    try {
        const res = await fetch('/api/blog/?limit=3');
        const articles = await res.json();

        grid.innerHTML = articles.map(art => `
            <article class="article-card">
                <div class="article-image" style="background: linear-gradient(135deg, #1a5f2a 0%, #2d8a3e 100%);">
                    <span class="article-category">${art.category}</span>
                </div>
                <div class="article-content">
                    <h3><a href="/article.html?slug=${art.slug}">${art.title}</a></h3>
                    <p>${art.excerpt.substring(0, 120)}...</p>
                    <div class="article-meta">
                        <span>${art.author}</span>
                        <span>${new Date(art.published_at).toLocaleDateString('fr-FR')}</span>
                    </div>
                </div>
            </article>
        `).join('');
    } catch (e) {
        console.error('Erreur chargement articles home:', e);
    }
}

// ========== ANIMATE STATS ==========
function animateStats() {
    const stat = document.getElementById('stat-sims');
    if (!stat) return;

    let count = 0;
    const target = 12547;
    const duration = 2000;
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        count += increment;
        if (count >= target) {
            count = target;
            clearInterval(timer);
        }
        stat.textContent = Math.floor(count).toLocaleString('fr-FR');
    }, 16);
}

// ========== INIT ==========
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadHomeArticles();

    // Animate stats when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats();
                observer.unobserve(entry.target);
            }
        });
    });

    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) observer.observe(statsSection);

    // Close modal on outside click
    document.getElementById('auth-modal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('auth-modal')) {
            closeModal();
        }
    });
});
