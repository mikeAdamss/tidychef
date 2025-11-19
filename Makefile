.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:
	poetry install
	
test: install ## Run all unit tests and view coverage report
	poetry run pytest --cov-report term-missing --cov=tidychef --cov-fail-under=100 ./tests/

fmt: ## Format the codebase with isort and black
	rm -rf ./jupyterbook/venv
	rm -rf ./jupyterbook/pdoc_venv
	poetry run isort ./* && poetry run black ./**/*.py

book: ## Create the jupyter book in /jupyterbook/_build
	rm -rf ./jupyterbook/_build
	rm -rf ./jupyterbook/venv
	python -m venv ./jupyterbook/venv
	. ./jupyterbook/venv/bin/activate
	pip install .
	pip install jupyter-book
	jupyter-book build jupyterbook/ --all

    # Copy additional static html files to the jupyter book build directory
	cp ./docs/ai-overview.html ./jupyterbook/_build/html/ai-overview.html
	cp ./docs/preamble-preview.html ./jupyterbook/_build/html/examples/preamble-preview.html
	cp ./docs/googlee3179b02e4a8c48e.html ./jupyterbook/_build/html/googlee3179b02e4a8c48e.html

push_docs: ## Publish the jupyter book to github pages
	poetry run pip install ghp-import
	poetry run ghp-import -n -p -f ./jupyterbook/_build/html

tox: install ## Use tox to run tests against all python versions
	poetry run tox

profile: ## Run a very basic performance profiling script
	poetry run python3 performance/profiler.py

push: ## Push to remote repository using custom SSH key (Usage: make push BRANCH=<branch_name> [KEY=<key_name>])
ifndef BRANCH
	$(error BRANCH is not set. Usage: make push BRANCH=<branch_name> [KEY=<key_name>])
endif
ifndef KEY
	$(eval KEY := id_ed25519_personnal)
endif
	GIT_SSH_COMMAND="ssh -i ~/.ssh/$(KEY)" git push origin $(BRANCH)
