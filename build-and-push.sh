#!/bin/bash
# ──────────────────────────────────────────────────────
# i27Academy Demo App — Build & Push Commands
# Run these once to publish to Docker Hub
# github.com/i27academy/devops-interview-series
# ──────────────────────────────────────────────────────

# ── STEP 1: Login to Docker Hub ───────────────────────
docker login
# Enter your Docker Hub username and password

# ── STEP 2: Build v1 ──────────────────────────────────
docker build \
  --build-arg APP_VERSION=v1 \
  -t i27academy/demo-app:v1 \
  -t i27academy/demo-app:latest \
  .

# ── STEP 3: Build v2 ──────────────────────────────────
# v2 differs only in APP_VERSION and APP_COLOR env vars
# Change them in the Dockerfile or pass as build args
docker build \
  --build-arg APP_VERSION=v2 \
  -t i27academy/demo-app:v2 \
  .

# ── STEP 4: Test locally before pushing ───────────────
docker run -d \
  --name i27-test \
  -p 8080:8080 \
  -e APP_VERSION=v1 \
  -e EPISODE=test \
  i27academy/demo-app:v1

# Test all endpoints
curl localhost:8080/
curl localhost:8080/healthz
curl localhost:8080/ready
curl localhost:8080/info

# Test failure simulation
curl localhost:8080/toggle-health
curl localhost:8080/healthz     # should return 500 now
curl localhost:8080/toggle-health
curl localhost:8080/healthz     # back to 200

curl localhost:8080/toggle-ready
curl localhost:8080/ready       # should return 503 now
curl localhost:8080/toggle-ready

# Clean up local test
docker stop i27-test && docker rm i27-test

# ── STEP 5: Push to Docker Hub ────────────────────────
docker push i27academy/demo-app:v1
docker push i27academy/demo-app:v2
docker push i27academy/demo-app:latest

# ── STEP 6: Verify on Docker Hub ─────────────────────
# Visit: https://hub.docker.com/r/i27academy/demo-app

# ── STEP 7: Deploy to GKE ─────────────────────────────
gcloud container clusters get-credentials <cluster> \
  --region <region> --project <project>

kubectl apply -f k8s-manifests.yaml

# Wait for pods
kubectl get pods -n demo -w

# Test from inside cluster
kubectl run test-curl \
  --image=curlimages/curl \
  --restart=Never -it --rm -n demo \
  -- curl http://i27-app-svc/info

# ── USEFUL COMMANDS DURING RECORDING ──────────────────

# Check version running
kubectl exec -n demo \
  $(kubectl get pod -n demo -l app=i27-app \
  -o jsonpath='{.items[0].metadata.name}') \
  -- curl -s localhost:8080/ | python3 -m json.tool

# Trigger readiness failure (for rolling update demo)
kubectl exec -n demo \
  $(kubectl get pod -n demo -l app=i27-app \
  -o jsonpath='{.items[0].metadata.name}') \
  -- curl -s localhost:8080/toggle-ready

# Trigger OOM (for OOMKilled demo)
kubectl exec -n demo \
  $(kubectl get pod -n demo -l app=i27-app \
  -o jsonpath='{.items[0].metadata.name}') \
  -- curl -s localhost:8080/oom

# ── CLEANUP ────────────────────────────────────────────
kubectl delete namespace demo
