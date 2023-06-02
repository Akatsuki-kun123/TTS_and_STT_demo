# Python program to translate
# speech to text and text to speech

import sys
import speech_recognition as sr

from textToSpeech import *
from translateTest import *
from VVspeakersList import *

# Initialize the recognizer
r = sr.Recognizer()
vv = Voicevox()

# Loop infinitely for user to
# speak
while 1:
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            input()

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.1)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(MyText)

            if "okay stop" in MyText:
                sys.exit(0)

            JPText = translate(MyText)
            print(JPText)

            vv.speak(text=JPText, output_index=find_audio_input_index())

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown Value Error")

    time.sleep(0.5)
