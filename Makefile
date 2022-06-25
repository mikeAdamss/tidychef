.PHONY: all

help:
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests and update your test coverage statistics
    poetry run coverage run -m pytest

coverage: ## View test coverage statistics
    poetry run coverage report -m

coveragehtml: ## Create html report of test coverage, accssible at ./htmlcov/index.html
    poetry run coverage html

isort: ## Run isort to sort out the imports
    poetry run isort ./*

black: ## Format the code base with black
    poetry run black ./*

pyright: ## Run pyright against the code base
    poetry run pyright . --lib