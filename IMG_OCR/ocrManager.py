import easyocr
import cv2
from PIL import Image
from pathlib import Path
import os
import re
from copy import deepcopy
import numpy as np
import warnings

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

        else:
            easyocr_dict: str = easyocr_text
        return [easyocr_dict, id_number, dob]
        """
        WHAT COULD GO WRONG
        - Keys used to identify not being found completely
        - Wrong image throwing error after extraction
        SOLUTIONS
        -Handle exceptions
        -Have a backup routine when dictionary fails
        """

    def postProcessingIMG(self, IMG: Image) -> Image:
        # Greyscale
        IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
        newName = self.image_path.split("/")[-1].split(".")[0]
        outPuttest = f"./temp/{newName}.{self.image_path.split(".")[-1]}"
        # Denoize
        outPuttestD = f"./temp/denoized-{newName}.{self.image_path.split(".")[-1]}"
        IMG: Image = cv2.bilateralFilter(IMG, 9, 75, 75)
        cv2.imwrite(outPuttestD, IMG)
        # Clahe
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(IMG)
        image = cv2.resize(IMG, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BAYER_BG2GRAY)
        cv2.imwrite(outPuttest, image)
        return image

    def preprocess_image(self, IMG, visualize=False):
        """
        Preprocess image for optimal OCR performance

        Args:
            image_path (str): Path to the input image
            visualize (bool): Whether to show processing steps

        Returns:
            processed_image: Preprocessed image ready for OCR
        """
        # Read the image
        image = IMG

        # Store original for visualization if needed
        original = image.copy()

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Noise reduction with bilateral filter (preserves edges)
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)

        # Contrast enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(denoised)

        # Thresholding to create binary image
        # Using adaptive threshold to handle varying lighting conditions
        binary = cv2.adaptiveThreshold(
            contrast_enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )

        # Morphological operations to remove noise and strengthen text
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)

        # Optional: Deskew image if needed
        processed = self.deskew(processed)

        # Visualization of processing steps
        if visualize:
            self.visualize_processing(
                original, gray, denoised, contrast_enhanced, binary, processed
            )

        return processed

    def deskew(self, image):
        """
        Deskew image to correct text alignment
        """
        # Find all contours
        coords = np.column_stack(np.where(image > 0))

        # Get angle of skewness
        angle = cv2.minAreaRect(coords)[-1]

        # Adjust angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # Rotate image to correct skew
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )

        return rotated


if __name__ == "__main__":
    cls = Eazi("profile.jpg").main()
