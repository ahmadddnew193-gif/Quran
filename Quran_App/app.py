import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests

# Discord bot setup


st.set_page_config(page_title="Quran Reminder", page_icon="📖")
st.title("📖 Quran Reminder PWA")



DISCORD_CHANNEL_ID = str(st.text_input(""))
DISCORD_BOT_TOKEN = str(st.text_input(""))

components.html("""
<link rel="manifest" href="manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
      .then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
      }).catch(function(error) {
        console.log('Service Worker registration failed:', error);
      });
  }
</script>
""", height=0)

reminder_time = st.time_input("🕒 Set your daily Quran reminder time", value=datetime.time(8, 0))
surah = st.selectbox("📖 Choose today's Surah", [
    "Al-Fatiha", "Al-Baqarah", "Al-Imran", "An-Nisa", "Al-Ma'idah"
])

st.success(f"Reminder set for {reminder_time.strftime('%I:%M %p')} to read {surah}")




if st.button("🔔 Send Reminder Now"):
    message = f"📖 Time to read {surah}! May Allah bless your day 🌙"
    url = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        st.success("Reminder sent to Discord!")
    else:
        st.error(f"Failed to send: {response.status_code}")

