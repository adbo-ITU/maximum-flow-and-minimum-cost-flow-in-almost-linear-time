update:
	poetry update
	poetry install

install:
	poetry check
	poetry install

ruff:
	poetry run ruff check -e --output-format=github .
	poetry run ruff format --check --diff  .


test:
	poetry run pytest

run:
	poetry run python3 main.py

