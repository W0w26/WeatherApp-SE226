import tkinter, requests
from tkinter import *

# defining window
root = tkinter.Tk()
root.title('Weather App')
root.geometry('420x420')
root.resizable(0, 0)

# define fonts and colors
sky_color = '#5D8AA8'
grass_color = '#355E3B'  # will be changed with a nicer color
output_color = '#dcf0fb'
input_color = '#ecf2ae'
large_font = ('SimSun', 14)
small_font = ('SimSun', 10)


# define functions
def search():
    """Use open weather api to look up current weather conditions given a city"""
    global response

    # Get API response
    # URL and my api key
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = '2dda5e28ba97f1ee803dec6ef15851c3'

    # search by the appropriate query
    if search_method.get() == 1:
        querystring = {"q": city_entry.get(), 'appid': api_key, 'units': 'metric'}
    elif search_method.get() == 2:
        querystring = {"q": city_entry.get(), 'appid': api_key, 'units': 'imperial'}

    # Call API
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    print(response)

    # Example response output
    '''{'coord': {'lon': -71.0598, 'lat': 42.3584}, 'weather': [{'id': 502, 'main': 'Rain', 'description': 'heavy intensity rain', 'icon': '10d'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50d'}], 'base': 'stations', 'main': {'temp': 287.01, 'feels_like': 286.67, 'temp_min': 284.63, 'temp_max': 290.73, 'pressure': 1016, 'humidity': 85}, 'visibility': 9656, 'wind': {'speed': 8.75, 'deg': 300}, 'rain': {'1h': 4.89}, 'clouds': {'all': 100}, 'dt': 1684969679, 'sys': {'type': 2, 'id': 2013408, 'country': 'US', 'sunrise': 1684919715, 'sunset': 1684973231}, 'timezone': -14400, 'id': 4930956, 'name': 'Boston', 'cod': 200}
'''

    get_weather()


def get_weather():
    """Grab information from API response and update our weather labels"""
    # Gather the data to be used from the API response
    city_name = response['name']
    city_lat = str(response['coord']['lat'])
    city_lon = str(response['coord']['lon'])

    main_weather = response['weather'][0]['main']
    description = response['weather'][0]['description']

    temperature = str(response['main']['temp'])
    temperature_min = str(response['main']['temp_min'])
    temperature_max = str(response['main']['temp_max'])
    humidity = str(response['main']['humidity'])

    # Update output labels
    if search_method.get() == 1:
        city_info_label.config(text=city_name + "{" + city_lat + ", " + city_lon + ")", font=large_font,
                               bg=output_color)
        weather_label.config(text="Weather: " + main_weather + ", " + description, font=small_font, bg=output_color)
        temp_label.config(text="Temperature: " + temperature + " C", font=small_font, bg=output_color)
        temp_min_label.config(text="Min Temperature: " + temperature_min + " C", font=small_font, bg=output_color)
        temp_max_label.config(text="Max Temperature: " + temperature_max + " C", font=small_font, bg=output_color)
        humidity_label.config(text="Humidity: " + humidity, font=small_font, bg=output_color)
    elif search_method.get() == 2:
        city_info_label.config(text=city_name + "{" + city_lat + ", " + city_lon + ")", font=large_font,
                               bg=output_color)
        weather_label.config(text="Weather: " + main_weather + ", " + description, font=small_font, bg=output_color)
        temp_label.config(text="Temperature: " + temperature + " F", font=small_font, bg=output_color)
        temp_min_label.config(text="Min Temperature: " + temperature_min + " F", font=small_font, bg=output_color)
        temp_max_label.config(text="Max Temperature: " + temperature_max + " F", font=small_font, bg=output_color)
        humidity_label.config(text="Humidity: " + humidity, font=small_font, bg=output_color)


# define layout
# create frames
sky_frame = tkinter.Frame(root, bg=sky_color, height=250)
grass_frame = tkinter.Frame(root, bg=grass_color)
sky_frame.pack(fill=BOTH, expand=True)
grass_frame.pack(fill=BOTH, expand=True)

output_frame = tkinter.LabelFrame(sky_frame, bg=output_color, width=325, height=225)
input_frame = tkinter.LabelFrame(grass_frame, bg=input_color, width=325)
output_frame.pack(pady=30)
output_frame.pack_propagate(0)
input_frame.pack(pady=15)

# output frame layout
city_info_label = tkinter.Label(output_frame, bg=output_color,)
weather_label = tkinter.Label(output_frame, bg=output_color)
temp_label = tkinter.Label(output_frame, bg=output_color)
temp_min_label = tkinter.Label(output_frame, bg=output_color, text='Please enter the city name', font=('SimSun', 15))
temp_max_label = tkinter.Label(output_frame, bg=output_color, text='below in the box', font=('SimSun', 15))
humidity_label = tkinter.Label(output_frame, bg=output_color)
photo_label = tkinter.Label(output_frame, bg=output_color)

city_info_label.pack(pady=8)
weather_label.pack()
temp_label.pack()
temp_min_label.pack()
temp_max_label.pack()
humidity_label.pack()
photo_label.pack(pady=8)

# input frame layout
# create input frame buttons and entry
city_entry = tkinter.Entry(input_frame, width=20, font=large_font)
submit_button = tkinter.Button(input_frame, text='Submit', font=large_font, bg=input_color, command=search)

search_method = IntVar()
search_method.set(1)
temp_unit_1 = tkinter.Radiobutton(input_frame, text='C', variable=search_method, value=1,
                                  font=small_font, bg=input_color)
temp_unit_2 = tkinter.Radiobutton(input_frame, text='F', variable=search_method, value=2,
                                  font=small_font, bg=input_color)

city_entry.grid(row=0, column=0, padx=10, pady=(10, 0))
submit_button.grid(row=0, column=1, padx=10, pady=(10, 0))
temp_unit_1.grid(row=1, column=0, pady=2)
temp_unit_2.grid(row=1, column=1, padx=10, pady=2)

# run root window's main loop
root.mainloop()
