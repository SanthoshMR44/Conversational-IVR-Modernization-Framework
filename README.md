Got it 👍 — here’s a **GitHub-ready `README.md`** written *specifically for your uploaded files*
(`ivr_web_conversational.html` and `ivr_sim_backend.py`), with exact feature references and working setup steps.

---

````markdown
# 🎙️ Conversational IVR Web Simulator

This project simulates a **real-time Interactive Voice Response (IVR)** system that can understand both **keypad inputs (DTMF)** and **spoken commands**.  
It uses a **FastAPI backend** (`ivr_sim_backend.py`) and a **speech-enabled web interface** (`ivr_web_conversational.html`) to provide a complete conversational IVR demo.

---

## 🚀 Overview

- **Frontend:** `ivr_web_conversational.html`
  - Modern dark-themed IVR simulator UI
  - Built-in speech recognition and text-to-speech
  - Keypad for DTMF input and microphone for natural conversation

- **Backend:** `ivr_sim_backend.py`
  - FastAPI-based IVR logic handler
  - Supports text conversation (`/ivr/conversation`)
  - DTMF keypad handler (`/ivr/dtmf`)
  - Call session management (`/ivr/start`, `/ivr/end`)
  - Optional GPT-based fallback via OpenAI API

---

## 🧩 Project Files

| File | Description |
|------|--------------|
| **ivr_web_conversational.html** | Frontend web interface for interacting with the IVR |
| **ivr_sim_backend.py** | FastAPI backend handling logic, intents, and voice simulation |

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

Make sure you have Python 3.8+ installed. Then run:

```bash
pip install fastapi uvicorn python-dotenv
````

(Optional – only if you want GPT fallback responses)

```bash
pip install openai
```

### 2️⃣ Run the Backend Server

```bash
uvicorn ivr_sim_backend:app --reload --port 8000
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

### 3️⃣ Open the Frontend

* Open `ivr_web_conversational.html` in your browser (Chrome or Edge recommended).
* It automatically connects to `http://localhost:8000`.

---

## 🎮 How to Use

1. Click **Start Call** → Backend creates a call session.
2. The IVR greets you (spoken + text).
3. Choose how to interact:

   * **Speak naturally** — Click 🎙️ **Listen** and say things like:

     * “Book a ticket”
     * “My PNR number is 123456”
     * “I want a refund”
   * **Press Keypad** — Use number buttons:

     * 1 → Booking
     * 2 → Train Status
     * 3 → Refund
     * 9 → Agent
     * 0 → Return to main menu
4. The IVR responds with text and speech.
5. Click **End Call** to close the session.

---

## 🧠 Intent Mapping (Backend Logic)

| Intent         | Trigger Words                | Response                                           |
| -------------- | ---------------------------- | -------------------------------------------------- |
| `booking`      | book, ticket, reserve        | “Do you want Sleeper or AC class?”                 |
| `train_status` | status, pnr                  | “Please tell me your 6-digit PNR.”                 |
| `refund`       | refund, cancel, tatkal       | “Is this for a cancelled train or tatkal booking?” |
| `agent`        | agent, human, representative | “Transferring you to an agent.”                    |
| `main`         | back, main, menu             | Returns to main menu                               |
| `pnr_lookup`   | 6-digit number               | Returns a mock train status                        |
| `ai_fallback`  | others (if OpenAI key set)   | GPT-generated reply                                |

---

## 🔐 Optional: Enable OpenAI Fallback

If you have an OpenAI API key, create a `.env` file in your project folder:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Then restart your backend.
When rule-based detection fails, GPT will generate a natural language response.

---

## 🧾 API Reference

| Endpoint            | Method | Description                   |
| ------------------- | ------ | ----------------------------- |
| `/`                 | GET    | Health check / status         |
| `/ivr/start`        | POST   | Starts a new IVR call session |
| `/ivr/conversation` | POST   | Handles text or speech input  |
| `/ivr/dtmf`         | POST   | Handles keypad (DTMF) input   |
| `/ivr/end`          | POST   | Ends an active call session   |

---

## 💬 Example Session

```
> Start Call
IVR: Welcome to Indian Railways Customer Support. You can say 'book ticket', 'train status' or 'refund'.

> You: book a ticket
IVR: Sure — I can help with booking. Do you want Sleeper or AC class?

> You: AC
IVR: Booking confirmed for AC class. Thank you!

> End Call
Call ended.
```

---

## 💡 Technical Notes

* Backend uses **FastAPI + Uvicorn**.
* Frontend uses **Web Speech API** for recognition and **SpeechSynthesis** for TTS.
* All sessions are stored **in-memory** — no database required.
* CORS enabled for local testing (`localhost`).
* Easy to extend with new menus or NLP logic.

---

## 🖼️ UI Preview

The HTML file provides:

* A dark card-style interface
* Caller ID display
* Real-time IVR chat log
* Keypad and Listen buttons
* Speech-to-text and TTS integration

---

## 📜 License

MIT License — free to use and modify.

---

**Author:** Santhosh M R
**Version:** 1.0
**Tech Stack:** FastAPI · HTML · JavaScript · Web Speech API


