# pull official base image
FROM python:3.14-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables (key=value format)
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=prod

# Install system dependencies (curl needed for uv)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install uv using the official script
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && mv /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

# activate virtual env
ARG VIRTUAL_ENV=/app/.venv
ENV PATH=/app/.venv/bin:$PATH

# install dependencies (layer cached as long as pyproject.toml/uv.lock unchanged)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# copy project
COPY . /app

# create data directory for sqlite and logs directory
RUN mkdir -p /app/data /app/logs

# expose port for granian
EXPOSE 80

# run entrypoint
CMD ["sh", "./entrypoint.sh"]
