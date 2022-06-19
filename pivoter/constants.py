from dataclasses import dataclass


@dataclass
class SupportedLocalFiles:
    CSV: str = "csv"

    def __repr__(self):
        return ",".join([self.CSV])


SUPPORTED_LOCAL_FILETYPES = SupportedLocalFiles()


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

# Aliases
ABOVE = UP
BELOW = DOWN
