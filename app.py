import tempfile

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from gtts.lang import tts_langs


st.set_page_config(page_title="Language Translator", page_icon="🌍", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b);
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 2rem;
        font-size: 1.05rem;
    }

    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 12px 40px rgba(15, 23, 42, 0.35);
    }

    .result-card {
        margin-top: 1.5rem;
    }

    .section-title {
        color: #e2e8f0;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .result-text {
        color: #f8fafc;
        font-size: 1.05rem;
        line-height: 1.7;
        background: rgba(15, 23, 42, 0.45);
        border-radius: 16px;
        padding: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        margin-top: 0.75rem;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb, #a855f7);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        font-weight: 700;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 24px rgba(168, 85, 247, 0.45);
    }

    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        background: rgba(15, 23, 42, 0.75) !important;
        color: white !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }

    .stats-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 0.8rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 class="main-title">🌍 AI Language Translation Tool</h1>
    <p class="subtitle">Translate between 130+ languages instantly with a sleek AI-powered experience.</p>
    """,
    unsafe_allow_html=True,
)

languages = GoogleTranslator().get_supported_languages(as_dict=True)
tts_supported_languages = tts_langs()

if "translated_text" not in st.session_state:
    st.session_state["translated_text"] = ""
if "source_lang" not in st.session_state:
    st.session_state["source_lang"] = "english"
if "target_lang" not in st.session_state:
    st.session_state["target_lang"] = "hindi" if "hindi" in languages else sorted(languages.keys())[0]

text = st.text_area(
    "📝 Enter Text",
    height=180,
    placeholder="Type your text here...",
)

col1, col2, col3 = st.columns([1, 0.35, 1])

language_options = sorted(languages.keys())

with col1:
    source_lang = st.selectbox(
        "🌐 Source Language",
        language_options,
        index=language_options.index(st.session_state["source_lang"]),
        key="source_lang",
    )

with col2:
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    swap_languages = st.button("🔄 Swap")

with col3:
    target_lang = st.selectbox(
        "🎯 Target Language",
        language_options,
        index=language_options.index(st.session_state["target_lang"]),
        key="target_lang",
    )

if swap_languages:
    st.session_state["source_lang"], st.session_state["target_lang"] = (
        st.session_state["target_lang"],
        st.session_state["source_lang"],
    )
    st.rerun()

translate = st.button("✨ Translate Now")

st.markdown("</div>", unsafe_allow_html=True)

if translate:
    if text.strip():
        try:
            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang],
            ).translate(text)
            st.session_state["translated_text"] = translated
            st.success("Translation completed successfully.")
        except Exception as error:
            st.session_state["translated_text"] = ""
            st.error(str(error))
    else:
        st.session_state["translated_text"] = ""
        st.warning("Please enter some text.")

if st.session_state["translated_text"]:
    st.markdown("<div class='glass result-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔮 Translation Result</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='result-text'>{st.session_state['translated_text']}</div>",
        unsafe_allow_html=True,
    )
    st.code(st.session_state["translated_text"])

    target_tts_code = languages[target_lang]
    if target_tts_code in tts_supported_languages:
        tts = gTTS(st.session_state["translated_text"], lang=target_tts_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)

            with open(fp.name, "rb") as audio_file:
                audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.info(f"Text-to-speech is not available for {target_lang}.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("🌍 Languages", "130+")
metric_col2.metric("⚡ Speed", "<1 sec")
metric_col3.metric("🤖 AI Powered", "Yes")
metric_col4.metric("🔒 Secure", "100%")
