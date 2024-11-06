update:
	poetry update
	poetry install

build:
	cd min_ratio && poetry -C ../ run maturin build --release

install:
	poetry check
	poetry install

ruff:
	poetry run ruff check -e --output-format=github .
	poetry run ruff format --check --diff  .


test:
	$(MAKE) build
	poetry run pytest

run:
	$(MAKE) build
	poetry run python3 main.py

