import streamlit as st
import datetime
import requests
import time

st.set_page_config(page_title="Quran Reminder", layout="wide")
st.title("📖 Quran Reminder")

time_choice = st.text_input("Choose Time (HH:MM)", value="17:45")
channel_id = st.text_input("Discord Channel ID", value="YOUR_CHANNEL_ID")
bot_token = st.text_input("Bot Token", type="password",value="xMTY5NjEzOTY2MDU2MjY0Mw.G-1SJh.FA5kGGRMo2T-EWgQAdK1O_qBB-KJp1Lsd6QRMU")

if st.check_box("Start Reminder"):
    st.success(f"Reminder set for {time_choice}. App will check every minute.")


    while True:
        time.sleep(10)
        current_time = datetime.datetime.now().strftime("%H:%M")
        st.write(f"Current time: {current_time}")

        if current_time == time_choice:
            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            headers = {
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json"
            }
            data = {"content": " @everyone 🕋 Time to read Quran!"}

            response = requests.post(url, headers=headers, json=data)

            if response.status_code in [200, 201]:
                st.success("✅ Reminder sent to Discord!")
                time.sleep(60)
            else:
                st.error(f"❌ Failed to send message: {response.status_code}")
            

        

