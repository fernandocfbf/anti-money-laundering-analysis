import streamlit as st
from src.utils.translate import get_translator

page_text_dict = get_translator()

if "lang" not in st.session_state:
    st.session_state.lang = "PT"

with st.sidebar:
    lang = st.segmented_control(
        "Language",
        default=st.session_state.lang,
        options=["EN", "PT"],
        selection_mode="single",
        required=True
    )

t = page_text_dict[lang]["explanation"]

# ---- STYLE ----
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# PAGE HEADER
# ----------------------
st.title(t["page"]["title"], text_alignment="center")
st.caption(t["page"]["subtitle"], text_alignment="center")
st.write("")

# ----------------------
# OVERVIEW
# ----------------------
st.header(t["overview"]["title"], divider="gray")
st.write(t["overview"]["description"])

# ----------------------
# LAYERS
# ----------------------
st.header(t["layers"]["title"], divider="gray")
st.write(t["layers"]["description"])

layers = t["layers"]

with st.expander(layers["isolation_forest"]["title"], expanded=True):
    st.write(layers["isolation_forest"]["description"])
    st.markdown(f"**{layers['isolation_forest']['question']}**")
    st.write(layers["isolation_forest"]["details"])

with st.expander(layers["hdbscan"]["title"]):
    st.write(layers["hdbscan"]["description"])
    st.markdown(f"**{layers['hdbscan']['question']}**")
    st.write(layers["hdbscan"]["details"])

with st.expander(layers["mahalanobis"]["title"]):
    st.write(layers["mahalanobis"]["description"])
    st.markdown(f"**{layers['mahalanobis']['question']}**")
    st.write(layers["mahalanobis"]["details"])

# ----------------------
# COMBINATION
# ----------------------
st.header(t["combination"]["title"], divider="gray")
st.write(t["combination"]["description"])

points = t["combination"]["points"]
st.markdown(f"- {points['global']}")
st.markdown(f"- {points['group']}")
st.markdown(f"- {points['peer']}")

# ----------------------
# EXPLAINABILITY
# ----------------------
st.header(t["explainability"]["title"], divider="gray")
st.write(t["explainability"]["description"])

# ----------------------
# KEY IDEA
# ----------------------
st.header(t["key_idea"]["title"], divider="gray")
st.write(t["key_idea"]["description"])

