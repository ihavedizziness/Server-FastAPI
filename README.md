# Stats Server

A self-hosted server dashboard for measuring network performance and monitoring system resources in real time.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)
![React](https://img.shields.io/badge/React-19-61dafb)
![Docker](https://img.shields.io/badge/Docker-ready-2496ed)

## Features

- **Download speed test** — stream random data from the server, speed measured client-side
- **Upload speed test** — send random data to the server, speed measured client-side
- **Server internet speed** — run a full `speedtest-cli` test on the server itself (~30s)
- **Live system stats** — CPU, RAM, disk, network I/O, uptime, process count
- **GPU monitoring** — per-GPU utilization, VRAM, and temperature (NVIDIA via pynvml)
- **Alerts** — toast notifications when CPU/RAM/disk/GPU cross critical thresholds
- **Prometheus metrics** — exposed at `/metrics`

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Frontend | React + Vite |
| Metrics | Prometheus + psutil + pynvml |
| Container | Docker (multi-stage build) |
| Orchestration | Kubernetes (k3s) |
| CI/CD | GitHub Actions → GHCR → kubectl |

## Project Structure

```
├── backend/          # FastAPI app
│   ├── routers/      # API endpoints
│   ├── services/     # Business logic (stats, speedtest, upload/download)
│   ├── schemas/      # Pydantic models
│   ├── config.py     # Settings (pydantic-settings, .env support)
│   └── main.py       # App factory
├── frontend/         # React + Vite source
│   └── src/
│       ├── components/
│       ├── hooks/
│       └── utils.js
├── static/           # Built frontend (output of npm run build)
├── k8s/              # Kubernetes manifests
└── Dockerfile        # Multi-stage: Node build → Python serve
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Web UI |
| `GET` | `/download?size_mb=25` | Stream random bytes (1–1000 MB) |
| `POST` | `/upload` | Accept binary upload, return speed result |
| `GET` | `/internet-speed` | Run speedtest-cli on the server |
| `GET` | `/stats` | Live system metrics (JSON) |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/docs` | Swagger UI |

## Running Locally

### With Docker

```bash
docker compose up
```

Open [http://localhost:8000](http://localhost:8000)

### Without Docker

**Backend:**
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Frontend (dev server with hot reload):**
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173/static/](http://localhost:5173/static/)

**Frontend (production build):**
```bash
cd frontend
npm run build   # outputs to static/
```

## Configuration

Settings are read from environment variables or a `.env` file:

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Stats Server` | Application name |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Port |
| `MAX_DOWNLOAD_MB` | `1000` | Max download test size |
| `MAX_UPLOAD_MB` | `500` | Max upload test size |
| `SPEEDTEST_THREADS` | `4` | Parallel threads for speedtest-cli |
| `CHUNK_SIZE_BYTES` | `262144` | Download stream chunk size (256 KB) |

## Deployment

The CI/CD pipeline runs on every push to `main`:

1. **Lint & type check** — ruff + mypy
2. **Build & push** — Docker image → `ghcr.io/ihavedizziness/server-fastapi`
3. **Deploy** — `kubectl set image` rolling update on the k8s cluster via SSH

### Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

### GPU Support

The Docker Compose file enables NVIDIA GPU passthrough. Requires the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) on the host.

## License

MIT
