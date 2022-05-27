from pathlib import Path

import pivoter.handlers.input.base
import pivoter.exceptions


class LocalCsvHandler(pivoter.handlers.input.base.BaseInputHandler):
    def parse(self):

        if not isinstance(self.source, Path):
            raise pivoter.exceptions.FileInputError(
                "A local csv input should be provided in the form of a pathlib.Path"
            )

        raise NotImplementedError
