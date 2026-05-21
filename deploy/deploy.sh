#!/bin/bash
# Script de déploiement Dirhami sur Hostinger VPS

echo "🚀 Déploiement de Dirhami..."

# Mise à jour du système
apt update && apt upgrade -y

# Installation des dépendances
apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git curl

# Configuration PostgreSQL
echo "🔧 Configuration PostgreSQL..."
sudo -u postgres psql -c "CREATE USER dirhami_user WITH PASSWORD 'CHANGEZ_CE_MOT_DE_PASSE';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE dirhami_db OWNER dirhami_user;" 2>/dev/null || true

# Création du répertoire
mkdir -p /var/www/dirhami

# Copie des fichiers (à adapter selon votre méthode de déploiement)
# git clone https://github.com/votre-compte/dirhami.git /var/www/dirhami

cd /var/www/dirhami/backend

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configuration .env
cat > .env << EOF
DATABASE_URL=postgresql://dirhami_user:CHANGEZ_CE_MOT_DE_PASSE@localhost:5432/dirhami_db
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://dirhami.ma
DEBUG=False
EOF

# Service systemd
cat > /etc/systemd/system/dirhami.service << 'EOF'
[Unit]
Description=Dirhami API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dirhami/backend
Environment="PATH=/var/www/dirhami/backend/venv/bin"
EnvironmentFile=/var/www/dirhami/backend/.env
ExecStart=/var/www/dirhami/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configuration Nginx
cat > /etc/nginx/sites-available/dirhami << 'EOF'
server {
    listen 80;
    server_name dirhami.ma www.dirhami.ma;

    location / {
        root /var/www/dirhami/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/docs {
        proxy_pass http://localhost:8000/api/docs;
    }

    location /api/redoc {
        proxy_pass http://localhost:8000/api/redoc;
    }
}
EOF

# Activation
ln -sf /etc/nginx/sites-available/dirhami /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Démarrage des services
systemctl daemon-reload
systemctl enable dirhami
systemctl start dirhami
systemctl restart nginx

echo "✅ Déploiement terminé !"
echo "🌐 Votre site est accessible sur http://dirhami.ma"
echo "📚 API Docs: http://dirhami.ma/api/docs"
echo ""
echo "⚠️  N'oubliez pas de:"
echo "   1. Configurer SSL avec: certbot --nginx -d dirhami.ma"
echo "   2. Changer le mot de passe PostgreSQL"
echo "   3. Mettre à jour le SECRET_KEY dans .env"
