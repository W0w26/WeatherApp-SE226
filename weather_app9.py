import tkinter
import requests
import json
from tkinter import messagebox
from tkinter import Label
from tkinter import Tk
import tk as tk
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import datetime

#to store multiple cities
city_preferences = []

# defining window
root = tkinter.Tk()
root.title('Weather App')
root.geometry('1200x600')
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
    "Ankara":
        {
        "url": "https://weather.com/weather/today/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3",

        "City Name" : "Ankara",
        "Day": "Today",
        "temperature": None,
        "wind_speed": None
        },



    "İstanbul": {
        "url": "https://weather.com/weather/today/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696",
        "City Name" : "İstanbul",
        "temperature": None,
        "wind_speed": None,
    },
    "İzmir": {
        "url": "https://weather.com/weather/today/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5",
        "City Name" : "İzmir",
        "temperature": None,
        "wind_speed": None,
      },
    "Muğla": {
        "url": "https://weather.com/weather/today/l/7cb1814c2810b68458e9e07f35d21a270803a6e3b3b63892332f7c65d684d2e2",
        "City Name" : "Muğla",
        "temperature": None,
        "wind_speed": None,
       },
    "Antalya": {
        "url": "https://weather.com/weather/today/l/71e885837d402a80c47f60e0149e619268e571d7fe780903ab0472d797e0afff",
        "City Name" : "Antalya",
        "temperature": None,
        "wind_speed": None,
    },
    "Aydın": {
        "url": "https://weather.com/weather/today/l/311a74394ae5945f829ccc05285753af2c4c86a4d48121a905c0f066a314959d",
        "City Name" : "Aydın",
        "temperature": None,
        "wind_speed": None,

    }

}
def save_preferences():
    """Save the selected city preference"""
    preferences = clicked.get()
    if preferences in city_attributes:
        city_info = city_attributes[preferences]
        city_name = city_info["City Name"]

        # Retrieve temperature and wind speed from web scraping data
        get_weather()
        temperature = temp_label.cget("text").split(":")[1].strip()
        wind_speed = wind_speed_label.cget("text").split(":")[1].strip()

        data = {
            "City Name": city_name,
            "Temperature": temperature,
            "Wind Speed": wind_speed
        }
        filename = "Settings.txt"
        with open(filename, 'w') as file:
            file.write("City Name: " + city_name + "\n")
            file.write("Temperature: " + temperature + "\n")
            file.write("Wind Speed: " + wind_speed + "\n")
        messagebox.showinfo('Save Preferences', 'Preferences saved successfully!')
    else:
        messagebox.showerror('Save Preferences', 'Invalid city preference selected.')


def load_preferences():
    """Load the saved city preferences"""
    try:
        with open('Settings.txt', 'r') as file:
            city_preferences = file.readlines()

        for preference in city_preferences:
            preference_data = preference.strip().split(':')
            if preference_data[0] == "City Name":
                city_info_label.config(text=preference_data[1].strip(), font=large_font, bg=output_color)
            elif preference_data[0] == "Temperature":
                temp_label.config(text=preference_data[1].strip(), font=small_font, bg=output_color)
            elif preference_data[0] == "Wind Speed":
                wind_speed_label.config(text=preference_data[1].strip(), font=small_font, bg=output_color)

        messagebox.showinfo('Load Preferences', 'Preferences loaded successfully!')
    except FileNotFoundError:
        messagebox.showinfo('Load Preferences', 'No saved preferences found.')

def get_weather():
    """Grab information from API response and update our weather labels"""
    preference = clicked.get()
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
    temp_label.config(text="Temperature: " + temperature + " F", font=small_font, bg=output_color)
    wind_speed_label.config(text="Wind Speed: " + wind_speed, font=small_font, bg=output_color)

    # Update output labels
    city_info_label.config(text=city_name, font=large_font, bg=output_color)

    weather_label.config(text="Hava Durumu: " + description, font=small_font, bg=output_color)
    temp_label.config(text="Temperature: " + temperature + " F", font=small_font, bg=output_color)
    wind_speed_label.config(text="Wind Speed: " + wind_speed, font=small_font, bg=output_color)




def convert():
    preference = clicked.get()
    url = city_attributes[preference]["url"]
    page = requests.get(url)
    soup = bs(page.content, "html.parser")

    temperatureC = soup.find('span', class_="CurrentConditions--tempValue--MHmYY").text
    temperatureC = temperatureC.replace('°', '')  # ° işaretini kaldır

    x = float(temperatureC)
    x = ((x-32)*5)/9
    x = int(x)
    temp_label.config(text="Temperature: " + str(x) + " C", font=small_font, bg=output_color)

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
temp_min_label = tkinter.Label(output_frame, bg=output_color,
                               font=('SimSun', 15))
temp_max_label = tkinter.Label(output_frame, bg=output_color,
                               font=('SimSun', 15))
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

#city dropdown
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
load_preferences()
dropdown_menu = tkinter.OptionMenu(root,clicked,*dropdown_options)

dropdown_label = tkinter.Label(input_frame, text='Select a city', font=small_font, bg=input_color)

get_weather_button = tkinter.Button(input_frame, text="Get Today's Weather", font=large_font, bg=input_color, command=get_weather)
get_weather_button.grid(row=0, column=1, padx=10, pady=(10, 0))

button = tkinter.Button(root, text="Convert", command=convert)
button.pack()

dropdown_label.grid(row=0, column=0, padx=10, pady=(10, 0))
dropdown_menu.pack()


"""#day dropdown 
day_entry = tkinter.Entry(input_frame, width=20, font=large_font)
dropdown_options = [
 ,"Today","Tomorrow", "The day after tomorrow" 
]
clicked = tkinter.StringVar()
clicked.set("Today")

dropdown_menu = tkinter.OptionMenu(root,clicked,*dropdown_options)

get_weather_button.grid(row=0, column=1, padx=10, pady=(10, 0))

dropdown_label.grid(row=0, column=0, padx=10, pady=(10, 0))
dropdown_menu.pack()
"""



# Save and Load buttons
save_button = tkinter.Button(input_frame, text='Save Preferences', font=large_font, bg=input_color, command=save_preferences)
save_button.grid(row=1, column=0, padx=10, pady=(10, 0))
# run root window's main loop
root.mainloop()