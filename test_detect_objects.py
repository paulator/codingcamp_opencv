import cv2
import numpy as np
import os

min_area = 500
# lower_blue = np.array([60,35,50])
# upper_blue = np.array([180,180,180])
#working lower_blue = np.array([65, 10, 45])
#working upper_blue = np.array([165, 150, 160])
lower_blue = np.array([100, 45, 45])
upper_blue = np.array([130, 255, 255])
step = 5
vis_offset = 200
cap = cv2.VideoCapture(0, cv2.CAP_V4L)


def lenke_links():
    print("lenke links")


def lenke_rechts():
    print("lenke rechts")


while True:

    # Nehmen Sie ein Bild von der Kamera auf
    ret, frame = cap.read()


    # Convert the image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a binary mask for blue regions
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply morphological operations
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtern Sie Konturen nach Größe
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            filtered_contours.append(cnt)

    # Zeichnen Sie eine grüne Umrandung um jedes erkannte Objekt
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # print("Objekt gefunden bei x=%d, y=%d" % (x, y))

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Zeigen Sie das Bild mit den umrandeten Objekten an
    cv2.imshow('frame', frame)
    cv2.imshow('hsv', hsv)
    #cv2.imshow('result', result)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # Check if the 'q' key was pressed
    if key == ord('q'):
        break

    # lower up
    elif key == ord('w'):
        lower_blue[0] = lower_blue[0] + step
        print(lower_blue)

    elif key == ord('e'):
        lower_blue[1] = lower_blue[1] + step
        print(lower_blue)

    elif key == ord('r'):
        lower_blue[2] = lower_blue[2] + step
        print(lower_blue)

    # lower down
    elif key == ord('s'):
        lower_blue[0] = lower_blue[0] - step
        print(lower_blue)

    elif key == ord('d'):
        lower_blue[1] = lower_blue[1] - step
        print(lower_blue)

    elif key == ord('f'):
        lower_blue[2] = lower_blue[2] - step
        print(lower_blue)

    # upper up
    elif key == ord('t'):
        upper_blue[0] = upper_blue[0] + step

    elif key == ord('z'):
        upper_blue[1] = upper_blue[1] + step

    elif key == ord('u'):
        upper_blue[2] = upper_blue[2] + step

    # upper down
    elif key == ord('g'):
        upper_blue[0] = upper_blue[0] - step

    elif key == ord('h'):
        upper_blue[1] = upper_blue[1] - step

    elif key == ord('j'):
        upper_blue[2] = upper_blue[2] - step

    os.system('clear')
    print("upper_blue: ")
    print(upper_blue)
    print("lower_blue: ")
    print(lower_blue)

    i = 1
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        print(f"Objekt Nummer: {i}: x: {x} y: {y} w: {w} h: {h}")
        i = i+1

    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        objekt_mitte_x = x + w / 2
        if objekt_mitte_x > 0 and objekt_mitte_x < vis_offset:
            lenke_links()
        if objekt_mitte_x > 640 - vis_offset and objekt_mitte_x < 640:
            lenke_rechts()
        # nur für das erste gefundene Objekt
        break


# Beenden Sie die Kamera-Verbindung und schließen Sie das Fenster
cap.release()
cv2.destroyAllWindows()
