import google.generativeai as genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import streamlit as st
import io
import styles as style

genai.configure(api_key="AIzaSyDrHGG6uIrQxnCGdfbwzIW4JD4M6u-hnhs")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def getResponseFromGemini(lyrics):
    if not lyrics.strip():
        return "Please give me some valid lyrics"
    
    prompt = f"""
        You are a rap artist. Take the following lyrics exactly as they are, in the same language, 
        and transform them into rap-style delivery by adjusting rhythm, flow, and phrasing only. 
        Do NOT change or rewrite the words or meaning. Keep the original lyrics intact, 
        just format or style them so they can be rapped with a catchy, natural rhythm.
        and Don't give like this (Snap, snap), (Faster tempo), (Fade out with a final "PaNam!") etc..
        Lyrics:
        {lyrics}
        """

    response = gemini_model.generate_content(prompt)
    text = response.text.replace('*', '').strip()

    return text

def getTextFromAudio(audio_bytes):
    recognizer = sr.Recognizer()

    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Speech Recognition error: {e}"

st.markdown(
    f"""
    <h1 style="{style.title}">
       🎤 RAPiFY 
    </h1>
    """,
    unsafe_allow_html=True
)

lyrics = st.text_input("Give me Your Own Lyrics to me:")

if st.button("Rap it Out"):
    answer = getResponseFromGemini(lyrics)

    num_lines = answer.count('\n') + 2
    dynamic_height = min(800, max(100, num_lines * 25))

    st.text_area("Output", value=answer, height=dynamic_height)

    if answer.strip() != "Please give me some lyrics":
        tts = gTTS(text=answer.strip(), lang='en')

        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        faster_audio = audio.speedup(playback_speed=1.5)
        
        faster_audio_file = io.BytesIO()
        faster_audio.export(faster_audio_file, format="mp3")
        faster_audio_file.seek(0)

        st.audio(faster_audio_file, format="audio/mp3", start_time=0)