# # TEXT TO SPEECH TRANSLATOR 
# import streamlit as st
# from gtts import gTTS
# from io import BytesIO
# from deep_translator import GoogleTranslator

# # ------------------ Supported Languages ------------------
# languages = {
#     "English": "en",
#     "Hindi": "hi",
#     "French": "fr",
#     "Spanish": "es",
#     "German": "de",
#     "Odia": "or",        # Odia
#     "Chinese": "zh-CN",  # Simplified Chinese
#     "Japanese": "ja",
#     "Korean": "ko"
# }

# # ------------------ Streamlit UI ------------------
# st.set_page_config(page_title="Text to Speech Translator", layout="centered")
# st.title("🌍 Text Translator & Speech Generator")

# st.write("Translate text to another language, hear it, and download the speech as MP3.")

# # Input text
# text = st.text_area("✍ Enter text here (in any language):", height=200)

# # Language selection
# target_lang = st.selectbox("🌐 Select target language for translation & speech:", list(languages.keys()))
# lang_code = languages[target_lang]

# # Convert & Translate
# if st.button("🌟 Translate & Convert to Speech"):
#     if not text.strip():
#         st.warning("Please enter some text.")
#     else:
#         try:
#             # Translate text using deep-translator
#             translated_text = GoogleTranslator(source='auto', target=lang_code).translate(text)

#             st.info(f"🔁 Translated Text ({target_lang}):")
#             st.write(translated_text)

#             # Convert to speech
#             tts = gTTS(text=translated_text, lang=lang_code)
#             mp3_fp = BytesIO()
#             tts.write_to_fp(mp3_fp)
#             mp3_fp.seek(0)

#             st.success("✅ Speech generated successfully!")

#             # Audio player
#             st.audio(mp3_fp, format="audio/mp3")

#             # Download button
#             st.download_button(label="📥 Download MP3",
#                                data=mp3_fp,
#                                file_name="translated_speech.mp3",
#                                mime="audio/mp3")
#         except Exception as e:
#             st.error(f"❌ Error: {e}")


# TEXT TO SPEECH TRANSLATOR (Enhanced Version)
import streamlit as st
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# ------------------ Supported Languages ------------------
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Odia": "or",        # Odia
    "Chinese": "zh-CN",  # Simplified Chinese
    "Japanese": "ja",
    "Korean": "ko"
}

# ------------------ Streamlit Page Config ------------------
st.set_page_config(page_title="Text to Speech Translator 🌍", layout="centered")

# ------------------ Custom Styling ------------------
st.markdown("""
    <style>
    body {background-color: #F9FBFD;}
    .stTextArea textarea {font-size: 18px;}
    .stButton>button {
        background-color: #4CAF50; color: white; font-size: 18px;
        border-radius: 8px; padding: 0.5em 1em;
    }
    .stSelectbox {font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.title("🌎 Text Translator & Speech Generator")
st.write("Translate any text into another language, listen to it, and download the spoken version as MP3!")

# ------------------ Input Section ------------------
text = st.text_area("✍ Enter text here:", height=200)

# Detect input language
if text.strip():
    try:
        detected_lang_code = detect(text)
        detected_lang = [k for k, v in languages.items() if v == detected_lang_code]
        if detected_lang:
            st.write(f"🕵️ Detected Language: **{detected_lang[0]}**")
        else:
            st.write(f"🕵️ Detected Language Code: **{detected_lang_code}**")
    except LangDetectException:
        st.warning("Unable to detect language. Please enter more text.")

# ------------------ Language Selection ------------------
target_lang = st.selectbox("🌐 Select target language:", list(languages.keys()))
lang_code = languages[target_lang]

# ------------------ Translate & Convert ------------------
@st.cache_data
def translate_text(text, target_code):
    return GoogleTranslator(source='auto', target=target_code).translate(text)

if st.button("🌟 Translate & Convert to Speech"):
    if not text.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        try:
            # Translate
            translated_text = translate_text(text, lang_code)
            st.info(f"🔁 Translated Text ({target_lang}):")
            st.write(translated_text)

            # Convert to speech (translated)
            tts = gTTS(text=translated_text, lang=lang_code)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            st.success("✅ Speech generated successfully!")
            st.audio(mp3_fp, format="audio/mp3")

            # Download button
            st.download_button(label="📥 Download Translated Speech (MP3)",
                               data=mp3_fp,
                               file_name=f"speech_{target_lang}.mp3",
                               mime="audio/mp3")

            # Optional: Speech for original text
            if st.checkbox("🔊 Also generate speech for the original text"):
                try:
                    orig_tts = gTTS(text=text, lang=detected_lang_code)
                    mp3_orig = BytesIO()
                    orig_tts.write_to_fp(mp3_orig)
                    mp3_orig.seek(0)
                    st.audio(mp3_orig, format="audio/mp3")
                    st.download_button(label="📥 Download Original Speech (MP3)",
                                       data=mp3_orig,
                                       file_name="original_speech.mp3",
                                       mime="audio/mp3")
                except Exception:
                    st.warning("⚠️ Could not generate speech for the original text (unsupported language).")

        except Exception as e:
            if "No internet" in str(e):
                st.error("⚠️ Check your internet connection.")
            else:
                st.error(f"❌ Error: {e}")
