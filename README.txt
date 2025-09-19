How to run (backend):
1. cd backend
2. python -m venv venv
3. .\venv\Scripts\activate on Windows
4. pip install -r requirements.txt
5. uvicorn main:app --reload

How to run (frontend):
1. cd frontend
2. npm install
3. npm run dev
4. Open the vite URL (http://localhost:5173)

Notes:
- Backend uses Whisper which downloads model weights on first run and may take time.
- edge-tts is used for emotion-aware TTS. It requires network access.
