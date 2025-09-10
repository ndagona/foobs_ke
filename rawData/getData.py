from pathlib import Path
import os
import pandas as pd
import numpy as np


def printer(msg: str) -> None:
    ...
    # print()
    # print()
    # print(msg)


class Data:
    def __init__(self, path: Path, draft0: Path) -> None:
        self.path: Path = path
        self.draft0 = draft0
        printer(f"Data path: {self.path}")
        printer(f"Draft path: {self.draft0}")

    def main(self) -> None:
        if not os.path.isfile(self.draft0):
            self.initRun()

        dataFrame = self.getData()
        if not self.colsExist(dataFrame):
            raise ValueError("Columns do not match expected schema.")
        return self.stripCols(dataFrame)

    def stripCols(self, df: pd.DataFrame) -> pd.DataFrame:
        expected_cols = self.Columns()
        df = df[expected_cols]
        return df

    def colsExist(self, df: pd.DataFrame) -> bool:
        expected_cols = set(self.Columns())
        actual_cols = set(df.columns)
        return expected_cols.issubset(actual_cols)

    def getData(self) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        df.replace({np.nan: None}, inplace=True)
        return self.reformatTimestampToDate(df)

    def reformatTimestampToDate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.where(pd.notna(df), None)
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"], format="mixed", errors="coerce"
        ).dt.date

        df["Timestamp"] = df["Timestamp"].where(df["Timestamp"].notna(), None)

        df["Date of Birth"] = pd.to_datetime(
            df["Date of Birth"], format="mixed", errors="coerce"
        ).dt.date

        df["Date of Birth"] = df["Date of Birth"].where(
            df["Date of Birth"].notna(), None
        )

        df["Row ID"] = df.index + 1

        df["ID Number"] = df["ID Number"].astype(str).str.replace(".0", "", regex=False)

        return df

    def Columns(self) -> list:
        cols: dict = {
            "Timestamp": "Timestamp",
            "First_Name": "First Name",
            "Last_Name": "Last Name",
            "email": "Email Address",
            "Mobile_no": "Mobile no",
            "Status": "Status",
            "Gender": "Gender",
            "ID_number": "ID Number",
            "DOB": "Date of Birth",
            "FO_picture": "Photo of the Front Officer",
            "ID_photo": "Front ID Picture",
        }
        return list(cols.values())

    def initRun(self) -> None: ...


if __name__ == "__main__":
    path = "./data.csv"
    draft0 = "./draft0.csv"
    cls = Data(path, draft0)
    cls.main()
