"""
Module used for acquiring source data
"""
from . import csv, ods, python, xls, xlsx
from .main import acquirer

__all__ = [
    "acquirer",
    "csv",
    "ods",
    "python",
    "xls",
    "xlsx",
]
