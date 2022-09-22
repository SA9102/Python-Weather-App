# An application that scrapes weather data from Google search, and puts the data into a user-friendly format using PySimpleGUI
# Enter a location to retrieve its weather information

import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests

# Set theme
sg.theme('DarkTeal1')

# Set layout
layout = [
    [sg.Input(key='-INPUT-'), sg.Button('Enter', key='-ENTER-')], # Location input
    [sg.Text(key='-LOCATION-', font='_ 15')], # Location displayed
    [sg.Text(key='-DESCRIPTION-', font='_ 12')], # Short summary of weather
    [sg.Text(key='-CURRENT_TEMP-', font='_ 40')], # Temperature of location right now
    # Predicted maximum day temperatures and minimum night temperatures for today and the next seven days
    [sg.Text(key='-DAY_1-'), sg.Text(key='-DAY_2-'), sg.Text(key='-DAY_3-'), sg.Text(key='-DAY_4-'), sg.Text(key='-DAY_5-'), sg.Text(key='-DAY_6-'), sg.Text(key='-DAY_7-'), sg.Text(key='-DAY_8-')]
]

# Performs web scraping from Google search
def get_weather_data(values, layout):
    location = values['-INPUT-'].replace(' ', '+')

    url = f'https://www.google.co.uk/search?q=weather+{location}'
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    html = session.get(url).text

    soup = BeautifulSoup(html, 'lxml')

    all_weather_data = soup.find('div', class_='ULSxyf')
    location = all_weather_data.find('div', class_='wob_loc q8U8x').text # Get location
    current_temp = all_weather_data.find('span', class_='wob_t q8U8x').text # Get current temperature for specified location
    description = all_weather_data.find('span', id='wob_dc').text # Get short description of temperature for specified location
    
    days_of_week = all_weather_data.find_all('div', class_='wob_df') # Retrieve the HTML tags containing all the data for weather on the next seven days

    # From days_of_week, we want to find specific data, namely the maximum day temperatures and minimum night temperatures for today and the next seven
    # days. The tags that will hold this data will have the same class, which is why we performed the 'find_all' method on days_of_week. Now we need to
    # iterate through this list to obtain the necessary data. Each element in the list will be its own day of the week and will contain its weather info.
    for index, item in enumerate(days_of_week):
        day = item.find('div', class_='Z1VzSb').text # Look for the day of the week
        max_day_temp = item.find('div', class_='gNCp2e').find('span', class_='wob_t').text # Look for the maximum day temperature
        min_night_temp = item.find('div', class_='QrNVmd ZXCv8e').find('span', class_='wob_t').text # Look for the minimum night temperature
        window[f'-DAY_{index+1}-'].update(f'{day}:\n{max_day_temp}° | {min_night_temp}°\t') # Update the appropriate Text element to hold the retrieved data.

    window['-LOCATION-'].update(location) # Display location
    window['-DESCRIPTION-'].update(description) # Display short description on weather
    window['-CURRENT_TEMP-'].update(current_temp + '°C') # Display current temperature

window = sg.Window('Weather App', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-ENTER-':
        get_weather_data(values, layout)


window.close()










# print('NOW:', current_temp)