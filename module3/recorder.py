# import wave
#
# def record(record_active, frames):
#     import pyaudio  # PyAudio'yu yalnızca fonksiyon çağrıldığında import et
#
#     audio = pyaudio.PyAudio()
#
#     # Akan veri (stream) oluştur
#     stream = audio.open(
#         format=pyaudio.paInt16,  # 16 bit
#         channels=1,  # Tek kanallı
#         rate=44100,  # Frekans
#         input=True,  # Mikrofon kaydı
#         frames_per_buffer=1024  # Kaç frame alınacağı
#     )
#
#     # Kayıt işlemi
#     while record_active.is_set():
#         data = stream.read(1024, exception_on_overflow=False)
#         frames.append(data)
#
#     # Stream'i durdur ve kapat
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#
#     # Ses dosyasını kaydet
#     sound_file = wave.open("voice_prompt.wav", "wb")
#     sound_file.setnchannels(1)
#     sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
#     sound_file.setframerate(44100)
#     sound_file.writeframes(b''.join(frames))
#     sound_file.close()

import sounddevice as sd
import wave
import os

def record(record_active, frames):
    import pyaudio

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    while record_active.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Kayıt tamamlandıktan sonra dosyayı kaydet
    output_path = os.path.join(os.getcwd(), "voice_prompt.wav")
    with wave.open(output_path, "wb") as sound_file:
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
