
import requests
import speech_recognition as sr
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
JARVIS_NAME = os.getenv("JARVIS_NAME", "Jarvis")

recognizer = sr.Recognizer()

def speak(text):
    print(f"{JARVIS_NAME}:", text)
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
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": f"You are {JARVIS_NAME}, a helpful AI assistant. {prompt}",
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

print(f"🤖 {JARVIS_NAME} Activated (VOICE ENABLED)")

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
