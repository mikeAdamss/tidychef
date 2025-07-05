def main():
    from tidychef import acquire, preview
    from tidychef.direction import down, right
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsxSelectable

    table: XlsxSelectable = acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xlsx/ons-oic.xlsx",
        tables="Table 1a",
    )
    anchor = table.excel_ref("A").re("Time period").assert_one().label_as("Anchor Cell")

    observations = (
        anchor.shift(right)
        .shift(down(2))
        .expand(right)
        .expand(down)
        .is_not_blank()
        .label_as("Value")
    )
    identifier = anchor.shift(down).fill(right).label_as("Identifier")
    housing = anchor.fill(right).label_as("Housing")
    time_period = anchor.shift(down).fill(down).label_as("Time Period")

    # Create a bounded preview inline but also write the full preview to path
    preview(anchor, observations, identifier, housing, time_period, bounded="A3:O13")

    tidy_data = TidyData(
        observations,
        Column(identifier.finds_observations_directly(down)),
        Column(housing.finds_observations_directly(down)),
        Column(time_period.finds_observations_directly(right)),
    )

    tidy_data.to_csv("data.csv")
