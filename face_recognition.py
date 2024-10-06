import cv2
import os
import numpy as np
from PIL import Image
from smart_voting.settings import BASE_DIR
from pathlib import Path

class FaceRecognition:

    def __init__(self):
        self.detector = cv2.CascadeClassifier(str(Path(BASE_DIR) / 'base' / 'haarcascade_frontalface_default.xml'))
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def faceDetect(self, entry_id):
        face_id = entry_id
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Camera could not be opened.")
            return

        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        count = 0

        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to grab frame")
                continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                count += 1
                img_path = str(Path(BASE_DIR) / 'base' / 'dataset' / f'User.{face_id}.{count}.jpg')
                cv2.imwrite(img_path, gray[y:y+h, x:x+w])
                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff
            if k == 27 or count >= 100:
                break

        cam.release()
        cv2.destroyAllWindows()

    def trainface(self):
        path = str(Path(BASE_DIR) / 'base' / 'dataset')

        def get_images_and_labels(path):
            image_paths = [os.path.join(path, f) for f in os.listdir(path)]
            face_samples = []
            ids = []

            for image_path in image_paths:
                pil_img = Image.open(image_path).convert('L')
                img_numpy = np.array(pil_img, 'uint8')
                face_id = int(os.path.split(image_path)[-1].split(".")[1])
                faces = self.detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    face_samples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(face_id)

            return face_samples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = get_images_and_labels(path)
        self.recognizer.train(faces, np.array(ids))

        trainer_path = str(Path(BASE_DIR) / 'base' / 'trainer' / 'trainer.yml')
        self.recognizer.save(trainer_path)

        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def recognizeface(self):
        trainer_path = str(Path(BASE_DIR) / 'base' / 'trainer' / 'trainer.yml')
        self.recognizer.read(trainer_path)

        cascade_path = str(Path(BASE_DIR) / 'base' / 'haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)

        font = cv2.FONT_HERSHEY_SIMPLEX
        confidence = 0
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Camera could not be opened.")
            return

        min_w = 0.1 * cam.get(3)
        min_h = 0.1 * cam.get(4)
        detected_face_id = None 
        is_face_recognized = False
        
        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(min_w), int(min_h)))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                detected_face_id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                name = 'Detected' if confidence < 80 else "Unknown"
                is_face_recognized = confidence < 80

                cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

            cv2.imshow('Detect Face', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(detected_face_id)

        return detected_face_id, is_face_recognized

    def verify(self, face_id):
        trainer_path = str(Path(BASE_DIR) / 'base' / 'trainer' / 'trainer.yml')
        self.recognizer.read(trainer_path)

        cascade_path = str(Path(BASE_DIR) / 'base' / 'haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Camera could not be opened.")
            return False

        min_w = 0.1 * cam.get(3)
        min_h = 0.1 * cam.get(4)

        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(int(min_w), int(min_h)))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                detected_face_id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

                if confidence < 80:
                    cam.release()
                    cv2.destroyAllWindows()
                    return True  # Face is verified

            cv2.imshow('Verify Face', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return False  # Face not verified
