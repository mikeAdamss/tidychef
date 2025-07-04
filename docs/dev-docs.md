# Development Docs

This needs expanding but for now its some simple reminders to self.

## Updating documentation

The jupyter book is not (yet) generated dynamically, you need to:

- make your changes as needed in `./jupyterbooks`
- `make book` to create the html in `./jupyterbooks/_build/html` (drag the index into a browser locally to preview)
- QA what's just been changed. **Do it careful**, things can easily slip through with all those notebooks applying their snippets to generate the examples.
- Merge into base branch.
- Then (from local - with `make book` having been ran) do `make push_docs`, this will push the jupyterbook to github pages for public consumption.