FROM ubuntu:24.04

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python 3.13 into a fixed path inside the container
ENV UV_PYTHON_INSTALL_DIR=/opt/python
RUN uv python install 3.13

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy source
COPY . .

# Create log directory
RUN mkdir -p var/log/

# Create non-root user and hand over ownership
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Gunicorn manages worker processes; each worker is a full uvicorn ASGI process.
CMD ["gunicorn", "app:app"]
