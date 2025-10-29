# VoiceVerse — Text Translator & Speech Generator

VoiceVerse is a Streamlit app that translates text into another language and converts the translated text into spoken audio (MP3) using Google Translate (via `deep-translator`) and `gTTS`.

## Included Files
- `app.py` — The Streamlit application.
- `requirements.txt` — Python dependencies.
- `Procfile` — For Render deployment.
- `setup.sh` — Startup script (used by Render / other hosts).
- `VoiceVerse.zip` — This packaged archive.

## Quick Local Run
1. Create and activate a virtual environment (recommended).
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open the shown local URL (usually http://localhost:8501).

## Deploy to Streamlit Cloud
1. Push this repository to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and create a new app.
3. Connect to your GitHub repo, choose the branch and `app.py`, and deploy. Streamlit Cloud will install packages from `requirements.txt` automatically.

## Deploy to Render.com
1. Create a new Web Service on Render.
2. Connect your GitHub repo and select the branch.
3. Set the build command:
   ```
   pip install -r requirements.txt
   ```
4. Set the Start Command:
   ```
   sh setup.sh
   ```
Render will provide the `PORT` environment variable automatically.

## Notes & Tips
- Both `deep-translator` and `gTTS` require outbound internet access.
- Some language codes may not be supported by `gTTS` (e.g., certain regional variants). If speech generation fails for a language, try selecting a closely related language code (e.g., `en` for English).
- If you see rate limits or occasional failures, consider adding retry logic or a different TTS provider (paid APIs) for production.
