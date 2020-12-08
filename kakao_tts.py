import requests

def get_mp3(txt, name):
    REST_API_KEY = '################################'
    headers = {
        'Content-Type': 'application/xml',
        'Authorization': 'KakaoAK ' + REST_API_KEY,
    }

    data = '<speak> '.encode('utf-8') +str(txt).encode('utf-8')+ ' </speak>'.encode('utf-8')


    response = requests.post('https://kakaoi-newtone-openapi.kakao.com/v1/synthesize', headers=headers, data=data)

    rescode = response.status_code

    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.content
        with open(name, 'wb') as f:
            f.write(response_body)

    else:
        print("Error Code:"+str(rescode))
        
