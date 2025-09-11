import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ---------------------- CONFIG ----------------------
API_KEY = "48f88ab3639a27fa15dd4d8190a07cf7"
LATITUDE = 40.7128   # New York City Latitude
LONGITUDE = -74.0060 # New York City Longitude
UNITS = "metric"     # Use 'imperial' for Fahrenheit
FORECAST_URL = (
    f"https://api.openweathermap.org/data/2.5/forecast"
    f"?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={UNITS}"
)

# ---------------------- FETCH DATA ----------------------
def fetch_weather_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("✅ Weather data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching data:", e)
        return None

# ---------------------- PARSE DATA ----------------------
def parse_forecast_data(data):
    timestamps = []
    temperatures = []
    humidities = []

    for entry in data.get('list', []):
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']

        timestamps.append(dt)
        temperatures.append(temp)
        humidities.append(humidity)

    return timestamps, temperatures, humidities

# ---------------------- VISUALIZE DATA ----------------------
def plot_weather(timestamps, temperatures, humidities, location="New York City"):
    sns.set(style="whitegrid")

    fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Temperature plot
    sns.lineplot(x=timestamps, y=temperatures, ax=axs[0], color="orangered", linewidth=2)
    axs[0].set_title(f"🌡️ Temperature Forecast for {location}")
    axs[0].set_ylabel("Temperature (°C)")
    axs[0].grid(True)

    # Humidity plot
    sns.lineplot(x=timestamps, y=humidities, ax=axs[1], color="blue", linewidth=2)
    axs[1].set_title(f"💧 Humidity Forecast for {location}")
    axs[1].set_ylabel("Humidity (%)")
    axs[1].grid(True)

    # Formatting x-axis
    axs[1].set_xlabel("Date & Time")
    for ax in axs:
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()

# ---------------------- MAIN ----------------------
def main():
    data = fetch_weather_data(FORECAST_URL)
    if data:
        timestamps, temperatures, humidities = parse_forecast_data(data)
        plot_weather(timestamps, temperatures, humidities, location="New York City")

if __name__ == "__main__":
    main()
