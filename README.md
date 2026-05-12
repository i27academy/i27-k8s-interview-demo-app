# i27Academy Demo App

Custom demo application used across the
**Kubernetes Interview Series** on YouTube.

**Channel:** youtube.com/@i27academy
**Series:** github.com/i27academy/devops-interview-series

---

## Why this app exists

Every episode was using `nginx` as a demo app.
nginx has no `/healthz` endpoint, no version info,
no way to simulate failures cleanly.

This app is built specifically for the series —
branded, realistic, and designed to reproduce
every common Kubernetes production scenario.

---

## Docker Hub

```bash
docker pull i27academy/demo-app:v1
docker pull i27academy/demo-app:v2
```

---

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | App home — version, color, uptime |
| `/healthz` | GET | Liveness probe — returns 200 or 500 |
| `/ready` | GET | Readiness probe — returns 200 or 503 |
| `/info` | GET | Full app info + all endpoints |
| `/crash` | GET | Simulates crash — exit code 1 |
| `/oom` | GET | Simulates OOMKilled — eats memory |
| `/slow` | GET | Simulates slow response — 30s delay |
| `/toggle-health` | GET | Toggles liveness probe pass/fail |
| `/toggle-ready` | GET | Toggles readiness probe pass/fail |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_VERSION` | `v1` | Version shown in responses |
| `APP_COLOR` | `orange` | v1=orange, v2=blue |
| `APP_ENV` | `production` | Environment name |
| `EPISODE` | `demo` | Episode reference |
| `PORT` | `8080` | Port to listen on |

---

## Quick start on GKE

```bash
# Deploy v1
kubectl apply -f k8s-manifests.yaml

# Check it is running
kubectl get pods -n demo

# Hit the app
kubectl run curl --image=curlimages/curl \
  --restart=Never -it --rm -n demo \
  -- curl http://i27-app-svc/info

# Update to v2
kubectl set image deployment/i27-app \
  app=i27academy/demo-app:v2 -n demo

# Cleanup
kubectl delete namespace demo
```

---

## Scenarios this app covers

| Episode | Scenario | How |
|---|---|---|
| Pods Q1 | CrashLoopBackOff | Broken liveness probe path |
| Pods Q5 | App not responding | App on 0.0.0.0 vs 127.0.0.1 |
| Pods Q6 | OOMKilled | Hit `/oom` + low memory limit |
| Deployments Q7 | Drain stuck | PDB blocking eviction |
| Deployments Q8 | Rollout frozen | `/toggle-ready` on new pods |
| Probes deep dive | All probe types | `/healthz` `/ready` `/slow` |

---

## Build locally

```bash
git clone github.com/i27academy/devops-interview-series
cd demo-app

docker build -t i27academy/demo-app:v1 .
docker run -p 8080:8080 i27academy/demo-app:v1

curl localhost:8080/info
```

---

**i27Academy © 2026 — helping you prepare for real jobs**
