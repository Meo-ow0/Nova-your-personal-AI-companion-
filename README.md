<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:F4C2CF,100:D6718A&height=150&section=header&text=Nova&fontSize=44&fontColor=ffffff&fontAlignY=40&desc=your%20personal%20AI%20companion&descSize=18&descAlignY=62" alt="Nova - your personal AI companion" />

**A lightweight multimodal AI companion built with Streamlit and the Google GenAI SDK. (•̀ᴗ•́)و**

![Python](https://img.shields.io/badge/Python-D6718A?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-D6718A?style=flat-square&logo=streamlit&logoColor=white)
![Google GenAI](https://img.shields.io/badge/Google%20GenAI-D6718A?style=flat-square&logo=google&logoColor=white)

</div>

---

<!-- Add a screenshot or demo GIF here:
<div align="center"><img src="screenshot.png" width="700" alt="Nova screenshot" /></div>
-->

## About

Nova is a chat companion that runs on your own computer. She remembers facts about you, looks at your pictures, listens and talks back, and can switch between personalities. Everything she saves stays in small local JSON files, so there is no database or cloud storage to set up.

## Features

| Feature | What it does |
|---|---|
| **Pastel UI** | Clean pastel interface with kaomojis in the headers and chat |
| **Long-term memory** | Save facts about yourself to a local JSON file so Nova remembers you between sessions |
| **Quick notes** | Keep code snippets, ideas and to-do lists in the sidebar |
| **Vision** | Upload photos (outfits, ingredients, plants, code screenshots) and Nova analyzes them |
| **Voice loop** | Talk with your microphone and hear Nova's reply out loud |
| **Six languages** | English, Spanish, French, Japanese, Hindi and German for text, speech recognition and audio |
| **Personalities** | Friendly and Casual, Witty and Sarcastic Friend, Wise Zen Mentor, Hyper-Supportive Cheerleader, Strict Coding Coach |

## Tech stack

| | |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **AI engine** | Google GenAI SDK (`google-genai`) |
| **Voice** | `gTTS` for text-to-speech, `streamlit-mic-recorder` for speech-to-text |
| **Storage** | Local JSON files: `memory.json`, `notes.json` |

## Getting started

**1. Clone the project**

```bash
git clone https://github.com/Meo-ow0/Nova-your-personal-AI-companion-.git
cd Nova-your-personal-AI-companion-
```

**2. Install the packages**

```bash
pip install streamlit google-genai gtts pillow streamlit-mic-recorder
```

**3. Add your API key**

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/) and set it the way `app.py` expects (environment variable or secrets file). Keep it private and never upload it to GitHub.

**4. Run the app**

```bash
streamlit run app.py
```

Open the link Streamlit prints in your terminal.

## Privacy

- Memory and notes are stored only on your computer, in `memory.json` and `notes.json`.
- Add `memory.json`, `notes.json` and your key file to `.gitignore` so they never get uploaded.
- Chat text, photos and voice are sent to Google's API to get a reply, so don't share anything you want to keep private.

## Contact

Made by Shreya · [LinkedIn](https://www.linkedin.com/in/shreya-8ab04536b/)

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:D6718A,100:F4C2CF&height=80&section=footer" alt="" />

</div>
