from datetime import datetime


def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import below, down, right
    from tidychef.output import Column, TidyData

    start_acquire = datetime.now()
    # Load a CSV table from a URL
    table = acquire.csv.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/csv/bands-wide.csv"
    )
    end_acquire = datetime.now()

    start_select = datetime.now()
    # Select numeric observations and label them
    observations = table.is_numeric().label_as("Value")

    # Select headers and label them
    bands = table.row_containing_strings(["Beatles"]).is_not_blank().label_as("Band")
    assets = table.row_containing_strings(["Cars"]).is_not_blank().label_as("Asset")
    names = table.cell_containing_string("Beatles").shift(down).expand_to_box().is_not_numeric().label_as("Name")
    end_select = datetime.now()


    start_transform = datetime.now()
    # Build tidy data by attaching observations and headers
    tidy_data = TidyData(
        observations,
        Column(bands.attach_closest(right)),
        Column(assets.attach_directly(below)),
        Column(names.attach_directly(right)),
    )
    # Force the transform
    tidy_data.to_csv("data.csv")
    end_transform = datetime.now()


    acquire_duration = end_acquire - start_acquire
    selection_duration = end_select - start_select
    transform_duration = end_transform - start_transform

    return acquire_duration, selection_duration, transform_duration, len(tidy_data)
