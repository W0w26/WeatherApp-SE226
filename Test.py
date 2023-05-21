import tkinter as tk
import requests
from bs4 import BeautifulSoup


# Task 1: GUI Development
def create_gui():
    # Create the GUI window and elements
    window = tk.Tk()
    window.title("Weather Information Display Program")

    # Dropdown list for city selection
    cities = ["City A", "City B", "City C"]  # Example cities, replace with actual city list
    city_var = tk.StringVar()
    city_dropdown = tk.OptionMenu(window, city_var, *cities)
    city_dropdown.pack()

    # Display area for weather information
    weather_label = tk.Label(window, text="")
    weather_label.pack()

    # Button for temperature unit toggle
    unit_btn = tk.Button(window, text="Toggle Unit", command=toggle_temperature_unit)
    unit_btn.pack()

    # Event handler for dropdown selection
    city_var.trace("w", lambda *args: fetch_weather_data(city_var.get(), weather_label))

    # Load user preferences
    load_preferences(city_var)

    # Run the GUI main loop
    window.mainloop()


# Task 2: Retrieve Weather Data
def fetch_weather_data(city, weather_label, c48dbf31920d650a750d5bf0654d93b0=None):
    try:
        # Send an HTTP request to a weather website
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid={c48dbf31920d650a750d5bf0654d93b0}"
        response = requests.get(url)

        # Retrieve the HTML content of the webpage
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the necessary weather data for the chosen city
        # Assuming weather information is in <div id="weather-info">
        weather_info_div = soup.find("div", id="weather-info")
        weather_data = weather_info_div.get_text()

        # Update the weather information display area
        weather_label.config(text=weather_data)

        # Store the weather data
        store_weather_data(city, weather_data)

    except requests.exceptions.RequestException:
        # Handle connection errors or failed data retrieval
        weather_label.config(text="Failed to fetch weather data")


# Task 3: Store and Display Weather Information
def store_weather_data(city, weather_data):
    # Use Python data structures to store the weather data
    # You can use a dictionary or any other suitable data structure to store the data

    # Example: Storing the weather data in a dictionary
    weather_data_dict[city] = weather_data


def display_weather_info(city_var, weather_label):
    # Update the weather information display area with the selected city's weather data
    selected_city = city_var.get()
    weather_data = weather_data_dict.get(selected_city)
    if weather_data:
        weather_label.config(text=weather_data)
    else:
        weather_label.config(text="No weather data available for the selected city")


# Task 4: Temperature Conversion
def toggle_temperature_unit():
    # Implement a function to convert temperature values between Celsius and Fahrenheit
    # You can update the displayed weather information with the converted values
    pass


# Task 5: Save and Load User Preferences
def save_preferences(city_var):
    # Save the selected city to the Settings.txt file
    with open("Settings.txt", "w") as file:
        file.write(city_var.get())


def load_preferences(city_var):
    try:
        # Check if the Settings.txt file exists
        with open("Settings.txt", "r") as file:
            # Read the saved preferences and set them as default
            saved_city = file.read().strip()
            if saved_city:
                city_var.set(saved_city)
    except FileNotFoundError:
        # If the file doesn't exist or preferences cannot be read,
        # set empty city and default temperature unit
        city_var.set("")
        # Set the default temperature unit here if needed


# Create a dictionary to store weather data
weather_data_dict = {}

# Create the GUI
create_gui()
