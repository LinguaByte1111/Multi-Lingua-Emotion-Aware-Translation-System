import os
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from nrclex import NRCLex

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

app = FastAPI(title="Emotion-Aware Translator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_remove(path):
    try:
        os.remove(path)
    except Exception:
        pass


@app.post("/translate")
async def translate_text(text: str = Form(...), target_lang: str = Form("en")):
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)

        # Emotion detection
        emo = NRCLex(text)
        emotion_scores = emo.raw_emotion_scores
        top_emotion = "Neutral"

        if emotion_scores:
            total = sum(emotion_scores.values())
            if total > 0:
                sorted_scores = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
                top, top_val = sorted_scores[0]
                if top_val / total >= 0.4:  # Arbitrary threshold to avoid over-reporting
                    top_emotion = top.capitalize()


        # Sarcasm detection
        lower = text.lower()
        sarcasm = "No sarcasm detected."
        if any(
            token in lower
            for token in [
                "wah",
                "great",
                "nice",
                "oh really",
                "yeah right",
                "kya baat hai",
                "वाह",
                "बढ़िया",
            ]
        ):
            sarcasm = "This sentence may contain sarcasm or taunting."

        return {
            "original": text,
            "translated": translated,
            "emotion": top_emotion,
            "sarcasm": sarcasm,
        }
    except Exception as e:
        print("ERROR /translate:", e)
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile):
    try:
        import whisper

        model = whisper.load_model("small")
        input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")
        with open(input_path, "wb") as f:
            content = await file.read()
            if not content:
                return JSONResponse({"error": "Uploaded file is empty."}, status_code=400)
            f.write(content)

        result = model.transcribe(input_path)
        text = result.get("text", "").strip()

        safe_remove(input_path)

        if not text:
            return JSONResponse({"error": "No speech detected in audio."}, status_code=400)

        return {"transcribed_text": text}

    except Exception as e:
        print("ERROR /speech-to-text:", e)
        return JSONResponse({"error": str(e)}, status_code=500)



@app.post("/tts")
async def text_to_speech(
    text: str = Form(...), lang: str = Form("en"), emotion: str = Form("Neutral")
):
    """
    First try edge-tts (emotion-based).
    If fails, fallback to gTTS (neutral).
    """
    out_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")

    # Voice/emotion map for edge-tts
    voice_map = {
    "Joy": ("en-US-JennyNeural", "+20%"),          # brighter, faster
    "Happy": ("en-US-JennyNeural", "+15%"),        # alias for joy
    "Anger": ("en-US-GuyNeural", "+10%"),          # strong, sharp
    "Sad": ("en-US-AriaNeural", "-15%"),           # slow, softer
    "Sadness": ("en-US-AriaNeural", "-15%"),       # alias for sad
    "Neutral": ("en-US-AriaNeural", "-8%"),          # lower tone
    "Disgust": ("en-US-GuyNeural", "-5%"),         # slightly harsh
    "Surprise": ("en-US-JennyNeural", "+20%"),     # high pitch
    "Trust": ("en-US-GuyNeural", "+5%"),           # calm, steady
    "Anticipation": ("en-US-JennyNeural", "+8%"),  # curious tone
    "fear": ("en-US-JennyNeural", "-10%"),       # baseline
    }


    try:
        import edge_tts

        key = emotion.capitalize() if isinstance(emotion, str) else "Neutral"
        voice, rate = voice_map.get(key, voice_map["Neutral"])

        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(out_path)

        return FileResponse(out_path, media_type="audio/mpeg", filename="output.mp3")

    except Exception as e:
        print("edge-tts failed, falling back to gTTS:", e)

        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang=lang)
            tts.save(out_path)
            return FileResponse(
                out_path, media_type="audio/mpeg", filename="output_fallback.mp3"
            )
        except Exception as e2:
            print("ERROR /tts:", e2)
            return JSONResponse({"error": str(e2)}, status_code=500)


@app.post("/speech-to-speech")
async def speech_to_speech(file: UploadFile, target_lang: str = Form("en")):
    try:
        import whisper, edge_tts

        model = whisper.load_model("small")
        input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")
        with open(input_path, "wb") as f:
            f.write(await file.read())
        result = model.transcribe(input_path)
        text = result.get("text", "")
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        out_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")
        communicate = edge_tts.Communicate(translated, "en-US-JennyNeural")
        await communicate.save(out_path)
        safe_remove(input_path)
        return FileResponse(
            out_path, media_type="audio/mpeg", filename="translated_output.mp3"
        )
    except Exception as e:
        print("ERROR /speech-to-speech:", e)
        return JSONResponse({"error": str(e)}, status_code=500)
