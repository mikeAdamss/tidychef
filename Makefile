.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:
	poetry install
	
test: install ## Run all unit tests and view coverage report
	poetry run pytest --cov-report term-missing --cov=datachef --cov-fail-under=100 ./tests/

format: ## Format the codebase with isort and black
	rm -rf ./jupyterbook/venv
	rm -rf ./jupyterbook/pdoc_venv
	poetry run isort ./* && poetry run black ./*

checkimports: install ## Use pylint to check for unused imports
	poetry run pylint ./datachef | grep "unused-import"

book: ## Create the jupyter book in /jupyterbook/_build
	rm -rf ./jupyterbook/_build
	rm -rf ./jupyterbook/venv
	python -m venv ./jupyterbook/venv
	. ./jupyterbook/venv/bin/activate
	pip install .
	pip install jupyter-book
	jupyter-book build jupyterbook/ --all

	python -m venv ./jupyterbook/pdoc_venv
	. ./jupyterbook/pdoc_venv/bin/activate
	pip install pdoc
	pdoc ./datachef -o ./jupyterbook/_build/html/api_docs

push_docs: ## Publish the jupyter book to github pages
	poetry run pip install ghp-import
	poetry run ghp-import -n -p -f ./jupyterbook/_build/html

tox: install ## Use tox to run tests against all python versions
	poetry run tox