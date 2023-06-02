import deepl


def translate(text):
    try:
        data = deepl.translate(
            source_language="EN",
            target_language="JA",
            text=text,
            formality_tone="informal",
        )

    except:
        print("Error when translating you voice, pls enter manually in JP!")

        data = input("Japanese line: ")

    return data
