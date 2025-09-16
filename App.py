from rawData.getData import Data
from pathlib import Path
import pandas as pd
from SQL_codex.DB_conn import DatabaseConnect
from PostgresSQL.queryData import getQuery
import time
from Exports.fileExport import theExporter
from IMG_OCR.Listings import ImageListing
import os


class App:
    def __init__(
        self, path: Path, draft0: Path, tableName: str, exportPath: Path
    ) -> None:

        self.path: Path = path
        self.draft0: Path = draft0
        self.tableName: str = tableName
        self.exportPath: Path = exportPath

        # Draft does nothing, functionality was deemed unnecessary

        # self.path = Path(__file__).parent / "rawData" / "data.csv"
        # self.draft0 = Path(__file__).parent / "rawData" / "draft0.csv"

    def main(self) -> None:

        data_instance = Data(self.path, self.draft0)
        data: pd.DataFrame = data_instance.main()
        db_instance = DatabaseConnect()
        db_instance.main(table_name=self.tableName, data=data)
        conn = db_instance.connect_postgres()
        sqlQuery = getQuery("PostgresSQL\CoreRaw.sql")
        QueriedData: pd.DataFrame = db_instance.queryData(sqlQuery, conn)
        # ImageListingClass: pd.DataFrame = ImageListing(QueriedData).main()
        exportInstance = theExporter(QueriedData)
        exportInstance.exportToCSV(path=self.exportPath)


def loopThroughList(folderPath: Path) -> None:
    if not os.path.isdir(folderPath):
        raise ValueError("Invalid Path, please recheck shared folder is accurate")
    CSVS: list[Path, Path] = [
        Path(folderPath) / x for x in os.listdir(folderPath) if x.endswith(".csv")
    ]
    if len(CSVS) < 1:
        raise ValueError("No files in the specified folder")
    for ind, csvPath in enumerate(CSVS, start=1):
        print()
        print(f"Working on file 000{ind} and the Path is : {csvPath}".center(120, "*"))
        print()
        App(
            path=csvPath,
            draft0=f"./Exports/DraftData_000{ind}.csv",
            tableName=f"foobs_data_ke_000{ind}",
            exportPath=f"./Exports/ExportedData_000{ind}.csv",
        ).main()


if __name__ == "__main__":
    # cls = App()
    # cls.main()
    loopThroughList("./rawData")
