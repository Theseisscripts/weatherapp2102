import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# Fetch weather data from the API
def get_weather(city):
    api_key = 'bc357020b8014271b44171544241211'
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"

    try:
        response = requests.get(url)
        print("Response text:", response.text)  # Debugging step: print the raw response

        # Check if the response is empty or contains invalid data
        if not response.text.strip():
            messagebox.showerror("Error", "Received empty response from the Weather API.")
            return None

        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", f"Error: {data['error']['message']}")
            return None

        # Parse the weather data
        current_weather = data['current']
        location = data['location']
        weather_info = {
            "city": location['name'],
            "temp_c": current_weather['temp_c'],
            "temp_f": current_weather['temp_f'],
            "condition": current_weather['condition']['text'],
            "wind_speed": current_weather['wind_kph'],
            "aqi": current_weather['air_quality']['us-epa-index'],
            "feels_like": current_weather['feelslike_c'],
            "chance_of_rain": current_weather['precip_mm'],
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

# Update the background image based on the weather condition
def set_background(image_name):
    try:
        img = Image.open(image_name)
        img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(img)

        background_label.config(image=bg_image)
        background_label.image = bg_image
        print(f"Background image set to {image_name}")
    except Exception as e:
        print(f"Error loading background image: {e}")

# Function to handle the weather data and update UI
def update_weather():
    city = city_entry.get()
    weather_data = get_weather(city)

    if weather_data:
        weather_info = (
            f"Weather in {weather_data['city']}\n"
            f"Temperature: {weather_data['temp_c']}°C / {weather_data['temp_f']}°F\n"
            f"Condition: {weather_data['condition']}\n"
            f"Wind Speed: {weather_data['wind_speed']} kph\n"
            f"AQI: {weather_data['aqi']}\n"
            f"Feels Like: {weather_data['feels_like']}°C\n"
            f"Chance of Rain: {weather_data['chance_of_rain']}%"
        )
        weather_label.config(text=weather_info)

        # Weather condition check (case-insensitive)
        condition = weather_data['condition'].lower()
        print("Weather condition:", condition)

        if "rain" in condition:
            background_image = 'rain.jpg'
        elif "snow" in condition:
            background_image = 'winter.jpg'
        elif "clear" in condition:
            background_image = 'sun.jpg'
        else:
            background_image = 'nature.jpeg'

        set_background(background_image)

# Function to exit the application
def exit_app():
    print("Exiting the app...")
    window.quit()

# Create main window
window = tk.Tk()
window.title("Weather App")
window.attributes("-fullscreen", True)

# Create the background label
background_label = tk.Label(window)
background_label.pack(fill="both", expand=True)

# Create main frame to center elements
main_frame = tk.Frame(window, bg="black")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Create the city entry and button inside a frame for cleaner layout
entry_frame = tk.Frame(main_frame, bg="black")
entry_frame.pack(pady=10)

city_label = tk.Label(entry_frame, text="Enter City:", font=("Arial", 16), fg="white", bg="black")
city_label.grid(row=0, column=0, padx=5, pady=5)

city_entry = tk.Entry(entry_frame, font=("Arial", 16), width=20)
city_entry.grid(row=0, column=1, padx=5, pady=5)

get_weather_button = tk.Button(entry_frame, text="Get Weather", font=("Arial", 16), command=update_weather)
get_weather_button.grid(row=0, column=2, padx=5, pady=5)

# Weather information display
weather_label = tk.Label(main_frame, text="", font=("Arial", 16), fg="white", bg="black", justify="left")
weather_label.pack(pady=20)

# Exit button
exit_button = tk.Button(main_frame, text="Exit", font=("Arial", 16), bg="red", fg="white", command=exit_app)
exit_button.pack(pady=10)

# Set the default background
set_background('nature.jpeg')

# Start the tkinter main loop
window.mainloop()
