FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
