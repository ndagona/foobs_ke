import pandas as pd
import urllib.request
import re
from pathlib import Path
from IMG_OCR.ocrManager import Eazi
from pprint import pprint


class ImageListing:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data

    def main(self) -> pd.DataFrame:
        OCR_class = Eazi()
        ocrText: list[str] = []
        idNumberData: list[str] = []
        dobData: list[str] = []
        for _, row in self.data.iterrows():
            idLink: str = row["Front ID Picture"]
            ocrExtraction: None = None
            idNumber: None = None
            dob: None = None
            new = re.search(
                r"(id\=)[A-Za-z0-9\_\-]+|(d\/)[A-Za-z0-9\_\-]+", idLink
            ).group()
            newNew = re.sub(r"(id\=)|(d\/)", "", new)
            downloadLink: str = (
                f"https://drive.google.com/uc?export=download&id={newNew}"
            )
            imagePath: Path = f"./tempImages/{re.sub(r"[^A-Za-z0-9]+","", newNew)}.png"
            downloadStatus: bool = self.downloadImage(downloadLink, imagePath)
            if downloadStatus:
                returnedData: list[dict | str, str, str] = OCR_class.main(imagePath)
                ocrExtraction: list | str = returnedData[0]
                idNumber: str = returnedData[1]
                dob: str = returnedData[2]
            ocrText.append(ocrExtraction)
            idNumberData.append(idNumber)
            dobData.append(dob)

        self.data["OCR Text"] = ocrText
        self.data["OCR ID Number"] = idNumber
        self.data["OCR Date Of Birth"] = dobData
        return self.data

    def downloadImage(self, link: str, filename: str) -> bool:
        try:
            urllib.request.urlretrieve(link, filename)
            return True
        except Exception as e:
            print(f"Failed to download with link \n {link} \n Err: {e}")
            return False
