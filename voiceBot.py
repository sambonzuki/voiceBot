import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import cryptocompare

#Weather setup
owm = OWM('c7534e6630f4656644cf59f70c19c498')
mgr = owm.weather_manager()

#Bitcoin setup
cryptocompare.cryptocompare._set_api_key_parameter('de827cbc70e6a52ef68626c74886cb062d423002576fc2100604b8c84f2e580f')

listener = sr.Recognizer()
player = pyttsx3.init()

def listen():
    # Speech to Text
    with sr.Microphone() as inputDevice:
        print("I'm listening...")
        voiceContent = listener.listen(inputDevice)
        textContent = listener.recognize_google(voiceContent)
        print(textContent)

    return textContent

def talk(text):
    # Text to Speech
    player.say(text)
    player.runAndWait()

def getWeather(location):
    observation = mgr.weather_at_place(location)
    w = observation.weather
    return w.detailed_status

def getTemp(location):
    observation = mgr.weather_at_place(location)
    w = observation.weather
    return w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

def getBitcoinPrice():
    return cryptocompare.get_price('BTC','USD', full=False)

def runVoiceBot():
    command = listen()

    # Checks for "what is a" commands
    if "what is" in command and "price" not in command:
        command = command.replace("what is a", "")
        #print(command)
        info = wikipedia.summary(command, 2)
        talk(info)

    # Checks for "who is" commands
    elif "who is" in command:
        command = command.replace("who is", "")
        #print(command)
        info = wikipedia.summary(command, 2)
        talk(info)

    # Checks for "play" commands
    elif "play" in command:
        command = command.replace("play", "")
        #print(command)
        pywhatkit.playonyt(command)

    # Check for "weather" commands
    elif "weather" in command:
        command = command.replace("what is the weather like in ", "")
        weather = getWeather(command)
        talk(weather)

    # Check for "temperature" commands
    elif "temperature" in command:
        command = command.replace("what is the temperature in ", "")
        weather = getTemp(command)
        talk(weather)

    # Check for "bitcoin" commands
    elif "Bitcoin" in command:
        command = command.replace("what is the price of ", "")
        price = getBitcoinPrice()
        price = price['BTC']['USD']
        string_price = str(price) +" Dollars"
        print(string_price)
        talk(string_price)

    # Catch
    else:
        talk("Sorry, I don't know what you mean.")

runVoiceBot()
