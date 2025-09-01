from rawData.getData import Data
from pathlib import Path
import pandas as pd
from SQL_codex.DB_conn import DatabaseConnect


def printer(msg: str) -> None:
    print()
    print()
    print(msg)


class App:
    def __init__(self) -> None:

        self.path = Path(__file__).parent / "rawData" / "data.csv"
        self.draft0 = Path(__file__).parent / "rawData" / "draft0.csv"

    def main(self) -> None:

        data_instance = Data(self.path, self.draft0)
        data: pd.Dataframe = data_instance.main()
        printer(data.head())
        db_instance = DatabaseConnect()
        db_instance.main(table_name="foobs_data_ke_001", data=data)


if __name__ == "__main__":
    cls = App()
    cls.main()
