from os import linesep

import pytest

from datachef.models.dsd.components.base import ComponentMatcher, ComponentVariant


def dontcallme(*args, **kwargs):
    """
    If the matcher matches where we don't expect it to, tell us
    about it.
    """
    raise NotImplementedError("Component matcher has unexpectedly succeeded.")


def get_component_variant(component_class: object) -> ComponentVariant:
    return ComponentVariant(
        component_class=component_class,
        arg_types=[int, bool],
        required_kwargs=["foo"],
        optional_kwargs=["bar", "baz"],
        failed_on="Some message about why a component doesn't match this",
    )


@pytest.fixture
def single_component_variant() -> ComponentVariant:
    return get_component_variant(object)


class SomeException(Exception):
    ...


class Matcher(ComponentMatcher):
    inventory = [get_component_variant(dontcallme)]
    contextual_exception = SomeException


def test_component_variant_repr(single_component_variant: ComponentVariant):
    """
    Test that a component variant class can provide a human
    readable representation.
    """

    expected_repr = """<class 'object'>
Requires args by type: [<class 'int'>, <class 'bool'>]
Expected kwargs: ['foo']
Optional kwargs: ['bar', 'baz']
----- unmatched because -----
Some message about why a component doesn't match this
""".strip()

    actual_repr = str(single_component_variant.__repr__()).strip()

    assert actual_repr in expected_repr, (
        f"Expected messge: {linesep}"
        f"{expected_repr}{linesep}"
        f"{linesep}"
        f"Got message : {actual_repr}"
    )


def test_component_matcher_bad_matches():
    """
    Test the expected behaviour when we provide a number of args
    that does not match any known component variant
    """

    # Too many args
    with pytest.raises(SomeException) as err_info:
        Matcher("foo", "bar", "baz")
    assert "Expected 2 args, got 3" in str(err_info.value)

    # Wrong number of keywords
    with pytest.raises(SomeException) as err_info:
        Matcher("foo", "bar")
    assert "Got 0 keyword arguments, but requires at least 1" in str(err_info.value)

    # Args of the wrong type
    with pytest.raises(SomeException) as err_info:
        Matcher("foo", "bar", foo=99)
    assert (
        f"Argument 0 must be of type: <class 'int'>, got foo as <class 'str'>"
        in str(err_info.value)
    )

    # do we have the required kwargs
    with pytest.raises(SomeException) as err_info:
        Matcher(0, True, something_random=99)
    assert f"A keyword argument of foo is required." in str(err_info.value)

    # are there any additional kwargs provided that we're not expecting
    with pytest.raises(SomeException) as err_info:
        Matcher(0, True, foo="yup", something_random=99)
    assert 'Keyword argument "something_random" is neither:' in str(err_info.value)
