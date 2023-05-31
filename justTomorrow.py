import tkinter
import requests
from tkinter import messagebox
from tkinter import Label
from tkinter import Tk
from bs4 import BeautifulSoup as bs

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
        "url": "https://weather.com/tr-TR/weather/tenday/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3",
        "City Name": "Ankara",
        "days": 4,
        "weather_data": []
    },
    "İstanbul": {
        "url": "https://weather.com/tr-TR/weather/tenday/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696",
        "City Name": "İstanbul",
        "days": 3,
        "weather_data": []
    },
    "İzmir": {
        "url": "https://weather.com/tr-TR/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5",
        "City Name": "İzmir",
        "days": 3,
        "weather_data": []
    },
    "Muğla": {
        "url": "https://weather.com/tr-TR/weather/tenday/l/7cb1814c2810b68458e9e07f35d21a270803a6e3b3b63892332f7c65d684d2e2",
        "City Name": "Muğla",
        "days": 3,
        "weather_data": []
    },
    "Antalya": {
        "url": "https://weather.com/tr-TR/weather/tenday/l/71e885837d402a80c47f60e0149e619268e571d7fe780903ab0472d797e0afff",
        "City Name": "Antalya",
        "days": 3,
        "weather_data": []
    },
    "Aydın": {
        "url": "https://weather.com/tr-TR/weather/tenday/l/311a74394ae5945f829ccc05285753af2c4c86a4d48121a905c0f066a314959d",
        "City Name": "Aydın",
        "days": 3,
        "weather_data": []
    }
}


def get_weather():
    """Grab information from API response and update our weather labels"""
    preference = clicked.get()
    try:
        url = city_attributes[preference]["url"]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "html.parser")

        city = preference
        weather_data = city_attributes[preference]["weather_data"]
        if len(weather_data) == 0:
            divs = soup.find_all('details', {'class': 'DaypartDetails--DayPartDetail--2XOOV Disclosure--themeList--1Dz21'})
            for i, div in enumerate(divs):
                if i >= city_attributes[preference]["days"]:
                    break

                daily_json = {}

                celcius = str(div.find('span', {'class': 'DetailsSummary--highTempValue--3PjlX'}).text).replace('°', '')
                if celcius == '--':
                    continue
                daily_json[celcius] = celcius
                daily_json['fahrenheit'] = (int(celcius) * 9 / 5) + 32
                daily_json['day'] = div.find('h3', {'class': 'DetailsSummary--daypartName--kbngc'}).text
                daily_json['details'] = div.find('span', {'class': 'DetailsSummary--extendedData--307Ax'}).text
                daily_json['windspeed'] = div.find('span', {'class': 'Wind--windWrapper--3Ly7c undefined'}).text

                weather_data.append(daily_json)

        # Get the weather data for the first day
        first_day = weather_data[0]
        description = first_day['details']
        temperature = list(first_day.keys())[0]
        wind_speed = first_day['windspeed']

        # Update output labels
        city_info_label.config(text=preference, font=large_font, bg=output_color)
        weather_label.config(text="Weather: " + description, font=small_font, bg=output_color)
        temp_label.config(text="Temperature: " + temperature + " C", font=small_font, bg=output_color)
        wind_speed_label.config(text="Wind Speed: " + wind_speed, font=small_font, bg=output_color)

        # Save weather data to a text file
        filename = "Settings.txt"
        with open(filename, 'w') as file:
            file.write("City Name: " + preference + "\n")
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
wind_speed_label = tkinter.Label(output_frame, bg=output_color)
city_info_label.pack(pady=8)
weather_label.pack()
temp_label.pack()
wind_speed_label.pack()

# input frame layout
# create input frame buttons and entry
city_label = Label(input_frame, text="Select a City:", bg=input_color, font=large_font)
city_label.pack(pady=10)

clicked = tkinter.StringVar()
clicked.set("Ankara")  # Set Ankara as the default city

drop = tkinter.OptionMenu(input_frame, clicked, *city_attributes.keys())
drop.pack(pady=8)

submit_button = tkinter.Button(input_frame, text="Submit", font=large_font, bg=input_color, command=get_weather)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
