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
    # Month without leading zero (e.g., 1)
    "M": "%-m",
    # Year without century (e.g., 21)
    "YY": "%y",
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
    # Month as an abbreviated string followed by year as a literal (e.g., Jan 2023)
    "mmm\\ yyyy": "%b\\ %Y",
    "mmm yyyy": "%b %Y",
    # Day/Month/Year with 2-digit year (e.g., 1/5/23)
    "d/m/yy": "%d/%m/%y",
    # Day/Month/Year with 4-digit year (e.g., 1/5/2023)
    "d/m/yyyy": "%d/%m/%Y",
    # Month/Day/Year with 2-digit year (e.g., 5/1/23)
    "m/d/yy": "%m/%d/%y",
    # Month/Day/Year with 4-digit year (e.g., 5/1/2023)
    "m/d/yyyy": "%m/%d/%Y",
    # Day/Month with 2-digit year (e.g., 1/5/23)
    "d/m": "%d/%m",
    # Month/Day with 2-digit year (e.g., 5/1/23)
    "m/d": "%m/%d",
    # Day with leading zero (e.g., 01)
    "DD": "%d",
    # Day of year with leading zero (e.g., 032)
    "DDDD": "%j",
    # Month with leading zero (e.g., 01)
    "MM": "%m",
    # Month abbreviation (e.g., Jan)
    "MMM": "%b",
    # Month full name (e.g., January)
    "MMMM": "%B",
    # Year without century (e.g., 21)
    "YY": "%y",
    # Year with century (e.g., 2023)
    "YYYY": "%Y",
    # Day-Month-Year with 2-digit year (e.g., 01-05-23)
    "DD-MM-YY": "%d-%m-%y",
    # Day-Month-Year with 4-digit year (e.g., 01-05-2023)
    "DD-MM-YYYY": "%d-%m-%Y",
    # Day/Month/Year with 2-digit year (e.g., 01/05/23)
    "DD/MM/YY": "%d/%m/%y",
    # Day/Month/Year with 4-digit year (e.g., 01/05/2023)
    "DD/MM/YYYY": "%d/%m/%Y",
    # Day.Month.Year with 2-digit year (e.g., 01.05.23)
    "DD.MM.YY": "%d.%m.%y",
    # Day.Month.Year with 4-digit year (e.g., 01.05.2023)
    "DD.MM.YYYY": "%d.%m.%Y",
    # Month-Day-Year with 2-digit year (e.g., 5-1-21)
    "MM-DD-YY": "%m-%d-%y",
    # Month-Day-Year with 4-digit year (e.g., 5-1-2023)
    "MM-DD-YYYY": "%m-%d-%Y",
    # Month/Day/Year with 2-digit year (e.g., 5/1/21)
    "MM/DD/YY": "%m/%d/%y",
    # Month/Day/Year with 4-digit year (e.g., 5/1/2023)
    "MM/DD/YYYY": "%m/%d/%Y",
    # Day Month Year (e.g., 01 May 2023)
    "DD MMM YYYY": "%d %b %Y",
    # Day Month Year with full month name (e.g., 01 May 2023)
    "DD MMMM YYYY": "%d %B %Y",
    # Month full name, Day with leading zero, Year with 2-digit year (e.g., May 01, 23)
    "MMMM DD, YY": "%B %d, %y",
    # Month full name, Day with leading zero, Year with 4-digit year (e.g., May 01, 2023)
    "MMMM DD, YYYY": "%B %d, %Y",
    # Day-Month abbreviation-Year with 2-digit year (e.g., 01-May-21)
    "DD-MMM-YY": "%d-%b-%y",
    # Day-Month abbreviation-Year with 4-digit year (e.g., 01-May-2023)
    "DD-MMM-YYYY": "%d-%b-%Y",
    # Day/Month abbreviation/Year with 2-digit year (e.g., 01/May/21)
    "DD/MMM/YY": "%d/%b/%y",
    # Day/Month abbreviation/Year with 4-digit year (e.g., 01/May/2023)
    "DD/MMM/YYYY": "%d/%b/%Y",
    # Day Month abbreviation, Year with 2-digit year (e.g., 1 May 23)
    "D MMM YY": "%-d %b %y",
    # Day Month abbreviation, Year with 4-digit year (e.g., 1 May 2023)
    "D MMM YYYY": "%-d %b %Y",
    # Day Month full name, Year with 2-digit year (e.g., 1 May 23)
    "D MMMM YY": "%-d %B %y",
    # Day Month full name, Year with 4-digit year (e.g., 1 May 2023)
    "D MMMM YYYY": "%-d %B %Y",
    # Month abbreviation-Day-Year with 2-digit year (e.g., May 1, 23)
    "MMM D, YY": "%b %d, %y",
    # Month abbreviation-Day-Year with 4-digit year (e.g., May 1, 2023)
    "MMM D, YYYY": "%b %d, %Y",
    # Month abbreviation Day, Year with 2-digit year (e.g., May 01, 23)
    "MMM DD, YY": "%b %d, %y",
    # Month abbreviation Day, Year with 4-digit year (e.g., May 01, 2023)
    "MMM DD, YYYY": "%b %d, %Y",
    # Month full name-Day-Year with 2-digit year (e.g., May 1, 23)
    "MMMM D, YY": "%B %d, %y",
    # Month full name-Day-Year with 4-digit year (e.g., May 1, 2023)
    "MMMM D, YYYY": "%B %d, %Y",
    # Month full name Day, Year with 2-digit year (e.g., May 01, 23)
    "MMMM DD, YY": "%B %d, %y",
    # Month full name Day, Year with 4-digit year (e.g., May 01, 2023)
    "MMMM DD, YYYY": "%B %d, %Y",
    # Day-Month abbreviation-Year with 2-digit year (e.g., 01-May-21)
    "DD-MMM-YY": "%d-%b-%y",
    # Day-Month abbreviation-Year with 4-digit year (e.g., 01-May-2023)
    "DD-MMM-YYYY": "%d-%b-%Y",
    # Day/Month abbreviation/Year with 2-digit year (e.g., 01/May/21)
    "DD/MMM/YY": "%d/%b/%y",
    # Day/Month abbreviation/Year with 4-digit year (e.g., 01/May/2023)
    "DD/MMM/YYYY": "%d/%b/%Y",
    # Day Month abbreviation, Year with 2-digit year (e.g., 1 May 23)
    "D MMM YY": "%-d %b %y",
    # Day Month abbreviation, Year with 4-digit year (e.g., 1 May 2023)
    "D MMM YYYY": "%-d %b %Y",
    # Day Month full name, Year with 2-digit year (e.g., 1 May 23)
    "D MMMM YY": "%-d %B %y",
    # Day Month full name, Year with 4-digit year (e.g., 1 May 2023)
    "D MMMM YYYY": "%-d %B %Y",
    # Month abbreviation-Day with 2-digit year (e.g., May 1)
    "MMM D": "%b %-d",
    # Month abbreviation-Day with 4-digit year (e.g., May 1)
    "MMM D": "%b %-d",
    # Month full name-Day with 2-digit year (e.g., May 1)
    "MMMM D": "%B %-d",
    # Month full name-Day with 4-digit year (e.g., May 1)
    "MMMM D": "%B %-d",
    # Day-Month abbreviation with 2-digit year (e.g., 1-May)
    "D-MMM": "%-d-%b",
    # Day-Month abbreviation with 4-digit year (e.g., 1-May)
    "D-MMM": "%-d-%b",
    # Day-Month full name with 2-digit year (e.g., 1-May)
    "D-MMMM": "%-d-%B",
    # Day-Month full name with 4-digit year (e.g., 1-May)
    "D-MMMM": "%-d-%B",
    # Month abbreviation-Year with 2-digit year (e.g., May-23)
    "MMM-YY": "%b-%y",
    # Month abbreviation-Year with 4-digit year (e.g., May-2023)
    "MMM-YYYY": "%b-%Y",
    # Month full name-Year with 2-digit year (e.g., May-23)
    "MMMM-YY": "%B-%y",
    # Month full name-Year with 4-digit year (e.g., May-2023)
    "MMMM-YYYY": "%B-%Y",
    # Day, Month abbreviation (e.g., 1, May)
    "D, MMM": "%-d, %b",
    # Day, Month abbreviation (e.g., 1, May)
    "D, MMM": "%-d, %b",
    # Day, Month full name (e.g., 1, May)
    "D, MMMM": "%-d, %B",
    # Day, Month full name (e.g., 1, May)
    "D, MMMM": "%-d, %B",
    # Month abbreviation-Day (e.g., May 1)
    "MMM D": "%b %-d",
    # Month abbreviation-Day (e.g., May 1)
    "MMM D": "%b %-d",
    # Month full name-Day (e.g., May 1)
    "MMMM D": "%B %-d",
    # Month full name-Day (e.g., May 1)
    "MMMM D": "%B %-d",
    # Day-Month abbreviation (e.g., 1-May)
    "D-MMM": "%-d-%b",
    # Day-Month abbreviation (e.g., 1-May)
    "D-MMM": "%-d-%b",
    # Day-Month full name (e.g., 1-May)
    "D-MMMM": "%-d-%B",
    # Day-Month full name (e.g., 1-May)
    "D-MMMM": "%-d-%B",
    # Month abbreviation-Year (e.g., May-23)
    "MMM-YY": "%b-%y",
    # Month abbreviation-Year (e.g., May-2023)
    "MMM-YYYY": "%b-%Y",
    # Month full name-Year (e.g., May-23)
    "MMMM-YY": "%B-%y",
    # Month full name-Year (e.g., May-2023)
    "MMMM-YYYY": "%B-%Y",
}