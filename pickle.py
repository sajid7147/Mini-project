import cv2
import pickle

# Load or create the parking position list
try:
    with open('ParkingPosition', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

width, height = 107, 48  # Size of each parking box

# Mouse click event handler
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

# Load background image (or first frame of your video)
img = cv2.imread('carParkImg.png')  # You can also use a video frame

cv2.namedWindow("Mark Parking Spots")
cv2.setMouseCallback("Mark Parking Spots", mouseClick)

# Display the image and draw rectangles
while True:
    img_copy = img.copy()
    for pos in posList:
        cv2.rectangle(img_copy, pos, (pos[0] + width, pos[1] + height),
                      (255, 0, 255), 2)
    cv2.imshow("Mark Parking Spots", img_copy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
