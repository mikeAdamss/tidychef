def main():
    from datetime import datetime

    from tidychef import acquire, filters, preview
    from tidychef.direction import down, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsSelectable

    table: XlsSelectable = acquire.xls.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/house-prices.xls",
        tables="Table 11",
    )

    housing = (
        table.re("New dwellings")
        .assert_one()
        .expand(right)
        .is_not_blank()
        .label_as("Housing")
    )

    area_code = (
        table.excel_ref("A").is_not_blank().re("[A-Z][0-9].*").label_as("Area Code")
    )

    area = area_code.shift(up).label_as("Area")

    year = area.shift(right).expand(down).is_not_blank().label_as("Year")

    quarter = year.shift(right).expand(down).is_not_blank().label_as("Quarter")

    observations = (
        quarter.fill(right)
        .is_not_blank()
        .filter(filters.is_not_numeric)
        .label_as("Value")
    )

    # Create a bounded preview inline but also write the full preview to path
    preview(observations, housing, area_code, area, year, quarter, bounded="A1:M20")

    tidy_data = TidyData(
        observations,
        Column(
            housing.finds_observations_directly(down), apply=lambda x: x.rstrip("4")
        ),
        Column(area.finds_observations_closest(down)),
        Column(area_code.finds_observations_closest(down)),
        Column(
            year.finds_observations_closest(down), apply=lambda x: x.replace(".0", "")
        ),
        Column(quarter.finds_observations_directly(right)),
        obs_apply=lambda x: x.replace(".0", ""),
    )

    tidy_data.to_csv("data.csv")
