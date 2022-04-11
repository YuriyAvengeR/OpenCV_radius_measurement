import cv2
import numpy as np
from decorators import size_checker, text_size
from connect import db_connect, target_color, target_name, tolerance_measurement
from math import sqrt

class Output:

    @staticmethod
    def frame():
        cap = cv2.VideoCapture(0)
        while True:

            # Select method video or image
            #ret, image = cap.read()
            image = cv2.imread('./1_1.jpg')

            try:
                # Aruco setup
                parameters = cv2.aruco.DetectorParameters_create()
                aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
                corners, _, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters = parameters)

                # Aruco draw border
                int_corners = np.int0(corners)
                #cv2.polylines(image, int_corners, True, (0, 255, 0), 1)

                # Aruco get perimeter
                aruco_perimeter = cv2.arcLength(corners[0], True)

                # Text Label for Aruco status
                cv2.putText(image, "ACF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (107,255,53), 3)
            except(IndexError):
                aruco_perimeter = 1
                cv2.putText(image, "ANF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (53,255,236), 3)

            # Pixel graduation
            pixel_cm_ratio = aruco_perimeter / 20

            # Get origin aruco size on cm
            aruco_size = (((aruco_perimeter / pixel_cm_ratio) / 4) /2.1)
            aruco_size = (aruco_size * sqrt(2)) / 2
            aruco_size = round(aruco_size, 2)

            # Picture scaling
            scale_percent = 100 # scale count
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

            # Setup to gray color
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Morph
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

            radius_list = []
            data = 0

            # Find contours [main]
            cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:

                # Get Width and Height of the Objects by applying the Ratio pixel to cm
                (x, y), r = cv2.minEnclosingCircle(c)
                r = round(r, 2)

                # Convert px to radius in cm
                object_radius = round(((r / pixel_cm_ratio) / 2.1), 2)
                cv2.putText(image,
                            f"R{str(object_radius)} cm",
                            (int(int(size_checker(int(y), int(r), int(x))[1])),
                             int(size_checker(int(y), int(r), int(x))[0])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            text_size(r)[0], (0, 0, 255),
                            text_size(r)[1])

                # Select object to detect
                try:
                    object_radius = round(object_radius, 2)
                    radius_list.append(object_radius)
                    list_len = len(radius_list)
                    if list_len == 2:
                        radius_list.remove(aruco_size)
                        data = float(radius_list[0])
                except(ValueError):
                    radius_list.clear()

                # Init current data about object
                obj_size = db_connect()[1]
                obj_tol = db_connect()[2]

                # Main stroke
                cv2.circle(image,(int(x), int(y)), int(r), (0,0,255), 2)
                # Center point
                cv2.circle(image, (int(x), int(y)), 2, (0, 0, 255), 2)
                # Note line
                cv2.line(image, (int(x), int(y)), (int(x) + int(r), int(y)), (0, 0, 255), 2)
                # Target status | note found
                cv2.putText(image, target_name(), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (target_color()), 3)
                # Target size | cm
                cv2.putText(image, f"{obj_size}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (target_color()), 3)
                # Target tolerance | cm
                cv2.putText(image, f"{obj_tol}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (target_color()), 3)
                # Target measurement STATUS
                cv2.putText(image, f"{tolerance_measurement(data)[0]}", (10, dim[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, tolerance_measurement(data)[1], 3)

            cv2.imshow('output post processing', image)
            #cv2.imshow("thresh", thresh)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

    cv2.destroyAllWindows()

# Run without main
a = Output().frame()

