import pytest

from datachef import acquire
from datachef import datafuncs as dfc
from datachef.direction.directions import down, left, right, up
from datachef.lookup.engines.within import Within
from datachef.selection.selectable import Selectable

# Note:
# The logic of reversing the directionality of a within lookup
# (which contains three directions) can be a little gnarly to
# comprehend.
# So while these tests are not required for coverage, they are
# nevertheless a sensible thing to maintain


def test_within_from_selection():
    """ """

    # Case 1
    # ------

    selection: Selectable = acquire.python.pipe_table(
        """
                |         | Male    |         |         | Female    |           |     
        male_ob | male_ob | male_ob | male_ob | male_ob | female_ob | female_ob | female_ob  
        male_ob | male_ob | male_ob | male_ob | male_ob | female_ob | female_ob | female_ob                                              
        """
    )

    sex = selection.excel_ref("1").is_not_blank().label_as("Sex")
    within_lookup: Within = sex.finds_observations_within(
        down, start=right(2), end=left(2)
    )

    male_obs = selection.re("male_ob")
    m_count = 0
    for male_ob in male_obs:
        assert within_lookup.resolve(male_ob).value == "Male"
        m_count += 1
    assert m_count == 10

    female_obs = selection.re("female_ob")
    f_count = 0
    for female_ob in female_obs:
        assert within_lookup.resolve(female_ob).value == "Female"
        f_count += 1
    assert f_count == 6

    # # Case 2
    # # ------

    selection: Selectable = acquire.python.pipe_table(
        """
        female_ob | female_ob | female_ob | female_ob | female_ob | male_ob | male_ob | male_ob | male_ob
        female_ob | female_ob | female_ob | female_ob | female_ob | male_ob | male_ob | male_ob | male_ob
                  | Female    |           |           |           |        |          | Male    |                                           
        """
    )

    sex = selection.excel_ref("3").is_not_blank().label_as("Sex")
    within_lookup: Within = sex.finds_observations_within(
        up, start=left(2), end=right(3)
    )

    male_obs = selection.re("male_ob")
    m_count = 0
    for male_ob in male_obs:
        assert within_lookup.resolve(male_ob).value == "Male", f"Cell was {male_ob}"
        m_count += 1
    assert m_count == 8

    female_obs = selection.re("female_ob")
    f_count = 0
    for female_ob in female_obs:
        assert (
            within_lookup.resolve(female_ob).value == "Female"
        ), f"Cell was {female_ob}"
        f_count += 1
    assert f_count == 10

    # # Case 3
    # # ------

    selection: Selectable = acquire.python.pipe_table(
        """
                | male_ob   | male_ob   |
        Male    | male_ob   | male_ob   |
                | male_ob   | male_ob   |
                | male_ob   |           |
        Female  |           | female_ob |
                | female_ob | female_ob |                                          
        """
    )

    sex = selection.excel_ref("A").is_not_blank().label_as("Sex")
    within_lookup: Within = sex.finds_observations_within(
        right, start=down(2), end=up(1)
    )

    male_obs = selection.re("male_ob")
    m_count = 0
    for male_ob in male_obs:
        assert within_lookup.resolve(male_ob).value == "Male", f"Cell was {male_ob}"
        m_count += 1
    assert m_count == 7

    female_obs = selection.re("female_ob")
    f_count = 0
    for female_ob in female_obs:
        assert (
            within_lookup.resolve(female_ob).value == "Female"
        ), f"Cell was {female_ob}"
        f_count += 1
    assert f_count == 3

    # Case 4
    # ------

    selection: Selectable = acquire.python.pipe_table(
        """
                | 1   | 1   |       |   |   |   |   
        One     | 1   | 1   |       | 3 | 3 |   | 3 
                | 1   | 1   |       | 3 |   |   |
                | 1   |     | Three |   | 3 |   | 
        Two     |     | 2   |       | 3 | 3 |   | 3
                | 2   | 2   |       | 3 |   |   | 3                    
        """
    )

    sex = (
        (selection.excel_ref("A") | selection.excel_ref("D"))
        .is_not_blank()
        .label_as("Sex")
    )
    within_lookup: Within = sex.finds_observations_within(
        right, start=down(2), end=up(2)
    )

    one_obs = selection.re("1")
    one_count = 0
    for one_ob in one_obs:
        assert within_lookup.resolve(one_ob).value == "One", f"Cell was {one_ob}"
        one_count += 1
    assert one_count == 7

    two_obs = selection.re("2")
    two_count = 0
    for two_ob in two_obs:
        assert within_lookup.resolve(two_ob).value == "Two", f"Cell was {two_ob}"
        two_count += 1
    assert two_count == 3

    three_obs = selection.re("3")
    three_count = 0
    for three_ob in three_obs:
        assert within_lookup.resolve(three_ob).value == "Three", f"Cell was {three_ob}"
        three_count += 1
    assert three_count == 10

    # Case 5
    # ------

    selection: Selectable = acquire.python.pipe_table(
        """
                | 1   | 1   | One   |   |   |   |    |       | 4 |   | Four
             1  | 1   | 1   |       | 3 | 3 |   | 3  |       | 4 |   |
                | 1   | 1   |       | 3 |   | 3 |    |       |   | 4 |
                | 1   |     |       | 3 |   |   | 3  | Three | 4 | 4 |
                |     | 2   | Two   | 3 | 3 | 3 | 3  |       |   |   |
                | 2   | 2   |       | 3 |   |   | 3  |       |   |   |  
        """
    )

    sex = (
        (selection.excel_ref("D") | selection.excel_ref("I") | selection.excel_ref("L"))
        .is_not_blank()
        .label_as("Sex")
    )

    within_lookup: Within = sex.finds_observations_within(
        left, start=down(3), end=up(2)
    )

    one_obs = selection.re("1")
    one_count = 0
    for one_ob in one_obs:
        assert within_lookup.resolve(one_ob).value == "One", f"Cell was {one_ob}"
        one_count += 1
    assert one_count == 8

    two_obs = selection.re("2")
    two_count = 0
    for two_ob in two_obs:
        assert within_lookup.resolve(two_ob).value == "Two", f"Cell was {two_ob}"
        two_count += 1
    assert two_count == 3

    three_obs = selection.re("3")
    three_count = 0
    for three_ob in three_obs:
        assert within_lookup.resolve(three_ob).value == "Three", f"Cell was {three_ob}"
        three_count += 1
    assert three_count == 13

    four_obs = selection.re("4")
    four_count = 0
    for four_ob in four_obs:
        assert within_lookup.resolve(four_ob).value == "Four", f"Cell was {four_ob}"
        four_count += 1
    assert four_count == 5
