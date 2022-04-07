import cv2
import numpy as np
import random
from decorators import size_checker, text_size


class Output:

    @staticmethod
    def frame():
        while True:
            #image = cv2.imread('C:\\Users\\yura0\\Desktop\\5.jpg')
            image = cv2.imread('C:\\Users\\yura0\\Desktop\\1_1.jpg')
            #image = cv2.imread('C:\\Users\\yura0\\Desktop\\measure_object_size\\phone_aruco_marker.jpg')

            # Get Aruco marker
            parameters = cv2.aruco.DetectorParameters_create()
            aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
            corners, _, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters = parameters)

            # Draw polygon around the marker
            int_corners = np.int0(corners)
            cv2.polylines(image, int_corners, True, (0, 255, 0), 1)

            # Aruco Perimeter
            aruco_perimeter = cv2.arcLength(corners[0], True)

            # Pixel to cm ratio
            pixel_cm_ratio = aruco_perimeter / 20

            # Scale
            scale_percent = 100 # scale count
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

            # Setup to gray color
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Morph open with a elliptical shaped kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

            # Find contours and draw minimum enclosing circle
            cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                # Get Width and Height of the Objects by applying the Ratio pixel to cm
                (x, y), r = cv2.minEnclosingCircle(c)
                r = round(r, 2)

                # Convert px to radius in cm
                object_radius = round(((r / pixel_cm_ratio) / 2.1), 3)
                print(object_radius)

                cv2.putText(image,
                            f"R{str(object_radius)} cm | {random.randint(1, 5)}",
                            (int(int(size_checker(int(y), int(r), int(x))[1])),
                             int(size_checker(int(y), int(r), int(x))[0])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            text_size(r)[0], (0, 0, 255),
                            text_size(r)[1])
                # Main stroke
                #cv2.circle(image,(int(x), int(y)), int(r), (0,0,255), 2)
                # Center point
                cv2.circle(image, (int(x), int(y)), 2, (0, 0, 255), 2)
                # Note line
                cv2.line(image, (int(x), int(y)), (int(x) + int(r), int(y)), (0, 0, 255), 2)

            cv2.imshow('output post processing', image)
            cv2.imshow("thresh", thresh)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

    cv2.destroyAllWindows()

# Run without main
a = Output().frame()

