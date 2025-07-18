import cv2
import pickle
import cvzone

# === Load Parking Position Data ===
try:
    with open('ParkingPosition', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# === Constants ===
width, height = 107, 48  # width and height of parking spot

# === Define Mouse Click Function to Mark Spots ===
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break
    with open('ParkingPosition', 'wb') as f:
        pickle.dump(posList, f)

# === Video Capture ===
cap = cv2.VideoCapture('carPark.mp4')  # replace with your video file

cv2.namedWindow("Parking Detection")
cv2.setMouseCallback("Parking Detection", mouseClick)

# === Check Parking Space Function ===
def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (x + width, y + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=0.7,
                           thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}',
                       (50, 50), scale=2, thickness=2, offset=20, colorR=(0, 200, 0))

# === Main Loop ===
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Parking Detection", img)
    cv2.waitKey(20)

