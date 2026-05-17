import requests
import speech_recognition as sr
import os
from datetime import datetime

recognizer = sr.Recognizer()

def speak(text):
    print("Jarvis:", text)
    os.system(f'say "{text}"')

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

def ask_jarvis(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": f"You are Jarvis, a helpful AI assistant. {prompt}",
            "stream": False
        }
    )
    return response.json()["response"]

def handle_command(command):
    command = command.lower()

    if "time" in command:
        return f"The time is {datetime.now().strftime('%H:%M:%S')}"

    if command == "exit":
        return "exit"

    return ask_jarvis(command)

print("🤖 Offline Jarvis Activated (VOICE ENABLED)")

while True:
    try:
        user_input = listen()
        result = handle_command(user_input)

        if result == "exit":
            speak("Shutting down")
            break

        speak(result)

    except Exception as e:
        print("Error:", e)
