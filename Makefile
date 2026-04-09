install-dev:
	uv sync --extra dev
	pre-commit install

check:
	ruff check .
	ruff format --format .

format:
	ruff check --fix .
	ruff format .

test:
	uv run pytest
