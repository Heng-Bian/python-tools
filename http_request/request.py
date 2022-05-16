import requests
import json
import time
import hashlib
import base64
import os

url = "https://api.deepsound.cn/tts"
appId = 'your_app_id'
appKey = 'your_app_key'
token = 'your_token'


def checksum(body_dict):
    ts = int(time.time())
    body_str = json.dumps(body_dict, ensure_ascii=False)
    print(body_str)
    str_all = appId+str(ts)+body_str
    md5Sum = hashlib.md5(str_all.encode(encoding='utf-8')).hexdigest()
    return str(ts), md5Sum,body_str


def text_content():
    text = '这是语音测试文本'
    base64_str = base64.urlsafe_b64encode(text.encode("utf-8"))
    return base64_str.decode('utf-8')


def tts():
    serverConfig = {}
    serverConfig['version'] = '1.0'
    serverConfig['service-mode'] = 'cloud'
    serverConfig['net-timeout'] = 10000

    audioConfig = {}
    audioConfig['audio-format'] = 'audio/L16; rate=44100'
    audioConfig['audio-encode'] = 'audio/mp3'
    audioConfig['output-format'] = 'json'  # json raw
    audioConfig['pitch'] = 'normal'
    audioConfig['speed'] = 'normal'
    audioConfig['quality'] = 'high_fast_v1'

    voice = {}
    voice['language'] = 'zh-CN'
    voices = ['zh-CN-female-lele', 'zh-CN-female-xiaoliang', 'zh-CN-female-xiaomiao', 'zh-CN-female-xiaoqi', 'zh-CN-male-shiye']
    voice['voice-name'] = voices[0]

    input = {}
    input['text-type'] = 'plain'
    input['text-encode'] = 'utf-8'
    input['number-read'] = 'ordinal_first'
    input['text'] = text_content()

    post_body = {
                'serverConfig': serverConfig,
                'audioConfig': audioConfig,
                'voice': voice,
                'input': input
                 }

    ts, md5str,body_str = checksum(post_body)

    headers = {'Content-Type': 'application/json; charset=utf-8',
               'X-Curtime': ts,
               'X-Appid': appId,
               'X-Appkey': appKey,
               'X-Token': token,
               'X-Checksum': md5str
               }

    response = requests.post(url=url,data=body_str,headers=headers)
    print(response.text)
    print(response.headers)

tts()
