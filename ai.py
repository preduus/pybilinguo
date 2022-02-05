import os
import sys

import pyaudio
from gtts import gTTS
import sounddevice as sd
from playsound import playsound
import speech_recognition as sr

from lang import Lang

user_language = sys.argv[1] if len(sys.argv) > 1 else "pt-BR"
translations = Lang(user_language)

path = os.path.dirname(os.path.abspath(__file__))


def execute_ai_responses(command: str):
    responses = translations.get("responses")
    if command in responses:
        default_output_audio = f"{path}/tmp/command.mp3"
        buffer_audio = gTTS(responses.get(command), lang=user_language)
        buffer_audio.save(default_output_audio)
        playsound(default_output_audio)
        os.remove(default_output_audio)


def identify_voice_command(text: str):
    text = text.lower()
    ai = translations.get("ai")

    responses = (0, None)
    for command, say in ai.items():
        if isinstance(say, list):
            has = [c for c in say if c in text]
            if len(has) > 0:
                responses = (1, command)
        elif say in text:
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
        return speaker.recognize_google(speaker_input, language=user_language)
    except sr.UnknownValueError:
        return ""


def start_ai(text: str):
    if translations.get("sir") in text:
        execute_ai_responses("sir")
        input_converted_to_text = get_speaker_input()
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
