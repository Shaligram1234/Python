import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier('data\\xml\\haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('data\\xml\\haarcascade_mcs_mouth.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
mask_font_color = (255, 255, 255)
no_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
with_mask = "Thank You for wearing MASK"
no_mask = "Please wear MASK to defeat Corona"

# Read video
cap = cv2.VideoCapture(0)


while 1:
    # Get individual frame
    ret, img = cap.read()
    # Convert Image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangle on gace
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        # Detect mouth
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)

        # Face detected and mouth not detected
        # Result: Person is wearing mask
        if(len(mouth_rects) == 0):
            cv2.putText(img, with_mask,org, font, font_scale, mask_font_color, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:

                if(my > y):
                    # Face and mouth are detected.
                    # Mouth rectangle coordinates are within face coordinates.
                    # Result: Person is not wearing mask
                    cv2.putText(img, no_mask, org, font, font_scale, no_mask_font_color, thickness, cv2.LINE_AA)
                    break
                else:
                    cv2.putText(img, with_mask,org, font, font_scale, mask_font_color, thickness, cv2.LINE_AA)

    # Show frame with results
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release video
cap.release()
cv2.destroyAllWindows()