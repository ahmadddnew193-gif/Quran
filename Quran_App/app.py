import streamlit as st
import json
from pywebpush import webpush, WebPushException

VAPID_PUBLIC_KEY = "BMceqKk9S3NwZQDRVoHSQxMGT3xbLgm_Ve4PpJ4YOwp-i6FhqNNeta0UcWh5IEpiEdfvzmV245t8wR6wtJa7bJs"
VAPID_PRIVATE_KEY = "wMKrTYELUOSj_iH9JyEnkky0Ar2Sul34KLVxeixPhdM"
VAPID_CLAIMS = {"sub": "mailto:ahmadddnew193@gmail.com@gmail.com"}

if "subscriptions" not in st.session_state:
    st.session_state["subscriptions"] = []

st.title("📖 Quran Reminder")
st.write("Enable push notifications below:")

st.markdown(
    f"""
    <script>
    async function urlBase64ToUint8Array(base64String) {{
      const padding = '='.repeat((4 - base64String.length % 4) % 4);
      const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
      const rawData = atob(base64);
      const outputArray = new Uint8Array(rawData.length);
      for (let i = 0; i < rawData.length; ++i) {{
        outputArray[i] = rawData.charCodeAt(i);
      }}
      return outputArray;
    }}

    async function subscribe() {{
      const registration = await navigator.serviceWorker.register("service-worker.js");
      console.log("Service worker registered:", registration);

      const permission = await Notification.requestPermission();
      if (permission !== "granted") {{
        alert("Notifications blocked. Please allow them in your browser.");
        return;
      }}

      const subscription = await registration.pushManager.subscribe({{
        userVisibleOnly: true,
        applicationServerKey: await urlBase64ToUint8Array("{VAPID_PUBLIC_KEY}")
      }});

      fetch("/subscribe", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(subscription)
      }});

      alert("Notifications enabled!");
    }}
    </script>
    <button onclick="subscribe()">Enable Notifications</button>
    """,
    unsafe_allow_html=True
)

st.write("Current subscriptions:", st.session_state["subscriptions"])

if st.button("Send Reminder Now"):
    payload = json.dumps({"title": "Quran Reminder", "body": "Time to read Quran 🤲"})
    for sub in st.session_state["subscriptions"]:
        try:
            webpush(
                subscription_info=sub,
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            st.success("Notification sent!")
        except WebPushException as e:
            st.error(f"Push error: {e}")


