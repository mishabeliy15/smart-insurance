import cv2
import numpy as np
import requests

url = "http://localhost:8001/ai/debug/landmark/"


def sendtoserver(frame):
    imencoded = cv2.imencode(".jpg", frame)[1]
    file = {'image': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    response = requests.post(url, files=file)
    return response


def main():
    while True:
        cap = cv2.VideoCapture('demo.mov')

        ret, frame = cap.read()

        while frame is not None:
            r = sendtoserver(frame)
            image = np.asarray(bytearray(r.content), dtype="uint8")
            landmark = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imshow("frame", landmark)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

            ret, frame = cap.read()
        cap.release()

    cv2.destroyAllWindows()

main()
