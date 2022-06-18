.PHONY: all

# Bash madness that creates a help menu on a naked make
help:
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests and update your test coverage statistics
    poetry run coverage run -m pytest

coverage: ## View test coverage statistics
    coverage report -m

black: ## Format the code base with black
    black ./*

pyright: ## Run pyright against the code base
    pyright . --lib