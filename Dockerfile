FROM python:3.12-slim

# Update and upgrade system packages
RUN set -ex \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /src

# Copy requirements file
COPY ./src/requirements.txt .

# Install Python dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv pip install -r requirements.txt --system

# Copy source code
COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
