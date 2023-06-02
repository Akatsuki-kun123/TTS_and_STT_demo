import io
import wave
import time
import deepl
import pyaudio
import requests

from VVspeakersList import *


class Voicevox:
    def __init__(self, host="127.0.0.1", port=50021):
        self.host = host
        self.port = port

    def speak(self, text=None, speaker=14, output_index=None):
        params = (("text", text), ("speaker", speaker))

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query", params=params
        )

        voicevox_query = init_q.json()
        voicevox_query["volumeScale"] = 6.0
        voicevox_query["intonationScale"] = 1.5
        voicevox_query["prePhonemeLength"] = 1.5
        voicevox_query["postPhonemeLength"] = 1.0
        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            json=voicevox_query,
        )

        audio = io.BytesIO(res.content)
        audio_data = res.content

        with wave.open(audio, "rb") as f:
            with wave.open("output.wav", "wb") as wav_file:
                wav_file.setnchannels(f.getnchannels())
                wav_file.setsampwidth(f.getsampwidth())
                wav_file.setframerate(f.getframerate())
                wav_file.writeframes(audio_data)

            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            output_stream = p.open(
                format=p.get_format_from_width(width=f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True,
                output_device_index=output_index,
                stream_callback=_callback,
            )

            output_stream.start_stream()

            while output_stream.is_active():
                time.sleep(0.1)

            output_stream.stop_stream()
            output_stream.close()
            p.terminate()


def main():
    vv = Voicevox()
    output_index = find_audio_input_index()

    while 1:
        text = input("Line: ")
        if text == "stop":
            break

        data = deepl.translate(
            source_language="EN",
            target_language="JA",
            text=text,
            formality_tone="informal",
        )
        print(f"Translate: {data}")

        vv.speak(text=data, output_index=output_index)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
