from datetime import datetime

def main():
    from tidychef import acquire, preview
    from tidychef.direction import down, right
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsxSelectable

    start_acquire = datetime.now()
    table: XlsxSelectable = acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xlsx/ons-oic.xlsx",
        tables="Table 1a",
    )
    end_acquire = datetime.now()

    start_select = datetime.now()
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
    end_select = datetime.now()

    start_transform = datetime.now()
    tidy_data = TidyData(
        observations,
        Column(identifier.attach_directly(down)),
        Column(housing.attach_directly(down)),
        Column(time_period.attach_directly(right)),
    )

    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()


    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)

