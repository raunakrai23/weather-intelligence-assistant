
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Weather Intelligence Assistant",
    page_icon="🌦️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "token" not in st.session_state:
    st.session_state.token = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


def headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }


# ---------------- STYLING ----------------

st.markdown("""
<style>
.main {
    background-color: #f5f8fc;
}
.stButton button {
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN / REGISTER ----------------

if not st.session_state.token:

    st.title("🌦️ Weather Intelligence Assistant")
    st.caption("Your AI-powered weather information and advisory platform")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Welcome Back")

        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={
                        "email": email,
                        "password": password
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Connection error: {e}")

    with register_tab:
        st.subheader("Create Account")

        username = st.text_input("Username", key="register_username")
        reg_email = st.text_input("Email", key="register_email")
        reg_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Register"):
            try:
                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "username": username,
                        "email": reg_email,
                        "password": reg_password
                    },
                    timeout=30
                )

                if response.status_code in (200, 201):
                    st.success("Registration successful! Please log in.")
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Connection error: {e}")

    st.stop()


# ---------------- MAIN DASHBOARD ----------------

with st.sidebar:
    st.title("🌦️ Weather AI")
    st.success("Logged in")

    if st.button("New Conversation"):
        st.session_state.conversation_id = None
        st.session_state.messages = []
        st.rerun()

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.conversation_id = None
        st.session_state.messages = []
        st.rerun()

st.title("Weather Intelligence Dashboard")
st.write("Ask weather questions and receive intelligent weather advisories.")

weather_tab, chat_tab = st.tabs(
    ["🌤️ Live Weather", "💬 AI Assistant"]
)


# ---------------- LIVE WEATHER ----------------

with weather_tab:

    st.subheader("Current Weather")

    city = st.text_input("Enter city name", value="Jaipur")

    if st.button("Get Weather"):
        try:
            response = requests.get(
                f"{API_URL}/weather/{city}",
                timeout=30
            )

            if response.status_code == 200:
                st.session_state.weather_result = response.json()
            else:
                st.error(response.text)

        except requests.RequestException as e:
            st.error(f"Weather service error: {e}")

    
if "weather_result" in st.session_state:
    data = st.session_state.weather_result

    current = data["current_weather"]
    location = data["location"]
    daily = data["daily_forecast"]

    st.subheader(f"Weather in {location['name']}, {location['country']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Temperature", f"{current['temperature_2m']} °C")
    col2.metric("Feels Like", f"{current['apparent_temperature']} °C")
    col3.metric("Humidity", f"{current['relative_humidity_2m']}%")
    col4.metric("Wind Speed", f"{current['wind_speed_10m']} km/h")

    st.subheader("7-Day Forecast")

    forecast = []

    for i, date in enumerate(daily["time"]):
        forecast.append({
            "Date": date,
            "Max Temperature (°C)": daily["temperature_2m_max"][i],
            "Min Temperature (°C)": daily["temperature_2m_min"][i],
            "Rain Probability (%)": daily["precipitation_probability_max"][i],
            "Wind Speed (km/h)": daily["wind_speed_10m_max"][i]
        })

    st.dataframe(forecast, use_container_width=True)



# ---------------- AI CHAT ----------------

with chat_tab:

    st.subheader("Ask Your Weather Assistant")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about weather...")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        try:
            # Create conversation if necessary
            if st.session_state.conversation_id is None:

                conv_response = requests.post(
                    f"{API_URL}/conversations/",
                    headers=headers(),
                    json={"title": question[:60]},
                    timeout=30
                )

                if conv_response.status_code not in (200, 201):
                    st.error(conv_response.text)
                    st.stop()

                st.session_state.conversation_id = (
                    conv_response.json()["id"]
                )

            # Ask assistant
            response = requests.post(
                f"{API_URL}/assistant/ask",
                headers=headers(),
                json={
                    "conversation_id": st.session_state.conversation_id,
                    "question": question,
                    "city": "Jaipur"
                },
                timeout=120
            )

            if response.status_code == 200:
                answer = response.json()["answer"]

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                with st.chat_message("assistant"):
                    st.markdown(answer)

            else:
                st.error(response.text)

        except requests.RequestException as e:
            st.error(f"API connection error: {e}")
