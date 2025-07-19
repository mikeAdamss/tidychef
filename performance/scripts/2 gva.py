from datetime import datetime


def main():
    from tidychef import acquire, preview
    from tidychef.direction import down, left, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsSelectable

    start_acquire = datetime.now()
    table: XlsSelectable = acquire.xls.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/monthlygdptablesapril2023.xls",
        tables="GVA",
    )
    end_acquire = datetime.now()


    start_select = datetime.now()
    # Sensible starting things
    anchor = table.excel_ref("B7").label_as("Anchor Cell")
    assert anchor.lone_value() == "CDID", "Anchor has moved position"

    cdid = (
        anchor.expand(down)
        .filter(lambda x: x.value == "CDID")
        .fill(right)
        .label_as("CDID")
    )
    identifier = anchor.shift(up(2)).fill(right).label_as("Identifier")
    category = (
        anchor.fill(down).filter(lambda x: x.value != "CDID").label_as("Category")
    )
    time_period = category.shift(left).label_as("Time Period")

    observations = (
        anchor.shift(right).shift(down).expand(right).expand(down).is_not_blank() - cdid
    ).label_as("Value")
    end_select = datetime.now()

    start_transform = datetime.now()
    tidy_data = TidyData(
        observations,
        Column(cdid.attach_directly(down)),
        Column(identifier.attach_directly(down)),
        Column(
            category.attach_directly(right),
            apply=lambda x: x.split("[")[0].strip(),
        ),
        Column(
            time_period.attach_directly(right),
            apply=lambda x: x.replace(".0", ""),
        ),
    )
    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()

    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)
