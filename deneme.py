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
class WeatherFetcher:
    def __init__(self):
        self.url= ""

    def set_url(self, city):
       if city == "Izmir":
           self.url = 'https://weather.com/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5'
       elif city == "Istanbul":
           self.url = 'https://weather.com/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5'
       elif city == "Ankara":
           self.url = 'https://weather.com/weather/tenday/l/f38419bdba5b880763808b472bd412cc03b64a36a7f21968ced9c4976789813c'
       else:
           self.url = ""




    def get_weather(self):

        try:
            if not self.url:
               return None, None,[]
            fetch = requests.get(self.url, timeout=10)
            fetch.raise_for_status()
            soup = BeautifulSoup(fetch.content, "html.parser")

            time = soup.find('div', class_ = 'DailyForecast--tinestamp--22Azh')
            place =soup.find('span', class_ ='LocationPageTitle--PresentationName-1AMA6')
            days = soup.find.all('h3', class_= 'DetailsSummary--daypartName--kbngc')
            day_temp = soup.find_all('span', class_='DetailsSummary--highTempValue--3PjlX')
            night_temp = soup.find_all('span', class_ = 'DetailsSummary--lowTempValue--2tesQ')
            weather_info = soup.find_all('span', class_ = 'DetailSummary--extendedData--307Ax')
            wind_info = soup.find_all('span',class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers')



            weather_data = []
            for i in range(min(3, len(days), len(day_temp), len(night_temp), len(weather_info), len(wind_info))):
                day = days[i].text
                day_temperature = day_temp[i].text
                night_temperature = night_temp[i].text
                weather = weather_info[i].text
                wind = wind_info[i].text
                weather_data.append((day, day_temperature, night_temperature, weather, wind))

            return time.text, place.text, weather_data

        except requests.exceptions.RequestException as e:
           print("An error occurred:", str(e))
           return None, None, []


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