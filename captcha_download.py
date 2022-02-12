import os
import random
import time

import requests
import shutil

CAPTCHA_URL = 'https://www.ub.tum.de/image_captcha?sid='

start_id = int(input('Get captchas from startid: '))


def save_captcha(sid):
    file_name = str(sid) + ".jpeg"
    path = os.sep.join(["captchas", file_name])
    res = requests.get(CAPTCHA_URL + str(sid), stream=True)

    if res.status_code == 200:
        with open(path, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('captcha saved to: ', path)
    else:
        print('could not retrieve captcha')


for i in range(start_id, start_id + 200):
    save_captcha(i)
    time.sleep(random.randrange(1, 6))
