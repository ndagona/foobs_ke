from rawData.getData import Data
from pathlib import Path
import pandas as pd
from SQL_codex.DB_conn import DatabaseConnect
from PostgresSQL.queryData import getQuery
import time
from Exports.fileExport import theExporter
from IMG_OCR.Listings import ImageListing


class App:
    def __init__(self) -> None:

        self.path = Path(__file__).parent / "rawData" / "data.csv"
        self.draft0 = Path(__file__).parent / "rawData" / "draft0.csv"

    def main(self) -> None:

        data_instance = Data(self.path, self.draft0)
        data: pd.DataFrame = data_instance.main()
        db_instance = DatabaseConnect()
        db_instance.main(table_name="foobs_data_ke_001", data=data)
        conn = db_instance.connect_postgres()
        sqlQuery = getQuery("PostgresSQL\CoreRaw.sql")
        QueriedData: pd.DataFrame = db_instance.queryData(sqlQuery, conn)
        ImageListingClass: pd.DataFrame = ImageListing(QueriedData.head(3)).main()
        exportInstance = theExporter(ImageListingClass)
        exportInstance.exportToCSV(path="./Exports/Data.csv")


if __name__ == "__main__":
    cls = App()
    cls.main()
