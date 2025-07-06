def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import down, right, below
    from tidychef.output import Column, TidyData

    # Load a CSV table from a URL
    table = acquire.csv.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/csv/bands-wide.csv"
    )

    # Select numeric observations and label them
    observations = table.is_numeric().label_as("Value")

    # Select headers and label them
    bands = table.row_containing_strings(["Beatles"]).is_not_blank().label_as("Band")
    assets = table.row_containing_strings(["Cars"]).is_not_blank().label_as("Asset")
    names = table.cell_containing_string("Beatles").shift(down).expand_to_box().is_not_numeric().label_as("Name")

    # Build tidy data by attaching observations and headers
    tidy_data = TidyData(
        observations,
        Column(bands.attach_closest(right)),
        Column(assets.attach_directly(below)),
        Column(names.attach_directly(right)),
    )

    # Force the transform
    tidy_data.to_dict()
