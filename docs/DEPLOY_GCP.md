# Deploy Cargo Pulse on a GCP Compute Engine VM

Cargo Pulse runs as **Docker Compose** (Postgres + Django/Gunicorn) behind **host nginx** on ports 80/443.

## Architecture

```text
Browser → nginx (:80 / :443) → Docker web (:8000) → Postgres (internal)
```

Static assets are served by **WhiteNoise** inside Django (no separate static container).

---

## 1. Create the GCP VM

| Setting | Suggested value |
|---------|-----------------|
| Project | `CargoPulse` (or your billing project) |
| Name | `cargopulse` |
| Region | `us-central1-a` (or nearest to users) |
| Machine | `e2-medium` (2 vCPU, 4 GB RAM) |
| OS | Debian 12 or 13 |
| Boot disk | 20 GB |
| Firewall | Allow HTTP + HTTPS |

Reserve a **static external IP** and point DNS when ready:

- `cargopulse.mx` → VM IP  
- `www.cargopulse.mx` → VM IP  

---

## 2. One-time VM setup (SSH)

```bash
# As your deploy user (e.g. trading_bot)
sudo apt-get update
sudo apt-get install -y git nginx certbot python3-certbot-nginx

# Docker (official convenience script)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# Log out and back in so docker group applies

# Docker Compose plugin
sudo apt-get install -y docker-compose-plugin
```

---

## 3. Clone and configure

```bash
cd ~
git clone https://github.com/YOUR_ORG/CargoPulse.git
cd CargoPulse/docker

cp .env.example .env
nano .env
```

Set at minimum:

```env
SECRET_KEY=<long-random-string>
DEBUG=False
USE_HTTPS=True
ALLOWED_HOSTS=cargopulse.mx,www.cargopulse.mx,YOUR_VM_EXTERNAL_IP
CSRF_TRUSTED_ORIGINS=https://cargopulse.mx,https://www.cargopulse.mx
POSTGRES_PASSWORD=<strong-db-password>
GOOGLE_MAPS_API_KEY=<your-maps-javascript-api-key>
```

For **local Docker** on your Mac, keep `DEBUG=True`, `USE_HTTPS=False`, and include `http://127.0.0.1:8000` in `CSRF_TRUSTED_ORIGINS` (see `.env.example`).

### Google Maps address autocomplete

Address fields on **carrier signup** and **post equipment** use Google Places Autocomplete when `GOOGLE_MAPS_API_KEY` is set.

In [Google Cloud Console](https://console.cloud.google.com/google/maps-apis) (same project as the VM):

1. Enable **Maps JavaScript API**, **Places API**, and **Places API (New)**
2. Create an API key (or reuse an existing one)
3. Restrict the key:
   - **Application restrictions:** HTTP referrers  
     `https://cargopulse.mx/*`, `https://www.cargopulse.mx/*`, `http://127.0.0.1:8000/*` (local dev)
   - **API restrictions:** Maps JavaScript API + Places API + **Places API (New)**
4. Add to `docker/.env`:

```env
GOOGLE_MAPS_API_KEY=AIza...
```

Rebuild: `docker compose up -d --build`

Generate a secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 4. Start the stack

```bash
cd ~/CargoPulse/docker
chmod +x run.sh entrypoint.sh
./run.sh
```

Verify:

```bash
curl -sI http://127.0.0.1:8000/ | head -5
docker compose ps
docker compose logs -f web
```

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 5. nginx reverse proxy

```bash
sudo cp ~/CargoPulse/docker/nginx/cargopulse.conf /etc/nginx/sites-available/cargopulse
sudo ln -sf /etc/nginx/sites-available/cargopulse /etc/nginx/sites-enabled/cargopulse

# Edit server_name if you are testing by IP first:
# sudo nano /etc/nginx/sites-available/cargopulse

sudo nginx -t && sudo systemctl reload nginx
```

Open `http://YOUR_VM_IP/` in a browser.

---

## 6. HTTPS (when DNS is live)

```bash
sudo certbot --nginx -d cargopulse.mx -d www.cargopulse.mx
```

Certbot updates nginx for SSL. Ensure `CSRF_TRUSTED_ORIGINS` in `.env` uses `https://`.

Reload after env changes:

```bash
cd ~/CargoPulse/docker
docker compose up -d --build
```

---

## 7. Deploy updates

```bash
cd ~/CargoPulse
git pull origin main

cd docker
docker compose up -d --build
```

Migrations run automatically on container start via `docker/entrypoint.sh`.

---

## 8. Firewall (GCP console)

| Rule | Ports | Source |
|------|-------|--------|
| `allow-http` | tcp:80 | `0.0.0.0/0` |
| `allow-https` | tcp:443 | `0.0.0.0/0` |

Do **not** expose Postgres (5432) publicly.

---

## Local Docker (Mac)

```bash
cd CargoPulse/docker
./run-dev.sh          # dev: live code + runserver
# or
./run.sh              # prod-like: Gunicorn + Postgres
```

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| `502 Bad Gateway` | `docker compose ps` — is `web` up? `curl http://127.0.0.1:8000/` |
| CSRF error on login | Add your `https://` origin to `CSRF_TRUSTED_ORIGINS` |
| `DisallowedHost` | Add domain/IP to `ALLOWED_HOSTS` in `docker/.env`, restart web |
| Disk full | `docker system prune` (careful), expand boot disk in GCP |

---

## Files

| Path | Purpose |
|------|---------|
| `docker/Dockerfile` | Python 3.12 image + Gunicorn |
| `docker/docker-compose.yml` | Production stack |
| `docker/docker-compose.dev.yml` | Dev override (code mount) |
| `docker/entrypoint.sh` | migrate + collectstatic |
| `docker/.env.example` | Environment template |
| `docker/nginx/cargopulse.conf` | Host nginx site |
