"""
Module used for acquiring source data from xlsx files
"""
from .http_implemented import http
from .local_implemented import local

__all__ = ["http", "local"]
