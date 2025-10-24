FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml /app/
RUN uv pip install -r <(uv pip compile pyproject.toml -q) --system
COPY eval_cli.py providers.py scorers.py /app/
CMD ["python", "eval_cli.py", "--config", "/config/eval.yaml"]
