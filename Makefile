.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Installs datacheck into a poetry venv 
	poetry install

test: install ## Run all unit tests and create new coverage report
	poetry run pytest --cov-report term-missing --cov=datachef --cov-fail-under=100 ./tests/

format: ## Format the codebase with isort and black
	poetry run isort ./* && poetry run black ./*

checkimports: install ## Use pylint to check for unused imports
	poetry run pylint ./datachef | grep "unused-import"

pylint: install ## Run pylint
	poetry run pylint ./datachef

book: ## Create the jupyter book in /jupyterbook/_build
	rm -rf ./jupyterbook/_build
	rm -rf ./jupyterbook/venv
	python -m venv ./jupyterbook/venv
	. ./jupyterbook/venv/bin/activate
	pip install .
	jupyter-book build jupyterbook/ --all

publish: ## Publish the jupyter book to github pages
	poetry run pip install ghp-import
	ghp-import -n -p -f ./jupyterbook/_build/html
