.PHONY: setup test lint format typecheck check all

setup:
	uv sync

test:
	uv run pytest -v

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

typecheck:
	uv run mypy src tests

check: format lint typecheck test

run:
	uv run mcp dev src/ee_mcp_demo/server.py
