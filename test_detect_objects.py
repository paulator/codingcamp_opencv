import cv2

min_area=1000

cap = cv2.VideoCapture(0,cv2.CAP_V4L)

while True:
    # Nehmen Sie ein Bild von der Kamera auf
    ret, frame = cap.read()

    # Konvertieren Sie das Bild in Graustufen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Führen Sie eine Schwellenwertanalyse durch, um Objekte zu isolieren
    threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

    # Finden Sie die Konturen der Objekte
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtern Sie Konturen nach Größe
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            filtered_contours.append(cnt)

    # Zeichnen Sie eine grüne Umrandung um jedes erkannte Objekt
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)

        print("Objekt gefunden bei x=%d, y=%d" % (x, y))

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Zeigen Sie das Bild mit den umrandeten Objekten an
    cv2.imshow('frame', frame)

    # Warten Sie auf eine Taste, um das Programm zu beenden
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Beenden Sie die Kamera-Verbindung und schließen Sie das Fenster
cap.release()
cv2.destroyAllWindows()