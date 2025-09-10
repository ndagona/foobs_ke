from pathlib import Path
import cv2
import os
from PIL import Image
from matplotlib import pyplot as plt
from typing import NoReturn, Never


class Vision:
    def __init__(self, path: Path):
        self.path = path
        self.acceptapleImages = ["png", "jpeg", "jpg"]

    def main(self) -> Never:
        IMG: Image = self.loadImage()
        minorProcessing: Image = self.setGrayScale(self.setBlur(self.layEdges(IMG)))
        self.counta(IMG=self.setGrayScale(IMG), Original=IMG)

    def loadImage(self) -> Image:
        if not os.path.isfile(self.path):
            raise ValueError("Error!! Invalid Image Path")
        if not any(imageType in self.path for imageType in self.acceptapleImages):
            raise ValueError("Error: Image format not supported!!")
        return cv2.imread(self.path)

    def setCorrectColor(self, IMG: Image) -> Image:
        return cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)

    def setGrayScale(self, IMG: Image) -> Image:
        return cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)

    def setBlur(self, IMG: Image) -> Image:
        return cv2.GaussianBlur(IMG, (5, 5), 0)

    def layEdges(self, IMG: Image) -> Image:
        """
        # 2. Edge Detection
        # Adjust the thresholds below to control edge sensitivity.
        # The Canny algorithm detects edges where the gradient falls between threshold1 and threshold2.
        """
        return cv2.Canny(IMG, 50, 100)

    def counta(self, IMG: Image, Original: Image) -> NoReturn:
        # contours, _ = cv2.findContours(IMG, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ret, thresh = cv2.threshold(IMG, 127, 255, 0)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print("I was here")

        # 4. Contour Filtering
        # We assume the largest contour with 4 vertices is our document.
        # Sort contours by area, largest first
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[
            :5
        ]  # Get top 5 largest contours

        document_contour = None

        for contour in contours:
            # Approximate the contour to a simpler polygon
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(
                contour, 0.02 * peri, True
            )  # 0.02 is the approximation accuracy

            # If our approximated contour has four points, we can assume we found the document
            if len(approx) == 4:
                document_contour = approx
                break

        # Check if we found a document
        if document_contour is None:
            print("No quadrilateral document contour found. Using full image.")
            # You might need to adjust your preprocessing or Canny thresholds here!
        else:
            # Draw the contour on the original image to verify
            image_with_contour = Original.copy()
            cv2.drawContours(
                image_with_contour, [document_contour], -1, (0, 255, 0), 10
            )  # Green contour, thickness 10
            plt.imshow(image_with_contour)
            plt.title("Detected Document Contour")
            plt.axis("off")
            plt.show()

    def showImage(self, IMG: Image) -> NoReturn:
        plt.imshow(IMG)
        plt.title("Zee Image")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    cls = Vision("Image.jpg").main()
