import cv2
from edgetpu.detection.engine import DetectionEngine
from PIL import Image

cap = cv2.VideoCapture(0)
model = 'mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'
engine = DetectionEngine(model)

while True:
    ret, frame = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        im_pil = Image.fromarray(img)
        results = engine.DetectWithImage(im_pil)
        for result in results:
            b = result.bounding_box
            x0, y0 = b[0]
            x1, y1 = b[1]
            x0 = int(x0 * w)
            y0 = int(y0 * h)
            x1 = int(x1 * w)
            y1 = int(y1 * h)
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.imshow('', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break
