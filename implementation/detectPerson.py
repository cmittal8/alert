import io, os, sys
import json
import setuptools
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Chiranshi/OneDrive - Georgia Institute of Technology/Gatech/PersonalGit/vaulted-night-329901-629349427f85.json"

def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    # likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
    #                    'LIKELY', 'VERY_LIKELY')
    # print('Faces:')
    count = 0
    for face in faces:
        count = count + 1
        # print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        # print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        # print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in face.bounding_poly.vertices])

        # print('face bounds: {}'.format(','.join(vertices)))
    if (count == 1):
        print("True")
    else:
        print(count)
        print("False")
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
if __name__ == '__main__':
    detect_faces("C:/Users/Chiranshi/Downloads/Kroger Recipt.jpg")
