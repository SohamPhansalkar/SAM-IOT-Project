import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 160)

wake_up_word = "jarvis"
serverUrl = "http://10.157.126.30:5000"

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def get_data(dataReq):
    try:
        response = requests.get(serverUrl + "/get_data")
        if response.status_code == 200:
            data = response.json()
            temperature = data.get("temperature", "unknown")
            humidity = data.get("humidity", "unknown")
            aqi = data.get("AQI", "unknown")
            
            if dataReq == "temperature":
                speak(f"The current temperature is {temperature} degrees Celsius.")
            elif dataReq == "humidity":
                speak(f"The current humidity is {humidity} percent.")
            elif dataReq == "AQI":
                speak(f"The current Air Quality Index is {aqi}.")
            elif dataReq == "stats":
                speak(f"Temperature {temperature}°C; Humidity {humidity}%; AQI {aqi}.")
        else:
            print("Failed to retrieve data from server.")
    except requests.RequestException as e:
        print("Error fetching data:", e)

def set_threshold(value):
    """Set threshold on server (-1 = fan always on, 100 = fan always off)"""
    try:
        response = requests.post(serverUrl + "/set_threshold", json={"threshold": value})
        if response.status_code == 200:
            print(f"Fan threshold set to {value}")
        else:
            speak("Failed to set fan threshold.")
    except requests.RequestException as e:
        print("Error sending threshold:", e)
        speak("Error communicating with the server.")

r = sr.Recognizer()
mic = sr.Microphone()

print("Listening for 'hey jarvis'...")

while True:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Say something...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        print("You said:", text)

        # --- Greetings ---
        if wake_up_word + " hello" in text:
            speak("Hello sir")

        # --- Sensor queries ---
        elif (wake_up_word + " temperature" in text) or (wake_up_word + " what is the temperature" in text):
            get_data("temperature")
        elif (wake_up_word + " humidity" in text) or (wake_up_word + " what is the humidity" in text):
            get_data("humidity")
        elif (wake_up_word + " aqi" in text) or (wake_up_word + " what is the aqi" in text):
            get_data("AQI")
        elif (wake_up_word + " stats" in text) or (wake_up_word + " what are the stats" in text):
            get_data("stats")

        # --- Fan control ---
        elif (wake_up_word + " turn fan on" in text) or (wake_up_word + " fan on" in text):
            set_threshold(-1)  # fan always ON
        elif (wake_up_word + " turn fan off" in text) or (wake_up_word + " fan off" in text):
            set_threshold(100)  # fan always OFF

        # --- Exit ---
        elif any(word in text for word in ["stop", "exit", "goodbye"]):
            speak("Goodbye sir")
            break

    except sr.UnknownValueError:
        print("Couldn't understand audio.")
    except sr.RequestError:
        print("Speech recognition service unavailable.")

print("Program terminated.")
