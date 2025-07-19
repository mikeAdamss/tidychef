from datetime import datetime

def main():
    from tidychef import acquire, against, preview
    from tidychef.direction import down, left, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsSelectable

    start_acquire = datetime.now()
    table: XlsSelectable = acquire.xls.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/service-industry.xls",
        tables="TOPSI9",
    )
    end_acquire = datetime.now()


    start_select = datetime.now()
    footer = table.excel_ref("A").re("Average").expand(right).expand(down)

    anchor = (
        table.re(".*ships and boats.*").assert_one().shift(left).label_as("Anchor Cell")
    )
    year = (anchor.shift(left(3)).expand(down).is_not_blank() - footer).label_as("Year")
    quarter = (
        (anchor.shift(left(2)).expand(down).is_not_blank() | year.shift(right)) - footer
    ).label_as("Quarter")
    cdid = table.re(r"^[A-Z]{3}\d$").assert_single_row().label_as("CDID")
    product = (
        anchor.extrude(up)
        .extrude(down)
        .expand(right)
        .is_not_blank()
        .label_as("Product")
    )
    observations = (cdid.waffle(down, quarter) - footer).label_as("Value")
    end_select = datetime.now()

    start_transform = datetime.now()
    tidy_data = TidyData(
        observations,
        Column(product.attach_directly(down)),
        Column(
            year.attach_closest(down),
            apply=lambda x: x[:4],
            validate=against.is_numeric,
        ),
        Column(
            quarter.attach_directly(right),
            apply=lambda x: "All" if x == "" else x,
        ),
        Column(cdid.attach_directly(down)),
    )

    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()

    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)

