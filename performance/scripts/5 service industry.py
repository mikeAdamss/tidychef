def main():
    from tidychef import acquire, against, preview
    from tidychef.direction import down, left, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsSelectable

    table: XlsSelectable = acquire.xls.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/service-industry.xls",
        tables="TOPSI9",
    )
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

    preview(anchor, observations, product, year, quarter, cdid)

    tidy_data = TidyData(
        observations,
        Column(product.finds_observations_directly(down)),
        Column(
            year.finds_observations_closest(down),
            apply=lambda x: x[:4],
            validate=against.is_numeric,
        ),
        Column(
            quarter.finds_observations_directly(right),
            apply=lambda x: "All" if x == "" else x,
        ),
        Column(cdid.finds_observations_directly(down)),
    )

    tidy_data.to_csv("data.csv")
