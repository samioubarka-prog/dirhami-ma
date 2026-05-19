// API Client Dirhami - Connexion au backend FastAPI
const API_BASE_URL = window.location.hostname.includes('localhost') 
    ? 'http://localhost:8000/api/v1' 
    : 'https://dirhami-backend.onrender.com/api/v1';

class DirhamiAPI {
    constructor() {
        this.token = localStorage.getItem('dirhami_token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(url, {
            ...options,
            headers
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Erreur serveur' }));
            throw new Error(error.detail || 'Erreur réseau');
        }
        return response.json();
    }

    // Auth
    async register(email, password, fullName = '') {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password, full_name: fullName })
        });
    }

    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        const data = await response.json();
        if (data.access_token) {
            this.token = data.access_token;
            localStorage.setItem('dirhami_token', data.access_token);
            localStorage.setItem('dirhami_user', JSON.stringify(data.user));
        }
        return data;
    }

    logout() {
        this.token = null;
        localStorage.removeItem('dirhami_token');
        localStorage.removeItem('dirhami_user');
    }

    isLoggedIn() {
        return !!this.token;
    }

    getUser() {
        const user = localStorage.getItem('dirhami_user');
        return user ? JSON.parse(user) : null;
    }

    // Cartes
    async getCartes(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/cartes/?${params}`);
    }

    // OPCVM
    async getOPCVM(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/opcvm/?${params}`);
    }

    // Calculators (public)
    async calculateCredit(data) {
        return this.request('/calculators/credit', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async calculateRetraite(data) {
        return this.request('/calculators/retraite', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async calculateBudget(data) {
        return this.request('/calculators/budget', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async calculateOPCVMSim(data) {
        return this.request('/calculators/opcvm-sim', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Simulations (auth required)
    async saveSimulation(type, name, data, result) {
        return this.request('/simulations/', {
            method: 'POST',
            body: JSON.stringify({ type, name, data: JSON.stringify(data), result: JSON.stringify(result) })
        });
    }

    async getSimulations() {
        return this.request('/simulations/');
    }

    // Blog
    async getArticles(categorie = null) {
        const params = categorie ? `?categorie=${categorie}` : '';
        return this.request(`/blog/${params}`);
    }
}

const api = new DirhamiAPI();
