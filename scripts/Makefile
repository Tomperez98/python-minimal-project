# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

SHELL = /bin/bash
OS = $(shell uname | tr A-Z a-z)

.PHONY: test
test: ## Run tests
	poetry run pytest --cov-report term-missing --cov=template_project tests/

.PHONY: new-release
new-release: ## Creates a new release
	@./scripts/release.sh

.PHONY: clean
clean: ## Cleans project folder mainly cache
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -f coverage.xml
	rm -rf build
	find tests template_project -empty -type d -delete
	rm coverage.svg


.PHONY: lint
lint: ## Checks code linting
	poetry run black --check .
	poetry run isort --check-only .
	poetry run flake8 template_project/ tests/
	make lint-types

.PHONY: format
format: ## Formats code
	poetry run black .
	poetry run isort .

.PHONY: lint-types
lint-types: ## Lint project types
	poetry run mypy . 

.PHONY: python-versions-badge
python-versions-badge: ## Creates badge so client know supported python versions. (args-> versions (string))
	python -m pybadges --left-text="python" --right-text="$(versions)" --whole-link="https://www.python.org/" --embed-logo --logo='https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg' > badges/python-versions.svg

.PHONY: help
.DEFAULT_GOAL := help
help:
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
