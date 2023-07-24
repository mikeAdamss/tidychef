from IPython import get_ipython


# based on
# https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def in_notebook() -> bool:  # pragma: no cover
    """
    Checks whether the python interpreter calling
    this code is doing so via an IPython or Jupyter
    notebook.
    """
    if not get_ipython():
        return False
    if "IPKernelApp" not in get_ipython().config:
        return False
    return True
