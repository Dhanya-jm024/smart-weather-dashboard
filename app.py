import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Weather Dashboard Pro",
    page_icon="🌦️",
    layout="centered"
)

# ---------------- LOAD API KEY SECURELY ----------------
API_KEY = st.secrets["281bc8416a8bc23560a6e55a98b0f779"]

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: white;
    margin-bottom: 30px;
}

.weather-card {
    background-color: rgba(255,255,255,0.2);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🌦️ Smart Weather Dashboard Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time weather, forecast, charts & smart suggestions</div>', unsafe_allow_html=True)

# ---------------- WEATHER ICON ----------------
def get_weather_icon(condition):

    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️",
        "Haze": "🌫️"
    }

    return icons.get(condition, "🌍")

# ---------------- SUGGESTION ----------------
def get_suggestion(temp, condition):

    if condition == "Rain":
        return "☔ Carry an umbrella"

    elif temp > 35:
        return "🥵 Stay hydrated"

    elif temp < 15:
        return "🧥 Wear warm clothes"

    elif condition == "Clear":
        return "😎 Great day outside"

    elif condition == "Clouds":
        return "☁️ Pleasant weather"

    else:
        return "✅ Have a great day!"

# ---------------- INPUT ----------------
city = st.text_input(
    "Enter City Name",
    placeholder="Example: Bangalore"
)

# ---------------- AUTO RUN WHEN USER TYPES ----------------
if city and len(city.strip()) > 1:

    try:

        with st.spinner("Fetching weather data..."):

            # Current weather API
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={API_KEY}&units=metric"

            # Forecast API
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city.strip()}&appid={API_KEY}&units=metric"

            current_response = requests.get(current_url, timeout=10)
            forecast_response = requests.get(forecast_url, timeout=10)

            current_data = current_response.json()
            forecast_data = forecast_response.json()

        # ---------------- CHECK VALID RESPONSE ----------------
        if current_response.status_code == 200 and current_data.get("cod") == 200:

            city_name = current_data["name"]
            country = current_data["sys"]["country"]
            temp = current_data["main"]["temp"]
            humidity = current_data["main"]["humidity"]
            wind = current_data["wind"]["speed"]
            condition = current_data["weather"][0]["main"]
            description = current_data["weather"][0]["description"]

            icon = get_weather_icon(condition)
            suggestion = get_suggestion(temp, condition)

            # ---------------- DISPLAY CURRENT WEATHER ----------------
            st.markdown("### Current Weather")

            st.subheader(f"{icon} {city_name}, {country}")
            st.write(description.title())

            col1, col2, col3 = st.columns(3)

            col1.metric("🌡️ Temperature", f"{temp} °C")
            col2.metric("💧 Humidity", f"{humidity}%")
            col3.metric("🌬️ Wind Speed", f"{wind} m/s")

            st.success(suggestion)

            # ---------------- FORECAST CHART ----------------
            if forecast_response.status_code == 200 and forecast_data.get("cod") == "200":

                st.markdown("### 5-Day Temperature Forecast")

                temps = []
                dates = []

                for item in forecast_data["list"]:
                    temps.append(item["main"]["temp"])
                    dates.append(item["dt_txt"])

                df = pd.DataFrame({
                    "Date": pd.to_datetime(dates),
                    "Temperature": temps
                })

                st.line_chart(df.set_index("Date"))

                # ---------------- FORECAST TABLE ----------------
                st.markdown("### Forecast Data")

                st.dataframe(df.head(10), use_container_width=True)

        else:

            st.error(current_data.get("message", "City not found"))

    except requests.exceptions.ConnectionError:

        st.error("No internet connection")

    except requests.exceptions.Timeout:

        st.error("Request timed out")

    except Exception as e:

        st.error(f"Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Python, and OpenWeather API")
