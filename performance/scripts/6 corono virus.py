def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import down, left, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsxSelectable

    table: XlsxSelectable = acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xlsx/coronavirusandlonelinessreferencetable.xlsx",
        tables="1.4 Loneliness by sex",
    )

    # We'll select the source entry at the end just so we can remove it from selections
    unwanted_footer = table.filter(filters.contains_string("Source: ")).assert_one()

    sex = table.re("Male").expand(right).is_not_blank().label_as("Sex")
    sample_size = (
        table.filter(filters.contains_string("Sample size"))
        .fill(right)
        .is_not_blank()
        .label_as("Sample Size")
    )
    loneliness = (
        (table.excel_ref("A4").expand(down) - sample_size.shift(left) - unwanted_footer)
        .is_not_blank()
        .label_as("Loneliness")
    )
    observations = loneliness.fill(right).is_not_blank().label_as("Observations")

    # Create a bounded preview inline but also write the full preview to path
    preview(observations, sex, sample_size, loneliness, bounded="A1:F20")

    tidy_data = TidyData(
        observations,
        Column(sex.finds_observations_directly(down)),
        Column(sample_size.finds_observations_directly(up)),
        Column(loneliness.finds_observations_directly(right)),
    )

    tidy_data.to_csv("data.csv")
