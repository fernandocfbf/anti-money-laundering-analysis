import streamlit as st
import pandas as pd
import time

# personalized modules
from src.utils.model import get_model
from src.utils.dataset import get_raw_transactions

#preprocess
from src.features import FeatureGenerator

#constants
DATA_PATH = f"src\\data\\output\\raw_transactions.csv"
RANDOM_STATE = 42

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)
st.set_page_config(layout="wide", page_title="AML Analysis")

col_left, col_center, col_right = st.columns([1, 3, 1])
model = get_model(random_state=RANDOM_STATE)

with col_center:
    st.title("AML Customer Scoring")
    st.caption("Upload your data or try a demo to see how it works")

with col_center:
    options = ["Use My Data", "Try Demo"]
    selection = st.segmented_control(
        label="", 
        options=options, 
        selection_mode="single",
        width="stretch",
        default="Try Demo")

    raw_data = None
    if selection == "Use My Data":
        uploaded_file = st.file_uploader(
            "Upload your transactions CSV",
            type=["csv"],
            accept_multiple_files=False
        )
        if uploaded_file:
            raw_data = pd.read_csv(uploaded_file)

    elif selection == "Try Demo":
        st.info("Using sample dataset for demonstration.")
        raw_data = get_raw_transactions(DATA_PATH, sample_percentage=0.001)

    st.write("Preview data:")
    if raw_data is not None:
        st.dataframe(raw_data.head(100), use_container_width=True, height=200)
        st.write(f"Rows loaded: {raw_data.shape[0]:,}")

    run_disabled = True if raw_data is None else False
    if st.button("Run Analysis", disabled=run_disabled):
        with st.spinner("Initializing..."):
            col_spin, col_bar = st.columns([1, 8])
            
            progress_bar = st.progress(0, text="Starting...")

            # Step 1 — Preprocessing
            progress_bar.progress(10, text="Preprocessing data...")

            feature_generator = FeatureGenerator()
            feature_generator.fit(raw_data)
            
            progress_bar.progress(30, text="Generating features...")
            feature_df = feature_generator.transform(raw_data)

            # Step 2 — Preparing data
            progress_bar.progress(50, text="Preparing model input...")
            feature_columns = [col for col in feature_df.columns if col != 'customer_id']
            X = feature_df[feature_columns]

            # Step 3 — Training model
            progress_bar.progress(70, text="Training model...")
            with st.spinner("Running model..."):
                model.fit(X)

            # Step 4 — Scoring
            progress_bar.progress(90, text="Scoring customers...")
            scores = model.score(X)
            feature_df["final_score"] = scores

            # Done
            progress_bar.progress(100, text="Done!")

            feature_df = feature_df.sort_values(by=["final_score"], ascending=False).reset_index(drop=True)
            st.success("Model run completed successfully!")
            st.dataframe(feature_df.head(100), use_container_width=True)