PROJECT_NAME=prompt-eval-platform
TAG?=dev
REGISTRY?=local
IMAGE_API=$(REGISTRY)/$(PROJECT_NAME)-prompt-hub:$(TAG)
IMAGE_RUNNER=$(REGISTRY)/$(PROJECT_NAME)-eval-runner:$(TAG)

.PHONY: build push test seed eval fmt

build:
\tdocker build -t $(IMAGE_API) services/prompt-hub
\tdocker build -t $(IMAGE_RUNNER) services/eval-runner

push:
\tdocker push $(IMAGE_API)
\tdocker push $(IMAGE_RUNNER)

test:
\tuv run -q -p ./services/prompt-hub pytest -q || true
\tuv run -q -p ./services/eval-runner pytest -q || true

seed:
\tuv run python scripts/seed_testset.py --dsn "$(POSTGRES_DSN)" --s3 s3://prompt-hub/testsets/

eval:
\tuv run python services/eval-runner/eval_cli.py --config configs/eval/sample-eval.yaml

fmt:
\tuv run ruff format services
\tuv run ruff check --fix services
