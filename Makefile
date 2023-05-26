.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Installs datacheck into a poetry venv 
	poetry install

test: install ## Run all unit tests and create new coverage report
	poetry run pytest --cov-report term-missing --cov=datachef --cov-fail-under=100 ./tests/

scenarios: install ## Run our scenario notebooks, make sure the output matches whats expected
	poetry run pytest -rx ./scenarios

report: install ## View the latest report of test coverage (includes missing coverage by line)
	poetry run coverage report -m

format: ## Format the codebase with isort and black
	poetry run isort ./* && poetry run black ./*

docs: install ## Combines auto API docs and contents of _docs and serves it locally for preview.
	poetry run python3 ./expand_docs.py
	poetry run pdoc -html ./datachef --output-dir ./docs
	cp -a ./scenarios/html_scenario_fixtures/ ./docs/
	cp ./_docs/splashpage.md ./docs/splashpage.md
	cd docs && python3 -m http.server

pyrightbuild: ## Build our docker image for running pyright
	docker build -t pyrightimage ./images

pyright: ## Run pyright through docker
	docker run -v $(PWD):/workspace -w /workspace -it pyrightimage /bin/bash -c "poetry run pyright ./datachef --lib"

checkimports: install ## Use pylint to check for unused imports
	poetry run pylint ./datachef | grep "unused-import"

pylint: install ## Run pylint
	poetry run pylint ./datachef

unbundle: install ## Unbundle (unzip) html and ipynb test resources
	poetry run python3 ./resources/bundler.py unbundle

bundle: install ## Bundle (zip) html and ipynb test resources
	poetry run python3 ./resources/bundler.py bundle

jupyter: ## Open up a jupyter lab to view the scenarios (this will occupy your termaial)
	poetry run jupyter lab