import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests
import json

BACKEND_URL = "http://localhost:5000"  # Replace with deployed backend URL if online

st.set_page_config(page_title="Quran Reminder", page_icon="📖")
st.title("📖 Quran Reminder PWA")

# Inject manifest + service worker
components.html("""
<link rel="manifest" href="manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
      .then(function(registration) { console.log('Service Worker registered:', registration.scope); })
      .catch(function(err){ console.log('SW registration failed:', err); });
  }
</script>
""", height=0)

# Time picker & Surah selection
reminder_time = st.time_input("🕒 Set your daily Quran reminder time", value=datetime.time(8, 0))
surah = st.selectbox("📖 Choose today's Surah", ["Al-Fatiha", "Al-Baqarah", "Al-Imran", "An-Nisa", "Al-Ma'idah"])

st.success(f"Reminder set for {reminder_time.strftime('%I:%M %p')} to read {surah}")

# Enable notifications
st.markdown(f"""
<button onclick="
navigator.serviceWorker.ready.then(async function(reg) {{
    const sub = await reg.pushManager.subscribe({{
        userVisibleOnly: true,
        applicationServerKey: '{'YOUR_PUBLIC_KEY'}'
    }});
    fetch('{BACKEND_URL}/subscribe', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(sub)
    }});
    alert('Notifications enabled!');
}});
">Enable Notifications</button>
""", unsafe_allow_html=True)

# Send reminder now
if st.button("🔔 Send Reminder Now"):
    data = {"title": "📖 Quran Reminder", "body": f"Time to read {surah}!"}
    res = requests.post(f"{BACKEND_URL}/send", json=data)
    if res.ok:
        st.success("Reminder sent!")
    else:
        st.error("Failed to send reminder.")
