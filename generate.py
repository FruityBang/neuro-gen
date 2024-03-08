import base64
import json
import requests
import sys
import time


API_KEY = '72F53422B9BB1C057F769850A722D2CD'
SECRET_KEY = '5364984F7DB97F18739D7DC0B2451AB3'
WIDTH = 1024
HEIGHT = 680
CENSORED = 'request have been censored by content policy'
FAIL = 'fail to generate image'
KANDINSKY_ERRORS_DICT = {
    400: 'Неверные параметры запроса или текстовое описание слишком длинное',
    401:  'Ошибка авторизации. Not your fault brother',
    404: 'Ресурс не найден. Not your fault dear sir',
    415: 'Формат содержимого не поддерживается сервером. Not your fault dear',
    500: 'Ошибка сервера при выполнении запроса. Not your fault at all'
}


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
        if response.status_code in KANDINSKY_ERRORS_DICT:
            return (
                f'Server status code is {response.status_code}: '
                f'{KANDINSKY_ERRORS_DICT[response.status_code]}'
                )
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
        if response.status_code in KANDINSKY_ERRORS_DICT:
            return (
                f'Server status code is {response.status_code}: '
                f'{KANDINSKY_ERRORS_DICT[response.status_code]}'
                )
        data = response.json()
        return data

    def check_generation(self, request, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request['uuid'],
                headers=self.AUTH_HEADERS)
            data = response.json()
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
    if isinstance(model_id, str):
        return model_id
    uuid = api.generate(prompt=prompt, model_id=model_id)
    if isinstance(uuid, str):
        return uuid
    image = api.check_generation(uuid)
    if (image == CENSORED) or (image == FAIL):
        return image
    byte_image = base64.b64decode(image)
    byte_image_size = float('{:.2f}'.format(sys.getsizeof(byte_image) / 1024))
    return byte_image, byte_image_size, WIDTH, HEIGHT
