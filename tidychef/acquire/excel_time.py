# Dev notes:
# ----------
# Excel has some opinions on time and so handles cells
# of type time as follows:
# - cells are stored as the equivalent of python datetime objects
# - excel also stores a formatting pattern so these time cells can
#   be presented to the user in the way they expect/want.
#
# The below table maps these "excel time formats" to pythons
# stftime() patterns so we can present the cell contents exactly
# as they would appear should the source file be opened via excel.
#
# Please note: this only applies where an excel source is being
# used where the cells have been specifically formatted as type time.

EXCEL_TIME_FORMATS = {
    # Day without leading zero (e.g., 1)
    "D": "%-d",
    # Day of year without leading zero (e.g., 32)
    "DDD": "%j",
    # Month without leading zero (e.g., 1)
    "M": "%-m",
    # Year without century (e.g., 21)
    "YY": "%y",
    # Day-Month-Year with 2-digit year (e.g., 01-05-23)
    "DD-MM-YY": "%d-%m-%y",
    # Day/Month/Year with 2-digit year (e.g., 01/05/23)
    "DD/MM/YY": "%d/%m/%y",
    # Day.Month.Year with 2-digit year (e.g., 01.05.23)
    "DD.MM.YY": "%d.%m.%y",
    # Month-Day-Year with 2-digit year (e.g., 5-1-21)
    "MM-DD-YY": "%m-%d-%y",
    # Month/Day/Year with 2-digit year (e.g., 5/1/21)
    "M/D/YY": "%m/%d/%y",
    # Month/Year with 4-digit year (e.g., 5/2023)
    "m/yyyy": "%-m/%Y",
    # Year/Month with 4-digit year (e.g., 2023/5)
    "yyyy/m": "%Y/%-m",
    # Day/Month/Year with 2-digit year (e.g., 1/5/23)
    "d/m/yy": "%-d/%-m/%y",
    # Day/Month/Year with 4-digit year (e.g., 1/5/2023)
    "d/m/yyyy": "%-d/%-m/%Y",
    # Month/Day/Year with 2-digit year (e.g., 5/1/23)
    "m/d/yy": "%-m/%-d/%y",
    # Month/Day/Year with 4-digit year (e.g., 5/1/2023)
    "m/d/yyyy": "%-m/%-d/%Y",
    # Day/Month with 2-digit year (e.g., 1/5/23)
    "d/m": "%-d/%-m",
    # Month/Day with 2-digit year (e.g., 5/1/23)
    "m/d": "%-m/%-d",
    # Day/Month/Year with 4-digit year (e.g., 01/05/2023)
    "DD/MM/YYYY": "%d/%m/%Y",
    # Day.Month.Year with 4-digit year (e.g., 01.05.2023)
    "DD.MM.YYYY": "%d.%m.%Y",
    # Month-Day-Year with 4-digit year (e.g., 05-01-2023)
    "MM-DD-YYYY": "%m-%d-%Y",
    # Month/Day/Year with 4-digit year (e.g., 05/01/2023)
    "M/D/YYYY": "%m/%d/%Y",
    # Month abbreviation (e.g., Jan)
    "MMM": "%b",
    # Month full name (e.g., January)
    "MMMM": "%B",
    # Year with century (e.g., 2023)
    "YYYY": "%Y",
    # Day-Month-Year with 2-digit year (e.g., 01-May-21)
    "DD-MMM-YY": "%d-%b-%y",
    # Day-Month-Year with 4-digit year (e.g., 01-May-2023)
    "DD-MMM-YYYY": "%d-%b-%Y",
    # Day/Month/Year with 2-digit year (e.g., 01/May/21)
    "DD/MMM/YY": "%d/%b/%y",
    # Day/Month/Year with 4-digit year (e.g., 01/May/2023)
    "DD/MMM/YYYY": "%d/%b/%Y",
    # Year-Month-Day (e.g., 2023-05-01)
    "YYYY-MM-DD": "%Y-%m-%d",
    # Hour in 24-hour format without leading zero (e.g., 3)
    "H": "%-H",
    # Hour in 24-hour format with leading zero (e.g., 03)
    "HH": "%H",
    # Hour in 12-hour format without leading zero (e.g., 3)
    "h": "%-I",
    # Hour in 12-hour format with leading zero (e.g., 03)
    "hh": "%I",
    # Minutes without leading zero (e.g., 5)
    "m": "%-M",
    # Minutes with leading zero (e.g., 05)
    "mm": "%M",
    # Seconds without leading zero (e.g., 8)
    "s": "%-S",
    # Seconds with leading zero (e.g., 08)
    "ss": "%S",
    # AM/PM indicator in uppercase (e.g., AM)
    "AM/PM": "%p",
    # AM/PM indicator in lowercase (e.g., am)
    "am/pm": "%#p",
    # Milliseconds (e.g., 567)
    "0": "%f",
    # Milliseconds without leading zeros (e.g., 7)
    "000": "%3f",
    # Milliseconds without trailing zeros (e.g., 567)
    "0.": "%.3f",
    # Time as month and year (e.g., May 2023)
    "mmm\ yyyy": "%b %Y",
}
