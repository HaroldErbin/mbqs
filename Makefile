.PHONY: install-dev, check, format, test, examples

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

examples:
	mbqs protocol -J 1. -L 4 -o examples/protocol_single.json
	mbqs protocol -J 1. -L $(shell seq 4 6) -o examples/protocol_multiple.json
	mbqs protocol -J 1. -L 4 --include-rydberg -o examples/protocol_single_rydberg.json
	mbqs protocol -J 1. -L $(shell seq 4 6) --include-rydberg -o examples/protocol_multiple_rydberg.json
	mbqs correlations -i examples/samples.json -o examples/correlations_samples.json
	mbqs correlations -J 1. -L 4 -o examples/correlations_exact.json
