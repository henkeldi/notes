import cv2

img1 = cv2.imread('imgA.jpg')
img2 = cv2.imread('imgB.jpg')
imgs = [img1, img2]
imgs_draw = [img1.copy(), img2.copy()]
pts = [[], []]

def drawPoints():
    global imgs_draw
    for i in range(len(imgs_draw)):
        imgs_draw[i] = imgs[i].copy()
        for j, pt in enumerate(pts[i]):
            cv2.circle(imgs_draw[i], pt, 3, (114, 38, 249), -1)
            cv2.putText(imgs_draw[i],
                        str(j),
                        pt,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (242, 248, 248),
                        1,
                        cv2.LINE_AA)

def printPoints():
    for j in range(len(pts)):
        print("pts{} = [".format(j+1))
        for i, pt in enumerate(pts[j]):
            terminate_char = "," if i < len(pts[j]) - 1 else "]"
            print("    ({}, {}){}".format(pt[0], pt[1], terminate_char))

def click_cb(e, x, y, flags, param):
    if e == cv2.EVENT_LBUTTONDOWN:
        pts[param].append((x, y))
        drawPoints()
        printPoints()

cv2.namedWindow('img1')
cv2.namedWindow('img2')
cv2.setMouseCallback("img1", click_cb, 0)
cv2.setMouseCallback("img2", click_cb, 1)

k = -1
while k == -1:
    cv2.imshow('img1', imgs_draw[0])
    cv2.imshow('img2', imgs_draw[1])
    k = cv2.waitKey(1)
