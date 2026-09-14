import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import os
import json
from PIL import Image
from streamlit_mic_recorder import speech_to_text

# --- Simple Storage Helpers (Zero bloat, tiny JSON files) ---
MEMORY_FILE = "memory.json"
NOTES_FILE = "notes.json"

def load_data(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_val
    return default_val

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Load persistent memory and notes
stored_memories = load_data(MEMORY_FILE, [])
user_notes = load_data(NOTES_FILE, [])

# 1. Page Configuration
st.set_page_config(
    page_title="Nova - AI Companion",
    page_icon="♥",
    layout="centered"
)

# Initialize the Gemini client using secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Sidebar for Customization & Features
st.sidebar.header("(✿) Companion Settings")
companion_name = st.sidebar.text_input("Bot Name", value="Nova")

personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "Friendly & Casual",
        "Witty & Sarcastic Friend",
        "Wise Zen Mentor",
        "Hyper-Supportive Cheerleader",
        "Strict Coding Coach"
    ]
)

# Language mapping
language_options = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Japanese": "ja",
    "Hindi": "hi",
    "German": "de"
}

selected_lang_name = st.sidebar.selectbox("Choose Language", list(language_options.keys()))
lang_code = language_options[selected_lang_name]

# Map personalities
instructions_map = {
    "Friendly & Casual": "You are a warm, friendly, and helpful AI companion.",
    "Witty & Sarcastic Friend": "You are a witty, sarcastic, but deeply loyal best friend. Keep answers punchy and fun.",
    "Wise Zen Mentor": "You are a calm, philosophical mentor who gives thoughtful, grounding advice.",
    "Hyper-Supportive Cheerleader": "You are extremely enthusiastic, positive, and always hype up the user!",
    "Strict Coding Coach": "You are a pragmatic, no-nonsense programming mentor who focuses on clean code and logic."
}

# Combine base instruction with stored memories so Nova remembers you!
memory_context = f"\nThings you remember about the user: {', '.join(stored_memories)}" if stored_memories else ""
selected_instruction = f"{instructions_map[personality]}{memory_context} You must always reply in {selected_lang_name}."

st.sidebar.markdown("---")
st.sidebar.markdown("### (ω) Voice Input")
spoken_text = speech_to_text(language=lang_code, start_prompt=f"Speak ({selected_lang_name})", stop_prompt="Stop", key='mic')

# --- Sidebar: Memory & Notes Management ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Nova's Memory Bank")
new_memory = st.sidebar.text_input("Teach Nova a fact about you:")
if st.sidebar.button("Save Memory"):
    if new_memory:
        stored_memories.append(new_memory)
        save_data(MEMORY_FILE, stored_memories)
        st.sidebar.success("Memory saved!")
        st.rerun()

if stored_memories:
    with st.sidebar.expander("View Saved Memories"):
        for i, mem in enumerate(stored_memories):
            st.write(f"- {mem}")
        if st.button("Clear Memories"):
            save_data(MEMORY_FILE, [])
            st.rerun()

st.sidebar.markdown("### 📝 Quick Notes")
note_input = st.sidebar.text_area("Jot down a quick note:")
if st.sidebar.button("Add Note"):
    if note_input:
        user_notes.append(note_input)
        save_data(NOTES_FILE, user_notes)
        st.sidebar.success("Note added!")
        st.rerun()

if user_notes:
    with st.sidebar.expander("View Notes"):
        for i, note in enumerate(user_notes):
            st.write(f"{i+1}. {note}")
        if st.button("Clear All Notes"):
            save_data(NOTES_FILE, [])
            st.rerun()

# --- Styled Proper Header Banner ---
st.markdown(
    f"""
    <div style="background-color: #fff0f3; padding: 22px; border-radius: 16px; text-align: center; border: 1px solid #ffd1dc; margin-bottom: 25px;">
        <h1 style="color: #d16ba5; margin: 0; font-family: sans-serif; font-size: 28px;">(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Chat with {companion_name}</h1>
        <p style="color: #8c788c; margin: 8px 0 0 0; font-size: 15px;">Current Vibe: <b>{personality}</b> &bull; Language: <b>{selected_lang_name}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Image Uploader Feature
uploaded_file = st.file_uploader("Show Nova an image (optional)...", type=["jpg", "jpeg", "png"])
image_payload = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Attached Image", width=300)
    image_payload = image

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        kaomoji_prefix = "(｡｡) " if message["role"] == "assistant" else "(•̀ᴗ•́)و "
        st.markdown(kaomoji_prefix + message["content"])

# 5. Handle Chat Input
user_query = st.chat_input(f"Say something to {companion_name}...")

if spoken_text:
    user_query = spoken_text

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown("(•̀ᴗ•́)و " + user_query)
        if image_payload:
            st.image(image_payload, width=200)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(f"{companion_name} is looking and typing..."):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=selected_instruction,
                    temperature=0.7,
                )

                chat = client.chats.create(
                    model="gemini-3.6-flash",
                    config=config
                )
                
                content_to_send = [user_query]
                if image_payload:
                    content_to_send.append(image_payload)

                response = chat.send_message(content_to_send)
                response_text = response.text
                
                st.markdown("(｡｡) " + response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                try:
                    tts = gTTS(text=response_text, lang=lang_code, slow=False)
                    audio_file = "temp_voice.mp3"
                    tts.save(audio_file)
                    st.audio(audio_file, format='audio/mp3')
                except Exception:
                    pass
                
            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")