from datetime import datetime


def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import down, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsSelectable

    start_acquire = datetime.now()
    table: XlsSelectable = acquire.xls.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/house-prices.xls",
        tables="Table 11",
    )
    end_acquire = datetime.now()
    
    start_select = datetime.now()

    housing = (
        table.row_containing_strings(["New dwellings"])
        .expand(right)
        .is_not_blank()
        .label_as("Housing")
    )

    area_code = table.excel_ref('A').is_not_blank().re("[A-Z][0-9].*").label_as("Area Code")

    area = area_code.shift(up).label_as("Area")

    year = area.shift(right).expand(down).is_not_blank().label_as("Year")

    quarter = year.shift(right).expand(down).is_not_blank().label_as("Quarter")

    observations = (
        quarter.fill(right)
        .is_not_blank()
        .is_numeric()
        .label_as("Value")
    )
    end_select = datetime.now()

    start_transform = datetime.now()

    tidy_data = TidyData(
        observations,
        Column(
            housing.attach_directly(down), apply=lambda x: x.rstrip("4")
        ),
        Column(area.attach_closest(down)),
        Column(area_code.attach_closest(down)),
        Column(
            year.attach_closest(down), apply=lambda x: x.replace(".0", "")
        ),
        Column(quarter.attach_directly(right)),
        obs_apply=lambda x: x.replace(".0", ""),
    )

    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()
    
    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)