import cv2
import pickle

# Width and height matching the values used in the first code snippet
width, height = 250-50, 300-192

vs = cv2.VideoCapture('http://192.168.219.216:8080/video')
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    _, img = vs.read()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouseClick)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
