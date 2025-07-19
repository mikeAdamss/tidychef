from datetime import datetime

def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import down, left, right, up
    from tidychef.output import Column, TidyData
    from tidychef.selection import XlsxSelectable

    start_acquire = datetime.now()
    table: XlsxSelectable = acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xlsx/coronavirusandlonelinessreferencetable.xlsx",
        tables="1.4 Loneliness by sex",
    )
    end_acquire = datetime.now()

    start_select = datetime.now()
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
    end_select = datetime.now()

    start_transform = datetime.now()
    tidy_data = TidyData(
        observations,
        Column(sex.attach_directly(down)),
        Column(sample_size.attach_directly(up)),
        Column(loneliness.attach_directly(right)),
    )

    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()


    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)
