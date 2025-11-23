BORDER_CELL_COLOUR = "lightgrey"
BORDER_CELL_SECONDARY_COLOUR = "#999999"
NO_COLOUR = "white"
WARNING_COLOUR = "#ff8080"

COLOURS = [
    "cyan",
    "#99ff99",
    "#eeccff",
    "#ffe066",
    "#ff4da6",
    "#ff9933",
    "#4d4dff",
    "#b3d9ff",
    "#00b3b3",
    "#99ffcc",
    "#b380ff",
]

# Separate color palette for multiple selection combinations
# These colors are distinct from individual selection colors to avoid confusion
MULTIPLE_SELECTION_COLOURS = [
    "#ffb3b3",  # Light red
    "#ffd9b3",  # Light orange  
    "#ffffb3",  # Light yellow
    "#d9ffb3",  # Light lime
    "#b3ffb3",  # Light green
    "#b3ffff",  # Light cyan
    "#c6e6ff",  # Very light blue (different from #b3d9ff)
    "#d9b3ff",  # Light purple
    "#ffb3ff",  # Light magenta
    "#ffb3d9",  # Light pink
    "#e6ccb3",  # Light brown
    "#cccccc",  # Light gray
]

# Simple CSS to make it pretty-ish
INLINE_CSS = """
    <style>
    table, th, td {
        border: 1px solid;
    }

    table {
        border-collapse: collapse;
    }

    td {
        align: center;
        border: 1px  black solid !important;
        color: black !important;
    }

    th, td {
        padding: 5px;
    }

    </style>
    """
