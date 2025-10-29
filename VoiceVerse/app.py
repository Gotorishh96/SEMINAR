# VoiceVerse: Text Translator & Speech Generator
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
st.set_page_config(page_title="VoiceVerse: Translator & Speech", layout="centered")

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
    .big-title {font-size:32px; font-weight:600;}
    </style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.markdown("<h1 class='big-title'>🎙️ VoiceVerse</h1>", unsafe_allow_html=True)
st.write("**Text Translator & Speech Generator** — translate any text, listen to it, and download the MP3.")

# ------------------ Input Section ------------------
text = st.text_area("✍ Enter text here:", height=200)

# Detect input language (best-effort)
detected_lang_code = None
if text.strip():
    try:
        detected_lang_code = detect(text)
        # friendly display name if available
        detected_lang = next((k for k, v in languages.items() if v == detected_lang_code), None)
        if detected_lang:
            st.write(f"🕵️ Detected Language: **{detected_lang}**")
        else:
            st.write(f"🕵️ Detected Language Code: **{detected_lang_code}**")
    except LangDetectException:
        st.warning("Unable to detect language. Enter more text for better detection.")
    except Exception:
        # keep going without blocking app
        detected_lang_code = None

# ------------------ Language Selection ------------------
target_lang = st.selectbox("🌐 Select target language:", list(languages.keys()))
lang_code = languages[target_lang]

# ------------------ Translate helper ------------------
@st.cache_data
def translate_text(text, target_code):
    return GoogleTranslator(source='auto', target=target_code).translate(text)

# ------------------ Translate & Convert ------------------
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
                               file_name=f"voiceverse_{target_lang}.mp3",
                               mime="audio/mp3")

            # Optional: Speech for original text
            if st.checkbox("🔊 Also generate speech for the original text"):
                try:
                    use_lang = detected_lang_code if detected_lang_code else 'en'
                    orig_tts = gTTS(text=text, lang=use_lang)
                    mp3_orig = BytesIO()
                    orig_tts.write_to_fp(mp3_orig)
                    mp3_orig.seek(0)
                    st.audio(mp3_orig, format="audio/mp3")
                    st.download_button(label="📥 Download Original Speech (MP3)",
                                       data=mp3_orig,
                                       file_name="voiceverse_original.mp3",
                                       mime="audio/mp3")
                except Exception:
                    st.warning("⚠️ Could not generate speech for the original text (unsupported language).")

        except Exception as e:
            err = str(e)
            if "No internet" in err or "failed to establish a new connection" in err.lower():
                st.error("⚠️ Check your internet connection. Translation and gTTS require network access.")
            else:
                st.error(f"❌ Error: {e}")
