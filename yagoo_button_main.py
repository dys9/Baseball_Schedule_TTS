import os
import RPi.GPIO as gpio
import crawling_pi  # GET YAGOO_DATA
import kakao_tts  # GET MP3_DATA
import mp3_to_wav  # MP3_2_WAV
import time

time.sleep(5)
print("wait 5 seconds... GPIO_INIT...")
pin = 21
gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)


matchTime = crawling_pi.getMatch()
kakao_tts.get_mp3(matchTime, 'match.mp3')
mp3_to_wav.mp3_to_wav('match')


def play(i):
    i += 1
    print("#######Button Pushed.#########", i)

    now_time = crawling_pi.ttsTime()
    kakao_tts.get_mp3(now_time, 'time.mp3')
    mp3_to_wav.mp3_to_wav('time')
    os.system('aplay time.wav')
    os.system('aplay match.wav')

# only add the detection call once!
i = 0
gpio.add_event_detect(pin, gpio.RISING, callback=lambda x: play(i), bouncetime=3500)
#
while (True):
    time.sleep(10)
    hour = time.localtime(time.time()).tm_hour
    mmin = time.localtime(time.time()).tm_min
    sec = time.localtime(time.time()).tm_sec

    if hour == 0 and mmin == 0 and sec <= 10:
        matchTime = crawling_pi.getMatch()
        kakao_tts.get_mp3(matchTime, 'match.mp3')
        mp3_to_wav.mp3_to_wav('match')