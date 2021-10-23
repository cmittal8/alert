import io, os, sys
import json
import setuptools
import google.protobuf
from google.protobuf.json_format import MessageToJson

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "secret.json"

def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.object_localization(image=image)
    response = response.localized_object_annotations
    for object in response:
        if object.name == 'Person':
            return 'Person detected'

    return 'Person not detected'
if __name__ == '__main__':
    print(detect_faces("image.jpg"))
