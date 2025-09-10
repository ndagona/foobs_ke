import pandas as pd
from typing import Never
from pathlib import Path


class theExporter:
    def __init__(self, data: pd.DataFrame) -> Never:
        self.data: pd.DataFrame = data

    def __isPandasDataFrame(self) -> bool:
        """
        Checks if the data passed is actually a pandas dataframe.
        This prevents execution when data format is wrong
        """
        return isinstance(self.data, pd.DataFrame)

    def exportToCSV(self, path: Path) -> bool:
        if not self.__isPandasDataFrame():
            raise ValueError("Error: Not a data panda frame")
        if ".csv" not in str(path).lower():
            raise NameError("Error!: Not a valid csv name/ path")
        self.data.to_csv(
            path,
            index=False,
        )
