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
        optional_kwargs=["bar", "baz"],
        failed_on="Some message about why a component doesn't match this",
    )


@pytest.fixture
def single_component_variant() -> ComponentVariant:
    return get_component_variant(object)


class SomeException(Exception):
    ...


class MyConstructor(ComponentConstructor):
    inventory = [get_component_variant(dontcallme)]
    contextual_exception = SomeException


def test_component_variant_repr(single_component_variant: ComponentVariant):
    """
    Test that a component variant class can provide a human
    readable representation.
    """

    expected_repr = """<class 'object'>
Requires args by type: [<class 'int'>, <class 'bool'>, <class 'Exception'>]
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
        MyConstructor("foo", "bar", "baz", "eps")
    assert "Expected 3 args, got 4" in str(err_info.value)

    # Wrong number of keywords
    with pytest.raises(SomeException) as err_info:
        MyConstructor("foo", "bar", "baz")
    msg_fragment = "Got 0 keyword arguments, but requires at least 1"
    assert msg_fragment in str(err_info.value), (
        f'Could not find message: {msg_fragment} in:{linesep*2}'
        f'{err_info.value}{linesep}'
    )

    # Args of the wrong type
    with pytest.raises(SomeException) as err_info:
        MyConstructor("foo", "bar", "eps", foo=99)
    msg_fragment = 'Argument 1 of 3 must be of type: <class \'int\'>, "foo" has type: <class \'str\'>'
    assert msg_fragment in str(err_info.value), (
        f'Could not find message: {msg_fragment} in:{linesep*2}'
        f'{str(err_info.value).split(linesep)}{linesep}'
    )

    # Args of the wrong type that are classes
    with pytest.raises(SomeException) as err_info:
        MyConstructor(0, True, NotImplementedError, foo=99)
    msg_fragment = "Argument 3 of 3 must be of type: <class 'Exception'>, has type: <class 'NotImplementedError'>."
    assert msg_fragment in str(err_info.value), (
        f'Could not find message: {msg_fragment} in:{linesep*2}'
        f'{str(err_info.value).split(linesep)}{linesep}'
    )

    # do we have the required kwargs
    with pytest.raises(SomeException) as err_info:
        MyConstructor(0, True, Exception, something_random=99)
    assert f"A keyword argument of foo is required." in str(err_info.value)

    # are there any additional kwargs provided that we're not expecting
    with pytest.raises(SomeException) as err_info:
        MyConstructor(0, True, Exception, foo="yup", something_random=99)
    assert 'Keyword argument "something_random" is neither:' in str(err_info.value)
