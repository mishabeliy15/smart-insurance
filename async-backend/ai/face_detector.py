import cv2
import numpy as np

from settings import MODELS_DIR


def get_face_detector(model_file=None, config_file=None, quantization=False):
    """
    Get the face detection caffe model of OpenCV's DNN module

    Parameters
    ----------
    model_file : string, optional
        Path to model file. The default is "models/res10_300x300_ssd_iter_140000.caffemodel" or models/opencv_face_detector_uint8.pb" based on quantization.
    config_file : string, optional
        Path to config file. The default is "models/deploy.prototxt" or "models/opencv_face_detector.pbtxt" based on quantization.
    quantization: bool, optional
        Determines whether to use quantized tf model or unquantized caffe model. The default is False.

    Returns
    -------
    model : dnn_Net

    """
    if quantization:
        if model_file is None:
            model_file = f"{MODELS_DIR}/opencv_face_detector_uint8.pb"
        if config_file is None:
            config_file = f"{MODELS_DIR}/opencv_face_detector.pbtxt"
        model = cv2.dnn.readNetFromTensorflow(model_file, config_file)
    else:
        if model_file is None:
            model_file = f"{MODELS_DIR}/res10_300x300_ssd_iter_140000.caffemodel"
        if config_file is None:
            config_file = f"{MODELS_DIR}/deploy.prototxt"
        model = cv2.dnn.readNetFromCaffe(config_file, model_file)
    return model


def find_faces(img, model):
    """
    Find the faces in an image

    Parameters
    ----------
    img : np.uint8
        Image to find faces from
    model : dnn_Net
        Face detection model

    Returns
    -------
    faces : list
        List of coordinates of the faces detected in the image

    """
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
    )
    model.setInput(blob)
    res = model.forward()
    faces = []
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])
    return faces


def draw_faces(img, faces):
    """
    Draw faces on image

    Parameters
    ----------
    img : np.uint8
        Image to draw faces on
    faces : List of face coordinates
        Coordinates of faces to draw

    Returns
    -------
    None.

    """
    for x, y, x1, y1 in faces:
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 3)
