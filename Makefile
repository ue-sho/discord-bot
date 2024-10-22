.PHONY: lint/fix
lint/fix:
	rye lint --fix
	rye fmt

.PHONY: lint
lint:
	rye lint
	rye fmt --check
	rye run mypy --explicit-package-bases src tests

.PHONY: test
test:
	set -o allexport; . ./.test.env; set +o allexport && rye test

.PHONY: run
run:
	set -o allexport; . ./.env; set +o allexport && \
	PYTHONPATH="src" rye run python src/main.py