import numpy as np
import cv2 as cv


def him() -> None:
    im = cv.imread("him.png").copy()
    assert im is not None, "file could not be read, check with os.path.exists()"
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    edged = cv.Canny(imgray, 30, 200)
    cv.imwrite("edge.jpg", edged)
    ret, thresh = cv.threshold(edged, 127, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    print("Number of Contours Found = " + str(len(contours)))
    print("Number of Contours Found = " + str(len(contours)))
    document_contour = None
    for cont in contours:
        # Approximate the contour to a simpler polygon
        peri = cv.arcLength(cont, True)
        approx = cv.approxPolyDP(
            cont, 0.02 * peri, True
        )  # 0.02 is the approximation accuracy

        # If our approximated contour has four points, we can assume we found the document
        if len(approx) == 4:
            document_contour = approx
            break
    if document_contour is None:
        print("No quadrilateral document contour found. Using full image.")
    else:
        print("Number of doc Contours Found = " + str(len(document_contour)))
        cv.imwrite("test3.jpg", im)
        image_with_contour = cv.imread("test3.jpg")
        cv.drawContours(image_with_contour, contours, -1, (0, 255, 0), 3)
        # image_with_contour = cv.imread("test2.jpg")
        cv.imwrite("test3.jpg", image_with_contour)

    return

    document_contour = None
    for contour in contours:
        # Approximate the contour to a simpler polygon
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(
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
        print("Drawing...")
        # Draw the contour on the original image to verify
        cv.imwrite("test2.jpg", im)
        image_with_contour = cv.imread("test2.jpg")
        cv.drawContours(image_with_contour, [document_contour], -1, (0, 255, 0), 10)
        cv.imwrite("test3.jpg", image_with_contour)


him()
