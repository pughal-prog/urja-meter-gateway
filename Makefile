.PHONY: install run test lint openapi clean help

help:
	@echo "Available commands:"
	@echo "  make install   Install dependencies in editable mode with dev tools"
	@echo "  make run       Start the FastAPI development server"
	@echo "  make test      Run pytest suite"
	@echo "  make lint      Run ruff linter and style check"
	@echo "  make openapi   Regenerate openapi.json from FastAPI app"
	@echo "  make clean     Clean temporary build and cache files"

install:
	pip install -e ".[dev]"

run:
	uvicorn urja_api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

lint:
	ruff check src tests scripts

openapi:
	python scripts/export_openapi.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
