# Contributing to tidychef

Thank you for your interest in contributing to tidychef. Contributions from the community are very welcome. The following guidance is intended to make the process as smooth as possible.

## Getting Started

1. **Fork** the tidychef repository and clone your fork locally.  
2. Create a new branch for your work:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. Set up your development environment:

    ```bash
    pip install poetry
    cd tidychef
    poetry install
    ```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.  
- Use [isort](https://pycqa.github.io/isort/) and [Black](https://black.readthedocs.io/en/stable/) for automatic formatting.  
- Write clear, concise, and descriptive commit messages.

## Testing

- Add tests for any new code you introduce, using [pytest](https://docs.pytest.org/en/stable/).  
- The CI requires 100% test coverage; tests are mandatory.

### Running Tests Locally

If you have `make` (Linux/macOS):

    ```bash
    make test
    ```

Otherwise:

    ```bash
    poetry run pytest
    ```

## Formatting Your Code

If you have `make` (Linux/macOS):

    ```bash
    make fmt
    ```

Otherwise:

    ```bash
    poetry run isort . && poetry run black .
    ```

> **Note:** When running the latter, if you have worked on documentation, consider deleting `./jupyterbook/venv` and `./jupyterbook/pdoc_venv` directories if they exist, to avoid formatting third-party library code unintentionally.

## Documentation

If your pull request adds or changes any user-facing functionality, update the documentation accordingly.

> *Note:* It’s fine to wait until we finalize the change before updating the docs, but the PR will not be merged without it.

Our documentation is built using [Jupyter Book](https://jupyterbook.org/en/stable/intro.html).  
To explore it locally:

    ```bash
    poetry run jupyter notebook
    ```

Then open the `jupyterbook` folder in the notebook interface to view the structured documentation notebooks.

## Reporting Issues

Use GitHub Issues to report bugs or suggest improvements.

When reporting bugs, please provide clear, reproducible steps along with relevant context or screenshots.

For usability feedback (e.g., "X scenario is too hard, please improve"), please include multiple screenshots and, if possible, links to source files for shared understanding.

## Pull Requests

- Submit pull requests against the `main` branch.  
- Clearly describe the purpose and scope of your changes.  
- Reference related issues using `#issue-number`.  
- Feedback is given constructively; PRs will only be merged once ready and meeting quality standards.  
- For major or potentially contentious changes, please open an issue first to discuss.

## Development Practices

While workflows vary, here is a recommended approach to get started:

- Open the `./tidychef` code in a development IDE (e.g., VS Code) from the repo root (`code .`).  
- Run a Jupyter notebook server from the repo root:

    ```bash
    poetry run jupyter notebook
    ```

This allows you to develop code in the IDE and simultaneously test or demo functionality interactively in notebooks. Restart the notebook kernel to load code changes. Since the notebook is opened in the repo root, you can freely import your local tidychef modules.
