import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st

# Page setup
st.set_page_config(page_title="Daily Mood Check-in", page_icon="✨", layout="centered")

def send_email(mood: str, notes: str) -> bool:
    smtp_server = st.secrets["SMTP_SERVER"]
    smtp_port = int(st.secrets["SMTP_PORT"])
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_PASSWORD"]
    receiver_email = st.secrets["RECEIVER_EMAIL"]

    # Compose message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily Mood Update: {mood}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2>Daily Mood Check-in</h2>
        <p style="font-size: 18px;"><strong>Mood:</strong> {mood}</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;" />
        <p><strong>Description / Notes:</strong></p>
        <div style="background: #f8f9fa; padding: 12px; border-left: 4px solid #4a90e2; white-space: pre-wrap;">
          {notes if notes.strip() else '<em>No notes added.</em>'}
        </div>
        <p style="color: #888; font-size: 12px; margin-top: 20px;">Submitted at: {timestamp}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    # Send through SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    return True

# UI Layout
st.title("How are you feeling today?")
st.write("Pick your mood and drop any thoughts or details below.")

with st.form("mood_form", clear_on_submit=True):
    mood = st.selectbox(
        "Current Mood",
        options=[
            "😊 Great",
            "🙂 Good",
            "😐 Okay / Neutral",
            "😔 Feeling Down",
            "😫 Stressed / Anxious",
            "😴 Exhausted"
        ]
    )

    notes = st.text_area(
        "Description (Markdown supported)",
        placeholder="What made you feel this way? Write anything you want to share...",
        height=160
    )

    submitted = st.form_submit_button("Send Mood")

    if submitted:
        try:
            with st.spinner("Sending..."):
                send_email(mood, notes)
            st.success("Your mood has been sent!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")