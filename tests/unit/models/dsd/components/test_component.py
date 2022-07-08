from os import linesep

import pytest

from datachef.models.dsd.components.base import ComponentConstructor, ComponentVariant


def dontcallme(*args, **kwargs):
    """
    If the matcher matches where we don't expect it to, tell us
    about it.
    """
    raise NotImplementedError("Component matcher has unexpectedly succeeded.")


def get_component_variant(component_class: object) -> ComponentVariant:
    return ComponentVariant(
        component_class=component_class,
        arg_types=[int, bool, Exception],
        required_kwargs=["foo"],
        optional_kwargs=["bar", "baz"]
    )


@pytest.fixture
def single_component_variant() -> ComponentVariant:
    return get_component_variant(object)


class SomeException(Exception):
    ...


class MyConstructor(ComponentConstructor):
    name = "Test Constructor"
    inventory = [get_component_variant(dontcallme)]
    contextual_exception = SomeException
    help_url = "fake-help.com"


def test_component_matcher_bad_matches():
    """
    Test the expected behaviour when we provide a number of args
    that does not match any known component variant
    """

    # Too many args
    with pytest.raises(SomeException):
        MyConstructor("foo", "bar", "baz", "eps")

    # Wrong number of keywords
    with pytest.raises(SomeException):
        MyConstructor("foo", "bar", "baz")

    # Args of the wrong type
    with pytest.raises(SomeException):
        MyConstructor("foo", "bar", "eps", foo=99)

    # Args of the wrong type that are classes
    with pytest.raises(SomeException):
        MyConstructor(0, True, NotImplementedError, foo=99)

    # do we have the required kwargs
    with pytest.raises(SomeException):
        MyConstructor(0, True, Exception, something_random=99)

    # are there any additional kwargs provided that we're not expecting
    with pytest.raises(SomeException):
        MyConstructor(0, True, Exception, foo="yup", something_random=99)
