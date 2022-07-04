"""
Base classes for all DSD components
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from os import linesep
from typing import Any, List, Optional

from datachef.constants.urls import CONSTRUCTING_DIMENSIONS

class BaseComponent(metaclass=ABCMeta):
    """
    The shared basic definition of a component
    """

    def __init__(self, *args, **kwargs):
        self._post_init(*args, **kwargs) # pragma: no cover

    @abstractmethod
    def _post_init(self, *args, **kwargs):
        """
        Instantiation behaviour specific to
        the given subclass of BaseComponent
        """


@dataclass
class ComponentVariant:
    """
    Helper to hold simple patterns of arg types and
    kwargs for identifying a required component.
    """

    component_class: BaseComponent
    arg_types: List[Any]
    required_kwargs: List[str]
    failed_on: Optional[str] = None
    optional_kwargs: Optional[List[str]] = None

    def __repr__(self):
        """
        A string representation of this style of component
        """
        return (
            f"{linesep}{self.component_class}{linesep}"
            f"Requires args by type: {self.arg_types}{linesep}"
            f"Expected kwargs: {self.required_kwargs}{linesep}"
            f"Optional kwargs: {self.optional_kwargs}{linesep}"
            f"----- unmatched because -----{linesep}"
            f"{self.failed_on}{linesep}"
        )


@dataclass
class ComponentFactory(metaclass=ABCMeta):
    """
    A base factory class, set_component will
    select the appropriate child component
    based on the combination, number, pattern
    and type of the args and kwargs provided.

    The purpose of this abstraction is that some
    components will only be valid in combination
    (or invalid in lack of combination) with other
    components.

    Example: a DSD cannot have a MeasureType component
    and a Measure component in combination, though
    both are valid components in isolation.

    The factory pattern helps us defer that cross
    component validation until all components have
    been successfully instantiated and validated.
    """

    inventory: List[ComponentVariant]
    contextual_exception: Exception

    def __init__(self, *args, **kwargs):
        self._component = self.set_component(*args, **kwargs)

    @property
    def component(self) -> BaseComponent:
        return self._component

    def set_component(self, *args, **kwargs) -> BaseComponent: 

        for potential_match in self.inventory:

            # do we have the expected number of arguments
            largs = len(args)
            lpargs = len(potential_match.arg_types)
            if largs != lpargs:
                potential_match.failed_on = f'Expected {largs} args, got {lpargs}'
                continue

            # do we have the minimum number of keyword arguments
            lkwargs = len(kwargs)
            lpkwargs = len(potential_match.required_kwargs)
            if lkwargs < lpkwargs:
                potential_match.failed_on = f'Got {lkwargs} keyword arguments, but requires at least {lpkwargs}'
                continue

            # do the arg types match that which we are expecting
            for i, arg in enumerate(args):
                arg_type = potential_match.arg_types[i]
                if not isinstance(arg, arg_type):
                    potential_match.failed_on = f'Argument {i} must be of type: {arg_type}.'
                    continue

            # do the required kwargs match that which we are expecting
            for kwarg in potential_match.required_kwargs:
                if kwarg not in kwargs:
                    potential_match.failed_on = f'A keyword argument of {kwarg} is required.'
                    continue

            # are there any optional kwargs provided that we're not expecting
            if potential_match.optional_kwargs:
                for extra_kwarg in [k for k in kwargs if k not in potential_match.required_kwargs]:
                    if extra_kwarg not in potential_match.optional_kwargs:
                        potential_match.failed_on = (
                            f'Keyword argument {extra_kwarg} is neither:'
                            f'a required kwarg from: {potential_match.required_kwargs}'
                            f'an optional kwarg from: {potential_match.optional_kwargs}'
                        )
                        continue 

            component_variant_matched: ComponentVariant = potential_match
            break

        else:
            raise self.contextual_exception(
                f"Unable to identify required dimension type from provided parameters, must be on of: {linesep}"
                f"{self.inventory}{linesep}"
                f"for more detailed help please see: {CONSTRUCTING_DIMENSIONS}"
            )

        return component_variant_matched.component_class(*args, **kwargs)
