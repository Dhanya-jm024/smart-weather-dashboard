import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Weather Dashboard",
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
        "Mist": "🌫️"
    }

    return icons.get(condition, "🌍")

# ---------------- SUGGESTIONS ----------------
def get_suggestion(temp, condition):

    if condition == "Rain":
        return "☔ Carry an umbrella"

    elif temp > 35:
        return "🥵 Stay hydrated"

    elif temp < 15:
        return "🧥 Wear warm clothes"

    elif condition == "Clear":
        return "😎 Great day outside"

    else:
        return "✅ Have a great day!"

# ---------------- INPUT ----------------
city = st.text_input("Enter City Name", placeholder="Example: Bangalore")

# ---------------- CURRENT WEATHER ----------------
if st.button("Get Weather"):

    if city.strip() == "":
        st.warning("Enter a city name")

    else:

        try:

            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

            current_response = requests.get(current_url, timeout=10)
            forecast_response = requests.get(forecast_url, timeout=10)

            current_data = current_response.json()
            forecast_data = forecast_response.json()

            if current_data.get("cod") != 200:

                st.error(current_data.get("message"))

            else:

                # CURRENT WEATHER
                city_name = current_data["name"]
                country = current_data["sys"]["country"]
                temp = current_data["main"]["temp"]
                humidity = current_data["main"]["humidity"]
                wind = current_data["wind"]["speed"]
                condition = current_data["weather"][0]["main"]
                description = current_data["weather"][0]["description"]

                icon = get_weather_icon(condition)
                suggestion = get_suggestion(temp, condition)

                st.subheader(f"{icon} {city_name}, {country}")
                st.write(description.title())

                col1, col2, col3 = st.columns(3)

                col1.metric("Temperature", f"{temp} °C")
                col2.metric("Humidity", f"{humidity}%")
                col3.metric("Wind Speed", f"{wind} m/s")

                st.success(suggestion)

                # ---------------- FORECAST CHART ----------------

                st.subheader("5-Day Temperature Forecast")

                temps = []
                dates = []

                for item in forecast_data["list"]:

                    temps.append(item["main"]["temp"])
                    dates.append(item["dt_txt"])

                df = pd.DataFrame({
                    "Date": dates,
                    "Temperature": temps
                })

                df["Date"] = pd.to_datetime(df["Date"])

                st.line_chart(df.set_index("Date"))

                # ---------------- FORECAST TABLE ----------------

                st.subheader("Forecast Data")

                st.dataframe(df.head(10))

        except Exception as e:

            st.error(f"Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Python, and OpenWeather API")
