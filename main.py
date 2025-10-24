import pyttsx3
import wikipedia
import webbrowser
import speech_recognition as sr
import datetime
import requests
import time
import random
import operator
import os
import platform
import subprocess

# Initialize pyttsx3 engine globally
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Male voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_cmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except Exception:
            print("Say that again please...")
            return "None"
        return query.lower()


def greet():
    speak("Hello sir, I am your desktop assistant. Tell me how may I help you.")


def tell_day():
    day = datetime.datetime.today().weekday() + 1
    days = {
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
        5: 'Friday', 6: 'Saturday', 7: 'Sunday'
    }
    if day in days:
        speak(f"Today is {days[day]}")


def tell_time():
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"The time is {hour} hours and {minute} minutes")


def tell_date():
    today = datetime.date.today()
    speak(f"Today is {today.strftime('%B %d, %Y')}")


def get_weather(city):
    api_key = "your_openweather_api_key"  # Add your OpenWeatherMap API key here
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        weather_data = response.json()
        if weather_data["cod"] != "404":
            main = weather_data["main"]
            temperature = main["temp"]
            description = weather_data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
        else:
            speak("City not found, please try again.")
    except Exception:
        speak("Sorry, I couldn't retrieve the weather information right now.")


def tell_joke():
    jokes = [
        "Why did the computer show up at work late? It had a hard drive!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
    ]
    speak(random.choice(jokes))


def set_reminder(reminder_time, message):
    speak(f"Reminder set for {reminder_time}. I will remind you to {message}.")
    try:
        reminder_obj = datetime.datetime.strptime(reminder_time, '%H:%M')
        now = datetime.datetime.now()
        reminder_datetime = now.replace(hour=reminder_obj.hour, minute=reminder_obj.minute, second=0, microsecond=0)
        if reminder_datetime < now:
            reminder_datetime += datetime.timedelta(days=1)
        seconds_to_wait = (reminder_datetime - now).total_seconds()
        time.sleep(seconds_to_wait)
        speak(f"Reminder: {message}")
    except Exception:
        speak("Sorry, I couldn't set the reminder. Please use the 24-hour HH:MM format.")


def calculate(expression):
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    try:
        tokens = expression.split()
        if len(tokens) == 3:
            num1, op, num2 = tokens
            num1, num2 = float(num1), float(num2)
            if op in ops:
                result = ops[op](num1, num2)
                speak(f"The result is {result}")
                return
        speak("Sorry, I could not calculate that.")
    except Exception:
        speak("Sorry, I encountered an error while calculating.")


def system_command(command):
    if platform.system() == 'Windows':
        if command == "shutdown":
            speak("Shutting down the system")
            os.system("shutdown /s /t 5")
        elif command == "restart":
            speak("Restarting the system")
            os.system("shutdown /r /t 5")
        elif command == "sleep":
            speak("Putting system to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        speak("System commands only supported on Windows currently.")


def open_app(app_name):
    try:
        if "notepad" in app_name:
            subprocess.Popen("notepad.exe")
            speak("Opening Notepad")
        elif "calculator" in app_name:
            subprocess.Popen("calc.exe")
            speak("Opening Calculator")
        else:
            speak(f"Sorry, I don't know how to open {app_name}")
    except Exception:
        speak(f"Failed to open {app_name}")


def get_news():
    api_key = "your_newsapi_key"  # Add your NewsAPI key here
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        response = requests.get(url)
        news = response.json()
        articles = news['articles'][:5]
        speak("Here are the top 5 news headlines.")
        for i, article in enumerate(articles, 1):
            speak(f"Headline {i}: {article['title']}")
    except Exception:
        speak("Sorry, I am unable to get the news right now.")


def main():
    greet()
    while True:
        query = take_cmd()
        if query == "none":
            continue

        if "open google" in query:
            webbrowser.open("https://www.google.com")

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")

        elif "open gmail" in query:
            webbrowser.open("https://mail.google.com")

        elif "which day it is" in query:
            tell_day()

        elif "tell me the time" in query:
            tell_time()

        elif "date" in query:
            tell_date()

        elif "weather in" in query:
            city = query.replace("weather in", "").strip()
            get_weather(city)

        elif "tell me a joke" in query:
            tell_joke()

        elif "search google for" in query:
            search_term = query.replace("search google for", "").strip()
            speak(f"Searching Google for {search_term}")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")

        elif "set reminder" in query:
            speak("Please tell me the time in 24-hour format, for example 18:30")
            reminder_time = take_cmd()
            if reminder_time == "none":
                continue
            speak("What should I remind you about?")
            message = take_cmd()
            if message == "none":
                continue
            set_reminder(reminder_time, message)

        elif "calculate" in query:
            expression = query.replace("calculate", "").strip()
            calculate(expression)

        elif "news" in query:
            get_news()

        elif "shutdown" in query:
            system_command("shutdown")

        elif "restart" in query:
            system_command("restart")

        elif "sleep" in query:
            system_command("sleep")

        elif "open notepad" in query:
            open_app("notepad")

        elif "open calculator" in query:
            open_app("calculator")

        elif "from wikipedia" in query:
            speak("Checking Wikipedia")
            query_wiki = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(query_wiki, sentences=4)
                speak("According to Wikipedia")
                speak(result)
            except Exception:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        elif "tell me your name" in query:
            speak("I am your desktop assistant.")

        elif "bye" in query or "exit" in query:
            speak("Bye sir. Have a great day!")
            break

        else:
            speak("I didn't understand that command, please try again.")


if __name__ == "__main__":
    main()
