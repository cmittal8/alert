import io, os, sys
import json
import setuptools

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "secret.json"

from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

def detect_faces(path):
    """Detects faces in an image."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    try:
        response = client.object_localization(image=image)
        response = response.localized_object_annotations
        # print("made call to google vision")
        # print(response)
        for obj in response:
            if obj.name == 'Person':
                return 'Person detected'

        return 'Person not detected'
    except:
        return ''
# if __name__ == '__main__':
#     print(detect_faces("image.jpg"))
