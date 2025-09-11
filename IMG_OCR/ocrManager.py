import easyocr
import cv2
from PIL import Image
from pathlib import Path
import os
import re
from copy import deepcopy
import numpy as np
import warnings
from datetime import datetime
import random

warnings.filterwarnings("ignore")


class Eazi:
    def __init__(self) -> None:
        self.easyocr_reader = easyocr.Reader(
            ["en", "sw"], gpu=False, download_enabled=True, recognizer=True
        )

    def main(self, image_path: Path) -> str:
        if not os.path.isfile(image_path):
            print("Invalid Image Path")
            return (None, None, None)
        IMG: Image = cv2.imread(image_path)
        return self.OCR(IMG)

    def listToDict(self, data: list[str]) -> dict:
        assert isinstance(data, list)
        dictData: dict = dict()
        tempData: list[str] = deepcopy(data)
        while len(tempData) > 0:
            if len(tempData) == 1:
                dictData[tempData[0]] = None
                tempData.pop(0)

            elif len(tempData) > 1:
                dictData[tempData[0]] = tempData[1]
                tempData.pop(0)
                tempData.pop(0)
        return dictData

    def OCR(self, IMG) -> str:
        easyocr_results = self.easyocr_reader.readtext(IMG)
        easyocr_text: str = " ".join([res[1] for res in easyocr_results])
        dob: str = None
        id_number: str = None
        easyocr_dict: dict = None
        if (
            len(re.sub(r"[^A-Za-z]+", "", easyocr_text)) > 5
        ):  # 5 is a value pulled outta air
            easyocr_dict: dict = self.listToDict(
                [
                    str(res[1]).title()
                    for res in easyocr_results
                    if len(str(res[1]).strip()) > 2
                ]
            )
        if isinstance(easyocr_dict, dict):
            """
            WHAT COULD GO WRONG
            - Keys used to identify not being found completely
            - Wrong image throwing error after extraction
            SOLUTIONS
            -Handle exceptions
            -Have a backup routine when dictionary fails
            """
            birth: list[str, str] = ["birth", "dob", "d.o.b"]
            id: list[str, str] = ["number", "id"]
            notId: list[str, str] = ["seria", "serial", "seri", "ser"]

            for key, val in easyocr_dict.items():
                for dobKeyword in birth:
                    if re.search(dobKeyword, str(key).lower()):
                        # We have distirict of birth and date of birth
                        # District of birth has only letters so filtering by digits should work
                        if re.search(r"[0-9]+", val):
                            dob = val
                            break
                if dob is None:
                    if isinstance(easyocr_dict, dict):
                        # Inverse
                        for dobKeyword in birth:
                            if re.search(dobKeyword, str(val).lower()):
                                # We have distirict of birth and date of birth
                                # District of birth has only letters so filtering by digits should work
                                if re.search(r"[0-9]+", key):
                                    dob = key
                                    break
                if dob is None:
                    dob = self.rawExtractionDOB(str(easyocr_dict))

                for idKeyword in id:
                    if re.search(idKeyword, str(key).lower()):
                        checkSerial: list[str, str] = any(
                            [x in str(key).lower() for x in notId]
                        )
                        if checkSerial:
                            break
                        if re.search(r"[0-9]+", val):
                            id_number: str = val
                if id_number is None:
                    if isinstance(easyocr_dict, dict):
                        for idKeyword in id:
                            if re.search(idKeyword, str(val).lower()):
                                checkSerial: list[str, str] = any(
                                    [x in str(val).lower() for x in notId]
                                )
                                if checkSerial:
                                    break
                                if re.search(r"[0-9]+", key):
                                    id_number: str = key
                if id_number is None:
                    id_number = self.rawExtractionID(str(easyocr_dict))

        else:
            easyocr_dict: str = easyocr_text
            if id_number is None:
                id_number = self.rawExtractionID(str(easyocr_text))
            if dob is None:
                dob = self.rawExtractionDOB(str(easyocr_text))
        return [easyocr_dict, id_number, dob]

    def rawExtractionDOB(self, text: str) -> datetime.date:
        dob: datetime.date = None
        """
        Final solution to fix cases where date is not extracted by the OCR technique
        There is date of issue and prolly expiry date, fetch the oldest date
        """
        dateFormat001: str = (
            "String with dots eg 19.12.2025 which equates to dd/mm/yyyy"
        )
        dateFormat001Regex: re.Pattern = re.compile(
            r"((\d{1,4})[\s]*[.,][\s]*(\d{1,4})[\s]*[.,][\s]*(\d{1,4}))"
        )

        results: set = [
            datetime.strptime(
                (re.sub(r"[\.,]", "-", re.sub(r"[\s]+", "", x[0]))), "%d-%m-%Y"
            ).date()
            for x in re.findall(dateFormat001Regex, text)
        ]

        if len(results) > 0:
            dob = min(results)
        return dob

    def rawExtractionID(self, text: str) -> int:
        idNumber: str = None
        """
        ISSUES
        Too many loosing heroines, hehe
        - More than one int val in the national ID => [Id number,serial Number, some random floating num??!]
        The regex ^[0-9]{6,9}$ will read all of this prolly
        Use russian rollete if more than one val is found, hehe
        """
        idRegex: re.Pattern = re.compile(r"[0-9]{6,9}")
        results: list[str, str] = re.findall(idRegex, text)
        if len(results) > 0:
            idNumber = results[random.randint(0, (len(results) - 1))]
        return idNumber


if __name__ == "__main__":
    cls = Eazi("profile.jpg").main()
