def main():
    from tidychef import acquire, filters, preview
    from tidychef.direction import below, down, right
    from tidychef.output import Column, TidyData

    # Load a CSV table from a URL
    table = acquire.csv.http(
        "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/csv/bands-wide.csv"
    )

    # Select numeric observations and label them
    observations = table.filter(filters.is_numeric).label_as("Value")

    # Label headers based on their positions
    bands = table.row("3").is_not_blank().label_as("Band")
    assets = table.row("2").is_not_blank().label_as("Asset")
    names = (
        table.excel_ref("A4")
        .expand(right)
        .expand(down)
        .filter(filters.is_not_numeric)
        .is_not_blank()
        .label_as("Name")
    )
    preview(observations, bands, assets, names)

    # Build tidy data by associating observations with their corresponding headers
    tidy_data = TidyData(
        observations,
        # "Band" labels are closest to the right of each value
        Column(bands.finds_observations_closest(right)),
        # "Assets" labels are directly below each value
        Column(assets.finds_observations_directly(below)),
        # "Names" labels are direcrly to the right of each value
        Column(names.finds_observations_directly(right)),
    )

    # Export the tidy data to CSV
    tidy_data.to_csv("bands_tidy.csv")
