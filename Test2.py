import tkinter as tk
import requests
from bs4 import BeautifulSoup

# Task 1: GUI Development
def create_gui():
    window = tk.Tk()
    window.title("Weather Information Display Program")

    cities = ["New York", "London", "Paris", "Tokyo", "İzmir", "İstanbul", "Moscow"]  # Example city list
    city_var = tk.StringVar()
    city_dropdown = tk.OptionMenu(window, city_var, *cities)
    city_dropdown.pack()

    weather_label = tk.Label(window, text="")
    weather_label.pack()

    unit_btn = tk.Button(window, text="Toggle Unit", command=lambda: toggle_temperature_unit(weather_label))
    unit_btn.pack()

    city_var.trace("w", lambda *args: fetch_weather_data(city_var.get(), weather_label))

    load_preferences(city_var)

    window.mainloop()

# Task 2: Retrieve Weather Data
def fetch_weather_data(city, weather_label):
    try:
        api_key = "c48dbf31920d650a750d5bf0654d93b0"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        weather_data = response.json()

        city_weather = extract_city_weather(weather_data)

        weather_label.config(text=city_weather)

        store_weather_data(city, city_weather)

    except requests.exceptions.RequestException:
        weather_label.config(text="Failed to fetch weather data")

# Task 3: Store and Display Weather Information
def store_weather_data(city, weather_data):
    weather_data_dict[city] = weather_data

def display_weather_info(city_var, weather_label):
    selected_city = city_var.get()
    weather_data = weather_data_dict.get(selected_city)
    if weather_data:
        weather_label.config(text=weather_data)
    else:
        weather_label.config(text="No weather data available for the selected city")

# Task 4: Temperature Conversion
def toggle_temperature_unit(weather_label):
    current_text = weather_label.cget("text")
    converted_text = convert_temperature(current_text)
    weather_label.config(text=converted_text)

def convert_temperature(text):
    temperature = float(text.split("°")[0])
    unit = text.split("°")[1]

    if unit == "C":
        converted_temperature = (temperature * 9/5) + 32
        converted_unit = "F"
    elif unit == "F":
        converted_temperature = (temperature - 32) * 5/9
        converted_unit = "C"
    else:
        return text

    converted_text = f"{converted_temperature:.1f}°{converted_unit}"
    return converted_text

# Task 5: Save and Load User Preferences
def save_preferences(city_var):
    with open("Settings.txt", "w") as file:
        file.write(city_var.get())

def load_preferences(city_var):
    try:
        with open("Settings.txt", "r") as file:
            saved_city = file.read().strip()
            if saved_city:
                city_var.set(saved_city)
    except FileNotFoundError:
        city_var.set("")

# Extract the relevant weather information from the API response
def extract_city_weather(weather_data):
    try:
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]

        city_weather = f"Temperature: {temperature}°C\n"
        city_weather += f"Humidity: {humidity}%\n"
        city_weather += f"Description: {description}"

        return city_weather

    except KeyError:
        return ""

# Create an empty dictionary to store weather data
weather_data_dict = {}

create_gui()
