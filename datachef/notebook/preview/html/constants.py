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
