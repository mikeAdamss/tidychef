.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run all unit tests and create new coverage report
	poetry run pytest --cov=datachef --cov-fail-under=100 tests/

scenarios: ## Run our scenario notebooks, make sure the output matches whats expected
	poetry run pytest ./scenarios

report: ## View the latest report of test coverage (includes missing coverage by line)
	poetry run coverage report -m

format: ## Format the codebase with isort and black
	poetry run isort ./* && poetry run black ./*

docs: ## Combines auto API docs and contents of _docs and serves it locally for preview.
	poetry run python3 ./expand_docs.py
	poetry run pdoc -html ./datachef --output-dir ./docs
	cp -a ./scenarios/expected/ ./docs/
	cp ./_docs/splashpage.md ./docs/splashpage.md
	cd docs && python3 -m http.server

pyrightbuild: ## Build our docker image for running pyright
	docker build -t pyrightimage ./images

pyright: ## Run pyright through docker
	docker run -v $(PWD):/workspace -w /workspace -it pyrightimage /bin/bash -c "poetry run pyright ./datachef --lib"

checkimports: ## Use pylint to check for unused imports
	poetry run pylint ./datachef | grep "unused-import"

pylint: ## Run pylint
	poetry run pylint ./datachef