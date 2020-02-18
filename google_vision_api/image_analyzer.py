#!/usr/bin/python3
'''
This program reads the command line argument and makes a call to the Google
Vision API. After that, it does some analysis on the image content.
'''

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Define a dictionary
labels = {
    'label_detection' : types.Feature.LABEL_DETECTION,
    'crop_hints' : types.Feature.CROP_HINTS,
    'text_detection' : types.Feature.TEXT_DETECTION,
    'face_detection' : types.Feature.FACE_DETECTION,
    'image_properties' : types.Feature.IMAGE_PROPERTIES,
    'landmark_detection' : types.Feature.LANDMARK_DETECTION,
    'logo_detection' : types.Feature.LOGO_DETECTION,
    'object_localization': types.Feature.OBJECT_LOCALIZATION,
    'web_detection': types.Feature.WEB_DETECTION
}

def load_image(file_name):
    '''
    Loads a local images into a Google Vision Image type.
    Arguments:
        - file_name: path to image

    Returns: Google Vision Image type.
    '''
    assert isinstance(file_name, str), 'Expected str type for file_name.'

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    return image

def check_plastic(image_path):
    '''
    Calls the Google Vision label detection and checks if plastic has been
    found.
    Arguments:
        - image_path: path to image

    Returns: True if plastic is present in image, False if plastic is not
        present.
    '''
    image = load_image(image_path)

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    label_detection = types.Feature(type=types.Feature.LABEL_DETECTION, \
                max_results=10)


    request = types.AnnotateImageRequest(image=image, \
                    features=[label_detection])

    result = client.annotate_image(request)

    if not result.label_annotations:
        return False

    for label in result.label_annotations:
        if 'Plastic' in label or 'plastic' in label:
            return True

def call_Vision_API(image_path, requested_features):
    '''
    Wrapper around the Google Vision API. Enables calling it in one line
    with image path and requested features.
    Arguments:
        - image_path: path to image
        - requested_features: array of strings with features requested.

    Returns: AnnotateImageResponse
    '''
    assert isinstance(image_path, str), 'image_path should be a string.'
    assert isinstance(requested_features, list), 'requested_features should be \
            a list.'

    # load the image
    image = load_image(image_path)

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    all_features = []

    # Attach all the features caller requested
    for request in requested_features:
        if request not in labels:
            print(request, "is not a valid feature.")

        # append feature to the list of features to be requested
        feature_type = labels[request]
        feature = types.Feature(type=feature_type, max_results=10)
        all_features.append(feature)

    # create the request
    request = types.AnnotateImageRequest(image=image, \
                    features=all_features)

    # call the image annotation
    result = client.annotate_image(request)

    return result
