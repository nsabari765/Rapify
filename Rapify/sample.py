import google.generativeai as genai
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import tempfile

genai.configure(api_key="AIzaSyBOkOdR20T8yFN2s7KsLzDdeMfMrNtwW60")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🎤 Speech to Text Web App")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="🛑 Stop Recording",
    just_once=False,
    use_container_width=True
)

if audio:
    st.audio(audio['bytes'], format="audio/webm")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
        temp_webm.write(audio['bytes'])
        temp_webm_path = temp_webm.name

    temp_wav_path = temp_webm_path.replace(".webm", ".wav")
    AudioSegment.from_file(temp_webm_path, format="webm").export(temp_wav_path, format="wav")

    with open(temp_wav_path, "rb") as f:
        audio_bytes = f.read()

        response = gemini_model.generate_content(
            contents=[audio_bytes, "Transcribe the above audio to text."]
        )

    st.success("✅ Transcription:")
    st.write(response.text)