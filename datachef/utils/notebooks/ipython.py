from IPython import get_ipython

# basedhttps://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def in_notebook() -> bool: # pragma: no cover
    if not get_ipython():
        return False
    if 'IPKernelApp' not in get_ipython().config:
        return False
    return True