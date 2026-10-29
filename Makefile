.DEFAULT_GOAL := help

.PHONY: help format lint test build run clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-8s %s\n", $$1, $$2}'

format: ## Format with ruff
	uv run ruff format src/ tests/

lint: format ## Lint with ruff (auto-fix)
	uv run ruff check --fix src/ tests/

test: ## Run the test suite
	uv run pytest -q

build: ## Build the wheel
	uv build

run: ## Show the CLI help
	uv run naver-cli --help

clean: ## Remove build and cache artifacts
	rm -rf dist build .pytest_cache .ruff_cache
