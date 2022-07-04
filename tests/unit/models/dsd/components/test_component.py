import pytest
from os import linesep

from datachef.models.dsd.components.base import ComponentVariant


def test_component_variant_repr():
    """
    Test that a component variant class can provide a human
    readable representation.
    """

    cv = ComponentVariant(
        component_class=object,
        arg_types = [int, bool],
        required_kwargs = ["foo"],
        optional_kwargs = ["bar", "baz"],
        failed_on = "Some message about why a component doesn't match this"
    )

    expected_repr = """<class 'object'>
Requires args by type: [<class 'int'>, <class 'bool'>]
Expected kwargs: ['foo']
Optional kwargs: ['bar', 'baz']
----- unmatched because -----
Some message about why a component doesn't match this
""".strip()

    actual_repr = str(cv.__repr__()).strip()

    assert actual_repr in expected_repr, (
        f'Expected messge: {linesep}'
        f'{expected_repr}{linesep}'
        f'{linesep}'
        f'Got message : {actual_repr}' 
    )