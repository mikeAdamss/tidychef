from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import Cell


def test_constant_lookup_engine():
    """
    Test that the constant lookup works
    """

    constant_engine = Constant("Some constant")

    for case in [
        Cell(x="1", y="3", value="foo"),
        Cell(x="2", y="2", value="bar"),
        Cell(x="3", y="3", value="baz"),
    ]:
        assert constant_engine.resolve(case).value == "Some constant"
        assert constant_engine.resolve(case).value == "Some constant"
        assert constant_engine.resolve(case).value == "Some constant"
