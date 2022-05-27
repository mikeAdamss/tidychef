from dataclasses import dataclass


@dataclass
class SupportedLocalFiles:
    CSV: str = "csv"

    def __repr__(self):
        return ",".join(self.CSV)


SUPPORTED_LOCAL_FILETYPES = SupportedLocalFiles()
