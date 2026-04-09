install-dev:
	uv sync --extra dev
	pre-commit install

check:
	ruff check .

	@echo ""
	ruff format --check .

	@echo ""
	mypy src/mbqs

format:
	ruff check --fix .
	ruff format .

test:
	uv run pytest
