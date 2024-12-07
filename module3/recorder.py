import pyaudio
import wave

def record(record_active):
    audio = pyaudio.PyAudio()

    # akan veri(stream)i tutacağım
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1, #tek kanallı
        rate=44100, #yüksek kalitede ses kayıt yapılması için belirtilen frekans
        input=True, #stream içindeki verileri kaydedeceğimizi belirtiyorum.(mikrofon kayıt)
        frames_per_buffer=1024 #kesintisiz akacak veri,bir defada kaç frame alınacağı
    )

    #kayıt işlemi
    while True:
        stream.read(1024,exception_on_overflow=False) #exception on overflow False: taşma olursa error vermesin



