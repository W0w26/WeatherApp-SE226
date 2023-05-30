import tkinter
import requests
import json
from tkinter import messagebox
from tkinter import Label
from tkinter import Tk
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import datetime

# to store multiple cities
city_preferences = []

# defining window
root = tkinter.Tk()
root.title('Weather App')
root.geometry('500x500')
root.resizable(0, 0)

# define fonts and colors
sky_color = '#5D8AA8'
grass_color = '#355E3B'
output_color = '#dcf0fb'
input_color = '#ecf2ae'
large_font = ('SimSun', 14)
small_font = ('SimSun', 12)

# City attributes dictionary
city_attributes = {
    "Ankara": {
        "url": "https://weather.com/tr-TR/weather/today/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3",
        "City Name": "Ankara",
        "Day": "Today",
        "temperature": None,
        "wind_speed": None
    },
    "İstanbul": {
        "url": "https://weather.com/tr-TR/weather/today/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696",
        "City Name": "İstanbul",
        "temperature": None,
        "wind_speed": None,
    },
    "İzmir": {
        "url": "https://weather.com/tr-TR/weather/today/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5",
        "City Name": "İzmir",
        "temperature": None,
        "wind_speed": None,
    },
    "Muğla": {
        "url": "https://weather.com/tr-TR/weather/today/l/7cb1814c2810b68458e9e07f35d21a270803a6e3b3b63892332f7c65d684d2e2",
        "City Name": "Muğla",
        "temperature": None,
        "wind_speed": None,
    },
    "Antalya": {
        "url": "https://weather.com/tr-TR/weather/today/l/71e885837d402a80c47f60e0149e619268e571d7fe780903ab0472d797e0afff",
        "City Name": "Antalya",
        "temperature": None,
        "wind_speed": None,
    },
    "Aydın": {
        "url": "https://weather.com/tr-TR/weather/today/l/311a74394ae5945f829ccc05285753af2c4c86a4d48121a905c0f066a314959d",
        "City Name": "Aydın",
        "temperature": None,
        "wind_speed": None,
    }
}


def get_weather():
    """Grab information from API response and update our weather labels"""
    preference = clicked.get()
    try:
        url = city_attributes[preference]["url"]
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        city_name = soup.find('h1', class_="CurrentConditions--location--1YWj_").text
        description = soup.find('div', class_="CurrentConditions--phraseValue--mZC_p").text
        temperature = soup.find('span', class_="CurrentConditions--tempValue--MHmYY").text
        wind_speed = soup.find('span', class_="Wind--windWrapper--3Ly7c undefined").text

        # Update output labels
        city_info_label.config(text=city_name, font=large_font, bg=output_color)
        weather_label.config(text="Hava Durumu: " + description, font=small_font, bg=output_color)
        temp_label.config(text="Temperature: " + temperature + " C", font=small_font, bg=output_color)
        wind_speed_label.config(text="Wind Speed: " + wind_speed, font=small_font, bg=output_color)

        # Save weather data to a text file
        data = {
            "City Name": city_name,
            "Temperature": temperature,
            "Wind Speed": wind_speed
        }
        filename = "Settings.txt"
        with open(filename, 'w') as file:
            file.write("City Name: " + city_name + "\n")
            file.write("Description: " + description + "\n")
            file.write("Temperature: " + temperature + " C\n")
            file.write("Wind Speed: " + wind_speed + "\n")
    except KeyError:
        messagebox.showerror("Error", "Invalid city selection!")
# define layout
# create frames
sky_frame = tkinter.Frame(root, bg=sky_color, height=250)
grass_frame = tkinter.Frame(root, bg=grass_color)
sky_frame.pack(fill=tkinter.BOTH, expand=True)
grass_frame.pack(fill=tkinter.BOTH, expand=True)

output_frame = tkinter.LabelFrame(sky_frame, bg=output_color, width=400, height=225)
input_frame = tkinter.LabelFrame(grass_frame, bg=input_color, width=325)
output_frame.pack(pady=30)
output_frame.pack_propagate(0)
input_frame.pack(pady=15)

# output frame layout
city_info_label = tkinter.Label(output_frame, bg=output_color)
weather_label = tkinter.Label(output_frame, bg=output_color)
temp_label = tkinter.Label(output_frame, bg=output_color)
temp_min_label = tkinter.Label(output_frame, bg=output_color, font=('SimSun', 15))
temp_max_label = tkinter.Label(output_frame, bg=output_color, font=('SimSun', 15))
humidity_label = tkinter.Label(output_frame, bg=output_color)
photo_label = tkinter.Label(output_frame, bg=output_color)

city_info_label.pack(pady=8)
weather_label.pack()
temp_label.pack()
temp_min_label.pack()
temp_max_label.pack()
humidity_label.pack()
photo_label.pack(pady=8)

# wind speed training
wind_speed_label = tkinter.Label(output_frame, bg=output_color)
wind_speed_label.pack()

# input frame layout
# create input frame buttons and entry
city_entry = tkinter.Entry(input_frame, width=20, font=large_font)

# city dropdown
dropdown_options = [
    "Ankara",
    "İstanbul",
    "İzmir",
    "Muğla",
    "Antalya",
    "Aydın",
    "Isparta"
]
clicked = tkinter.StringVar()
clicked.set("Ankara")
dropdown_menu = tkinter.OptionMenu(root, clicked, *dropdown_options)

dropdown_label = tkinter.Label(input_frame, text='Select a city', font=small_font, bg=input_color)

get_weather_button = tkinter.Button(input_frame, text="Get Weather Information", font=large_font, bg=input_color,
                                    command=get_weather)
get_weather_button.grid(row=0, column=1, padx=10, pady=(10, 0))

dropdown_label.grid(row=0, column=0, padx=10, pady=(10, 0))
dropdown_menu.pack()

root.geometry('1200x600')  # pencere büyütüldü

# run root window's main loop
root.mainloop()