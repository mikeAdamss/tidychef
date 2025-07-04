def main():
    from tidychef import acquire, preview
    from tidychef.direction import up, down, left, right
    from tidychef.output import TidyData, Column
    from tidychef.selection import XlsSelectable

    table: XlsSelectable = acquire.xls.http("https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/monthlygdptablesapril2023.xls", tables="GVA")

    # Sensible starting things
    anchor = table.excel_ref("B7").label_as("Anchor Cell")
    assert anchor.lone_value() == "CDID", "Anchor has moved position"

    cdid = anchor.expand(down).filter(lambda x: x.value == "CDID").fill(right).label_as("CDID")
    identifier = anchor.shift(up(2)).fill(right).label_as("Identifier")
    category = anchor.fill(down).filter(lambda x: x.value != "CDID").label_as("Category")
    time_period = category.shift(left).label_as("Time Period")

    observations = (anchor.shift(right).shift(down).expand(right).expand(down).is_not_blank() - cdid).label_as("Value")

    # Create a bounded preview inline but also write the full preview to path
    preview(anchor, identifier, category, cdid, time_period, observations, bounded="A4:Z16")

    tidy_data = TidyData(
        observations,
        Column(cdid.finds_observations_directly(down)),
        Column(identifier.finds_observations_directly(down)),
        Column(category.finds_observations_directly(right), apply=lambda x: x.split("[")[0].strip()),
        Column(time_period.finds_observations_directly(right), apply=lambda x: x.replace(".0", ""))
    )
    tidy_data.to_csv("data.csv")