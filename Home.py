import streamlit as st

from src.utils.translate import get_translator

st.set_page_config(
    layout="wide",
    page_title="AML Analysis"
)

page_text_dict = get_translator()

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    /* Main container padding */
    .block-container {
        padding-top: 5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stColumn"] > div {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 14px;
        border: 1px solid #D1D5DB;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        height: 100%;
    }
                
    /* Center title */
    .title {
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

with st.sidebar:
    lang = st.segmented_control(
        "Language",
        default=st.session_state.lang,
        options=["EN", "PT"],
        selection_mode="single"
    )

# ---- HERO SECTION ----
st.markdown(f'<h1 class="title">{page_text_dict[lang]["home"]["hero"]["title"]}</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="subtitle">{page_text_dict[lang]["home"]["hero"]["subtitle"]}</p>',
    unsafe_allow_html=True
)

st.write("")  # spacing


# ---- MAIN CARDS ----
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader(page_text_dict[lang]["home"]["cards"]["analysis"]["title"])
    st.write(page_text_dict[lang]["home"]["cards"]["analysis"]["description"])
    st.write("")
    if st.button(page_text_dict[lang]["home"]["cards"]["analysis"]["button"], key="analysis_button"):
        st.switch_page("pages/1_Upload_and_Run.py")


with col2:
    st.subheader(page_text_dict[lang]["home"]["cards"]["methodology"]["title"])
    st.write(page_text_dict[lang]["home"]["cards"]["methodology"]["description"])
    st.write("")
    if st.button(page_text_dict[lang]["home"]["cards"]["methodology"]["button"], key="methodology_button"):
        st.switch_page("pages/2_Explanation.py")