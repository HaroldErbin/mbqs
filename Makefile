install-dev:
	uv sync --extra dev
	pre-commit install

check:
	ruff check .

	@echo ""
	ruff format --check .

	@echo ""
	ty check

format:
	ruff check --fix .
	ruff format .

test:
	uv run pytest
