import pandas as pd
from typing import NoReturn, Never
from pathlib import Path
import gspread


class GoogleSheetsWorkFlow:
    def __init__(self, sheetUri: str, sheetTab: str, secretsJSON: Path) -> NoReturn:
        self.sheetUri = sheetUri
        self.sheetTab = sheetTab
        self.secretJSON = secretsJSON

    def main(self) -> Never: ...

    def createSheetConnection(self):
        """
        Attempts to create a connection to the sheet uri shared
        """

        conn = gspread.service_account(
            filename=self.secretJSON,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
            http_client=gspread.HTTPClient,
            # http_client=gspread.BackOffHTTPClient # Opt for this to avoid rate limiting
        )

    def writeToSheet(self, data: pd.DataFrame) -> bool:
        """
        Clears data in the tab and pastes the new data
        """
        ...

    def appendToSheet(self, data: pd.DataFrame) -> bool:
        """
        Writes the new data after the last row
        """

    def copyDataFromSheet(self, rowLimit: int = 1000) -> pd.DataFrame:
        """
        Copies data from sheet and returns it in a pandas dataframe
        """

    def getLastRow(self) -> int: ...


if __name__ == "__main__":
    sheetUri = "13Y45JjN_lqgxP8szD0zKwmualTj1_HwNhjM4PM2bxlM"
    sheetTab = "MD"
    secretsJSON = ""
    cls = GoogleSheetsWorkFlow(sheetUri, sheetTab, secretsJSON)
    cls.createSheetConnection()
