# Dirhami - Deploy on Render

## Si le deploy echoue (Exited with status 1)

### Etape 1: Modifier le Start Command sur Render

1. Allez sur votre service Render → **Settings**
2. Trouvez **Start Command**
3. Remplacez par:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
   ```
4. Cliquez **Save Changes**
5. **Manual Deploy** → **Deploy latest commit**

### Etape 2: Si ca plante encore, activer le Shell

1. Render Dashboard → votre service → **Shell** (onglet en haut)
2. Tapez:
   ```bash
   python -c "import sys; print(sys.version)"
   python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine); print('DB OK')"
   python -c "from app.routers import auth; print('Auth OK')"
   ```
3. Envoyez-moi le message d'erreur exact

### Etape 3: Forcer Python 3.11 (si possible)

1. Settings → **Environment**
2. Ajoutez:
   - `PYTHON_VERSION` = `3.11.0`
3. **Manual Deploy** → **Clear build cache & deploy**

## Fichiers modifiables directement

- `start.sh` - Script de demarrage
- `render.yaml` - Configuration Render
