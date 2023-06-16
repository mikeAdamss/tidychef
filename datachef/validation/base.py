from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class BaseValidation(metaclass=ABCMeta):
    print_not_raise_exception: bool = False
