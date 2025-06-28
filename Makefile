.PHONY: lint/fix
lint/fix:
	uv run ruff check --fix
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check
	uv run ruff format --check
	uv run mypy src

.PHONY: run
run:
	set -o allexport; . ./.env; set +o allexport && \
	PYTHONPATH="src" uv run python src/main.py
