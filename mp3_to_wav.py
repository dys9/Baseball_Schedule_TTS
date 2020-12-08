from os import path
from pydub import AudioSegment
def mp3_to_wav(txt):
    
    src = txt+".mp3"
    dst = txt+".wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    print("make " +dst)