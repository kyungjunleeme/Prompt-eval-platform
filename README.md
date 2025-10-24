# Prompt Hub + Multi‑LLM Eval Platform (EKS/NKS/IDC/Databricks)

End-to-end template to **collect prompts**, **run multi‑model evaluations**, and **observe cost/latency/quality** across AWS EKS, Naver Cloud NKS, internal IDC, and Databricks.

## Quick start

```bash
# 0) Prereqs: uv (or pip), Docker, kubectl, kustomize, helm
# 1) Build images
make build

# 2) Run unit tests
make test

# 3) Package and push images (configure REGISTRY and TAG)
make push REGISTRY=registry.example.com/myproj TAG=dev

# 4) Deploy to EKS/NKS/IDC (choose overlay)
kubectl apply -k configs/k8s/overlays/eks
# or
kubectl apply -k configs/k8s/overlays/nks
# or
kubectl apply -k configs/k8s/overlays/idc

# 5) Seed DB + sample testset
make seed

# 6) Submit an evaluation (uses sample-eval.yaml)
make eval
```

## Components
- **services/prompt-hub**: FastAPI service for prompt/testset/runs (Postgres meta + S3/MinIO for artifacts).
- **services/eval-runner**: Batch worker that pulls eval-configs and runs A/B/n tests against providers.
- **configs/k8s**: Kustomize base + overlays for EKS/NKS/IDC. Includes Ingress, HPA, Secrets templates.
- **db/migrations**: Minimal schema for meta tables.
- **observability**: Example Grafana dashboards, ClickHouse sink (optional).

## Providers supported (out of the box stubs)
- OpenAI, Anthropic, Google (Gemini), AWS Bedrock, Azure OpenAI
- **Databricks Model Serving** (via personal access token) 
- Local **vLLM** (optional deployment manifest included)

---

> ⚠️ Replace placeholder domains, registries, and credentials in `.env` and K8s Secret templates.
