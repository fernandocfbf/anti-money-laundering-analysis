import streamlit as st
import pandas as pd

# personalized modules
from src.utils.model import get_model
from src.utils.dataset import get_raw_transactions
from src.explanability import SHAPExplainer
from src.features import FeatureGenerator

# constants
DATA_PATH = f"src\\data\\output\\raw_transactions.csv"
RANDOM_STATE = 42

st.set_page_config(layout="wide", page_title="AML Analysis")

# ---- STYLE ----
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }      
    </style>
""", unsafe_allow_html=True)

# ---- INIT STATE ----
if "raw_data" not in st.session_state:
    st.session_state.raw_data = None

if "top_offenders_df" not in st.session_state:
    st.session_state.top_offenders_df = None

if "feature_df" not in st.session_state:
    st.session_state.feature_df = None

col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    st.title("AML Customer Scoring")
    st.caption("Upload your data or try a demo to see how it works")

    data_source_expander = True
    results_expander = False

    with st.expander("1. Data Source", expanded=data_source_expander):
        selection = st.segmented_control(
            label="Choose input method",
            options=["Demo Data", "Upload CSV"],
            default="Demo Data",
            width="stretch"
        )

        st.divider()

        if selection == "Upload CSV":
            st.write("Upload a CSV file containing transaction-level data. The file must follow the required format with appropriate columns for processing.")
            uploaded_file = st.file_uploader(
                "Upload transactions file",
                type=["csv"],
                help="Accepted format: CSV with transaction-level data"
            )
            if uploaded_file is not None:
                st.session_state.raw_data = pd.read_csv(uploaded_file)
                st.success("File uploaded successfully")
        else:
            st.write("Select the percentage of the demo dataset to load. The demo dataset contains synthetic transaction data for testing purposes.")
            sample_pct = st.number_input(
                "Sample percentage",
                min_value=0.01,
                max_value=100.0,
                value=50.0,
                format="%0.1f",
                step=0.5,
                help="Percentage of the demo dataset to load (e.g., 10 for 10%)"
            )
        st.divider()
        st.write("Select the score threshold for explaining customers. Only customers with a risk score above this threshold will have explanations generated.")
        explanability_threshold = st.number_input(
            "Explanability threshold",
            min_value=0.01,
            max_value=1.0,
            value=0.6,
            format="%0.2f",
            step=0.05,
            help="Threshold for generating explanations (e.g., 0.6 means only customers with a score above 0.6 will be explained)"
        )

        if (st.session_state.raw_data is None and selection == "Upload CSV"):
            run_disabled = True
        else: 
            run_disabled = False

        run_clicked = st.button("Run Model", disabled=run_disabled,  use_container_width=True)
            
        if run_clicked:    
            progress_bar = st.progress(0, text="Processing uploaded data...")
            st.session_state.raw_data = get_raw_transactions(DATA_PATH, sample_percentage=sample_pct / 100)
            raw_data = st.session_state.raw_data

            # Step 1
            progress_bar.progress(20, text="Generating customer profiles...")
            fg = FeatureGenerator()
            fg.fit(raw_data)
            feature_df = fg.transform(raw_data)

            # Step 2
            progress_bar.progress(40, text="Preparing model input...")
            feature_columns = [c for c in feature_df.columns if c != "customer_id"]
            X = feature_df[feature_columns]

            # Step 4
            progress_bar.progress(60, text="Training model...")
            model = get_model(random_state=RANDOM_STATE)
            model.fit(X)

            # Step 5
            progress_bar.progress(80, text="Generating scores...")
            scores = model.score(X)
            feature_df["final_score"] = scores

            # Step 6
            progress_bar.progress(95, text="Generating explanations...")
            explainer = SHAPExplainer(threshold=explanability_threshold, random_state=RANDOM_STATE)
            explanations = explainer.explain(feature_df, "final_score")
            feature_df["explanation"] = explanations

            progress_bar.progress(100, text="Done!")

            # Save results
            feature_df = feature_df.sort_values(by="final_score", ascending=False).reset_index(drop=True)
            top_offenders_df = feature_df[feature_df["final_score"] >= explanability_threshold]
            st.session_state.feature_df = feature_df
            st.session_state.top_offenders_df = top_offenders_df[["customer_id", "final_score", "explanation"]]

            st.success("Model run completed successfully!")
            data_source_expander = False
            results_expander = True

    with st.expander("2. Model Results", expanded=results_expander):
        if st.session_state.top_offenders_df is not None:
            st.write("Top offenders based on their risk scores (above the selected threshold)")
            st.dataframe(st.session_state.top_offenders_df)
        else:
            st.write("After running the model, the results will be displayed here. You can view the top customers based on their risk scores and see the explanations for their scores.")