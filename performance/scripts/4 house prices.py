def main():
    from tidychef import acquire, preview, filters
    from tidychef.direction import up, down, right
    from tidychef.output import TidyData, Column
    from tidychef.selection import XlsSelectable
    from datetime import datetime

    print(f"starting house prices example: {datetime.now().isoformat()}")

    table: XlsSelectable = acquire.xls.http("https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/xls/house-prices.xls", tables="Table 11")

    print(f"finished acquiring data: {datetime.now().isoformat()}")

    housing = table.re('New dwellings').assert_one().expand(right).is_not_blank().label_as("Housing")
    print(f"finished selecting housing: {datetime.now().isoformat()}")

    area_code = table.excel_ref("A").is_not_blank().re("[A-Z][0-9].*").label_as("Area Code")
    print(f"finished selecting area code: {datetime.now().isoformat()}")

    area = area_code.shift(up).label_as("Area")
    print(f"finished selecting area: {datetime.now().isoformat()}")

    year = area.shift(right).expand(down).is_not_blank().label_as("Year")
    print(f"finished selecting year: {datetime.now().isoformat()}")
    
    quarter = year.shift(right).expand(down).is_not_blank().label_as("Quarter")
    print(f"finished selecting quarter: {datetime.now().isoformat()}")

    observations = quarter.fill(right).is_not_blank().filter(filters.is_not_numeric).label_as("Value")
    print(f"finished selecting observations: {datetime.now().isoformat()}")
    
    print(f"finished selecting data: {datetime.now().isoformat()}")

    # Create a bounded preview inline but also write the full preview to path
    preview(observations, housing, area_code, area, year, quarter, bounded="A1:M20")

    print(f"finished previewing data: {datetime.now().isoformat()}")

    tidy_data = TidyData(
        observations,
        Column(housing.finds_observations_directly(down), apply=lambda x: x.rstrip("4")),
        Column(area.finds_observations_closest(down)),
        Column(area_code.finds_observations_closest(down)),
        Column(year.finds_observations_closest(down), apply=lambda x: x.replace(".0", "")),
        Column(quarter.finds_observations_directly(right)),
        obs_apply = lambda x: x.replace(".0", "")
    )

    print(f"finished specifying tidying data: {datetime.now().isoformat()}")

    tidy_data.to_csv("data.csv")

    print(f"finished writing data to csv: {datetime.now().isoformat()}")

