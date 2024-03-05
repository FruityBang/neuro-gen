import requests
import json
import time

API_KEY = '72F53422B9BB1C057F769850A722D2CD'
SECRET_KEY = '5364984F7DB97F18739D7DC0B2451AB3'


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
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model_id, images=1, width=1024, height=1024):
        params = {
            'type': 'GENERATE',
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
            if data['status'] == 'DONE':
                return data['images'][0]
            attempts -= 1
            time.sleep(delay)


api = TextToImageAPI('https://api-key.fusionbrain.ai/',
                     api_key=API_KEY,
                     secret_key=SECRET_KEY)
model_id = api.get_model()
uuid = api.generate('near blackhole', model_id)
image = api.check_generation(uuid)
file = open('image.jpeg', 'w')
file.write(image)
