import os
import sys
from typing import Union

import speech_recognition as sr

from gtts import gTTS
from playsound import playsound
from googletrans import Translator

from lang import Lang

user_language = sys.argv[1] if len(sys.argv) > 1 else "pt-BR"
translations = Lang(user_language)

path = os.path.dirname(os.path.abspath(__file__))


def get_voice(text, lang=user_language):
    default_output_audio = f"{path}/tmp/command.mp3"
    buffer_audio = gTTS(text, lang=lang)
    buffer_audio.save(default_output_audio)
    playsound(default_output_audio)
    os.remove(default_output_audio)


def execute_ai_responses(command: str):
    responses = translations.get("responses")
    if command in responses:
        get_voice(responses.get(command))


def get_translations_type(text: str, trans: Union[str, list]):
    if isinstance(trans, list):
        has = [c for c in trans if c in text]
        if len(has) > 0:
            return True
    elif trans in text:
        return True


def auto_translate_command(text: str):
    props = translations.get("translate-dest")
    translator = Translator()
    translated = translator.translate(text, dest=props["lang"])
    get_voice(translated.text, props["region"])


def identify_voice_command(text: str):
    ai = translations.get("ai")

    responses = (0, None)
    for command, say in ai.items():
        if get_translations_type(text, say):
            responses = (1, command)

        if responses[0] > 0:
            break

    if responses[0] == 0:
        execute_ai_responses("understand")
    elif responses[0] == 1:
        execute_ai_responses(str(responses[1]))


def get_speaker_input():
    speaker = sr.Recognizer()
    with sr.Microphone() as source:
        speaker.adjust_for_ambient_noise(source)
        speaker_input = speaker.listen(source)

    try:
        return speaker.recognize_google(speaker_input, language=user_language).lower()
    except sr.UnknownValueError:
        return ""


def start_ai(text: str):
    if translations.get("sir") in text:
        execute_ai_responses("sir")
        input_converted_to_text = get_speaker_input()
        if get_translations_type(input_converted_to_text, translations.get("translate")):
            first_translate = True
            while True:
                execute_ai_responses("translate" if first_translate else "translate-more")
                text_to_translate = get_speaker_input()
                if translations.get("translate-nomore") in text_to_translate:
                    execute_ai_responses("translate-end")
                    break
                auto_translate_command(text_to_translate)
                first_translate = False
        else:
            identify_voice_command(input_converted_to_text)


def watch_for_speaker():
    while True:
        input_converted_to_text = get_speaker_input()

        if not translations.get("sir"):
            identify_voice_command(input_converted_to_text)
        else:
            start_ai(input_converted_to_text)


if __name__ == "__main__":
    watch_for_speaker()
