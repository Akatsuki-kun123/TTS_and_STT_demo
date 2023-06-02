import pyaudio


def find_audio_input_index():
    audio = pyaudio.PyAudio()

    device_count = audio.get_device_count()
    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        device_name = device_info["name"]

        if "CABLE Input" in device_name:
            audio.terminate()
            return i
        # print(f"Device {i}: {device_name}")

    audio.terminate()


def main():
    print(find_audio_input_index())


if __name__ == "__main__":
    main()
