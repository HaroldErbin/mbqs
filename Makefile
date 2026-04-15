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
	pytest

refresh-examples:
	mbqs protocol -J 1. -L 4 --json examples/protocol_single.json
	mbqs protocol -J 1. -L {4..6} --json examples/protocol_multiple.json
	mbqs protocol -J 1. -L 4 --include-rydberg --json examples/protocol_single_rydberg.json
	mbqs protocol -J 1. -L {4..6} --include-rydberg --json examples/protocol_multiple_rydberg.json
	mbqs correlations -i examples/samples.json -o examples/correlations.json
