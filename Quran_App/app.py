import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests
import threading
import json

from flask import Flask, request
from pywebpush import webpush, WebPushException

# ===================
# CONFIG
# ===================

VAPID_PUBLIC_KEY = "BMceqKk9S3NwZQDRVoHSQxMGT3xbLgm_Ve4PpJ4YOwp-i6FhqNNeta0UcWh5IEpiEdfvzmV245t8wR6wtJa7bJs"
VAPID_PRIVATE_KEY = "wMKrTYELUOSj_iH9JyEnkky0Ar2Sul34KLVxeixPhdM"

# Store push subscriptions
subscriptions = []

# ===================
# FLASK BACKEND
# ===================
flask_app = Flask(__name__)

@flask_app.route("/save-subscription", methods=["POST"])
def save_subscription():
    subscription = request.json
    subscriptions.append(subscription)
    print("New subscription:", subscription)
    return {"status": "saved"}

def run_flask():
    flask_app.run(port=5001)

# Start Flask in background
threading.Thread(target=run_flask, daemon=True).start()

# ===================
# STREAMLIT APP
# ===================
st.set_page_config(page_title="Quran Reminder", page_icon="📖")
st.title("📖 Quran Reminder PWA")

components.html(f"""
<link rel="manifest" href="manifest.json">
<script>
  if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('service-worker.js').then(function(reg) {{
      console.log('Service Worker registered:', reg);

      Notification.requestPermission().then(function(result) {{
        if (result === 'granted') {{
          console.log("Notifications allowed.");

          reg.pushManager.subscribe({{
            userVisibleOnly: true,
            applicationServerKey: "{VAPID_PUBLIC_KEY}"
          }}).then(function(subscription) {{
            console.log("Subscribed:", JSON.stringify(subscription));

            fetch('http://localhost:5001/save-subscription', {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify(subscription)
            }});
          }});
        }}
      }});
    }});
  }}
</script>
""", height=0)

reminder_time = st.time_input("🕒 Set your daily Quran reminder time", value=datetime.time(8, 0))
surah = st.selectbox("📖 Choose today's Surah", [
    "Al-Fatiha", "Al-Baqarah", "Al-Imran", "An-Nisa", "Al-Ma'idah"
])

st.success(f"Reminder set for {reminder_time.strftime('%I:%M %p')} to read {surah}")

# Function to send push
def send_push_to_all(title, body, url="/"):
    payload = json.dumps({"title": title, "body": body, "url": url})
    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": "mailto:you@example.com"}
            )
        except WebPushException as ex:
            print("Web push failed:", repr(ex))

if st.button("🔔 Send Reminder Now"):
    send_push_to_all(
        title="📖 Quran Reminder",
        body=f"Time to read {surah}! May Allah bless your day 🌙",
        url="https://quran.com"
    )
    st.success("Push notification sent!")
