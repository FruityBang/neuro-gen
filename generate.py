import base64
import requests
import json
import time
import sys


API_KEY = '72F53422B9BB1C057F769850A722D2CD'
SECRET_KEY = '5364984F7DB97F18739D7DC0B2451AB3'
WIDTH = 1024
HEIGHT = 680
CENSORED = 'request have been censored by content policy'
FAIL = 'fail to generate image'


class TextToImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}'
        }

    def get_model(self):
        response = requests.get(
            self.URL + 'key/api/v1/models',
            headers=self.AUTH_HEADERS
            )
        print(response.status_code)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model_id, images=1, width=WIDTH, height=HEIGHT):
        params = {
            'type': 'GENERATE',
            'style': 'UHD',
            'numImages': images,
            'width': width,
            'height': height,
            'generateParams': {'query': f'{prompt}'}
        }
        data = {
            'model_id': (None, model_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(
            self.URL + 'key/api/v1/text2image/run',
            headers=self.AUTH_HEADERS,
            files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request_id,
                headers=self.AUTH_HEADERS)
            data = response.json()
            data['status'] = 'FAIL'
            if data['censored']:
                return CENSORED
            if data['status'] == 'FAIL':
                return FAIL
            if data['status'] == 'DONE':
                return data['images'][0]
            attempts -= 1
            time.sleep(delay)


def generate_image(prompt,
                   url='https://api-key.fusionbrain.ai/',
                   api_key=API_KEY,
                   secret_key=SECRET_KEY):

    api = TextToImageAPI(url=url, api_key=api_key, secret_key=secret_key)
    model_id = api.get_model()
    uuid = api.generate(prompt=prompt, model_id=model_id)
    image = api.check_generation(uuid)
    if (image == CENSORED) or (image == FAIL):
        return image
    byte_image = base64.b64decode(image)
    byte_image_size = float('{:.2f}'.format(sys.getsizeof(byte_image) / 1024))
    return byte_image, byte_image_size, WIDTH, HEIGHT

#byte_image, byte_image_size, width, height = (
#                generate_image('Сашка'))


#api = TextToImageAPI('https://api-key.fusionbrain.ai/',
#                     api_key=API_KEY,
#                     secret_key=SECRET_KEY)
#model_id = api.get_model()
#uuid = api.generate('heroes of might and magick 3', model_id)
#image = api.check_generation(uuid)
#f = open('image3.png', 'wb')
#f.write(byte_image)
#print(byte_image_size, WIDTH, HEIGHT)
