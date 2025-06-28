# Use a lightweight Python base image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY src ./src

# Install dependencies using uv
# We install dev dependencies as well for linting/testing in CI/CD, but for production, you might want to remove [dev]
RUN uv pip install --system -e ".[dev]"

# Command to run the application
# This assumes your bot's main entry point is src/main.py
CMD ["uv", "run", "python", "src/main.py"]
