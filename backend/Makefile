.PHONY: help install dev build clean test lint format venv

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

help:
	@echo "pipelinex backend - makefile commands"
	@echo ""
	@echo "make venv       - create virtual environment"
	@echo "make install    - install dependencies"
	@echo "make dev        - start dev server (port 3001)"
	@echo "make clean      - remove venv & build artifacts"
	@echo "make test       - run tests (when added)"
	@echo "make lint       - run linter (when added)"

venv:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --port 3001

clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage

test:
	$(PYTHON) -m pytest

lint:
	@echo "linting not configured yet"

format:
	@echo "formatter not configured yet"

