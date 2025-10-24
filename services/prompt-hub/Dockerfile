FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml /app/
RUN uv pip install -r <(uv pip compile pyproject.toml -q) --system
COPY app /app/app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
