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
RUN uv pip install --system -e "."

# Command to run the application
# This assumes your bot's main entry point is src/main.py
CMD ["uv", "run", "python", "src/main.py"]
