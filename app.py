import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Weather Dashboard",
    page_icon="🌦️",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
.title {
    text-align: center;
    font-size: 42px;
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
st.markdown('<div class="title">🌦️ Smart Weather Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time weather with smart suggestions</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
city = st.text_input("Enter City Name", placeholder="Example: Bangalore")

# 🔑 Your API key
API_KEY = "281bc8416a8bc23560a6e55a98b0f779"


# ---------------- WEATHER ICON FUNCTION ----------------
def get_weather_icon(condition):

    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️",
        "Smoke": "🌫️",
        "Haze": "🌫️",
        "Fog": "🌫️"
    }

    return icons.get(condition, "🌍")


# ---------------- SMART SUGGESTION FUNCTION ----------------
def get_suggestion(temp, condition):

    if condition == "Rain":
        return "☔ Carry an umbrella"

    elif temp > 35:
        return "🥵 Stay hydrated and avoid sun"

    elif temp < 15:
        return "🧥 Wear warm clothes"

    elif condition == "Clear":
        return "😎 Great day for outdoor activities"

    elif condition == "Clouds":
        return "☁️ Pleasant weather outside"

    else:
        return "✅ Have a great day!"


# ---------------- BUTTON ACTION ----------------
if st.button("Get Weather"):

    if city.strip() == "":
        st.warning("⚠️ Please enter a city name")

    else:

        try:

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={API_KEY}&units=metric"

            with st.spinner("Fetching weather data..."):

                # Improved request with timeout
                response = requests.get(url, timeout=10)

                data = response.json()

            # Check both status code and API response
            if response.status_code == 200 and data.get("cod") == 200:

                city_name = data["name"]
                country = data["sys"]["country"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                condition = data["weather"][0]["main"]
                description = data["weather"][0]["description"]

                icon = get_weather_icon(condition)
                suggestion = get_suggestion(temp, condition)

                st.success("✅ Weather data fetched successfully")

                # Display location
                st.subheader(f"{icon} {city_name}, {country}")
                st.write(f"**Condition:** {description.title()}")

                # Metrics layout
                col1, col2, col3 = st.columns(3)

                col1.metric("🌡️ Temperature", f"{temp} °C")
                col2.metric("💧 Humidity", f"{humidity}%")
                col3.metric("🌬️ Wind Speed", f"{wind} m/s")

                # Suggestion
                st.info(f"💡 Suggestion: {suggestion}")

                # Extra details
                with st.expander("📊 More Details"):

                    feels_like = data["main"]["feels_like"]
                    pressure = data["main"]["pressure"]

                    st.write(f"Feels Like: {feels_like} °C")
                    st.write(f"Pressure: {pressure} hPa")

            else:

                st.error(f"❌ API Error: {data.get('message', 'Unknown error')}")

        except requests.exceptions.ConnectionError:

            st.error("❌ No internet connection")

        except requests.exceptions.Timeout:

            st.error("❌ Request timed out. Try again.")

        except Exception as e:

            st.error(f"❌ Unexpected error: {str(e)}")


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and OpenWeather API")