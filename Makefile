.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run all unit tests and create new coverage report
	poetry run coverage run -m pytest

report: ## View the latest report of test coverage
	poetry run coverage report -m

format: ## Format the codebase with isort and black
	poetry run isort ./* && poetry run black ./*

docs: ## Combines auto API docs and contents of _docs and serves it locally for preview.
	poetry run pdoc -html ./datachef --output-dir ./docs
	cp -a ./_docs/* ./docs/
	cd docs && python3 -m http.server

pyrightbuild: ## Build docker image
	docker build -t pyrightimage ./images

pyright: ## Run pyright through docker
	docker run -v $(PWD):/workspace -w /workspace -it pyrightimage /bin/bash -c "poetry run pyright ./datachef --lib"