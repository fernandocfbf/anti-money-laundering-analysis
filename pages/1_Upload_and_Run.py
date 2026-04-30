import streamlit as st
import pandas as pd
import plotly.express as px

# personalized modules
from src.utils.translate import get_translator
from src.utils.model import get_model
from src.utils.dataset import get_raw_transactions
from src.explanability import SHAPExplainer
from src.features import FeatureGenerator

page_text_dict = get_translator()

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
        [data-testid="stMetric"] > div {
            background-color: #FFFFFF;
            padding: 1rem 1rem 1rem 2rem;
            border-radius: 1rem;
        }
        [data-testid="stMetricValue"] > div {
            font-size: 1.5rem;
        }
        [data-testid="stMetricLabel"] > div {
            font-size: 0.9rem;
            color: #6B7280;
        }
        [data-testid="stPlotlyChart"] > div {
            background-color: #FFFFFF;
            border-radius: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- INIT STATE ----
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

if "raw_data" not in st.session_state:
    st.session_state.raw_data = None

if "top_offenders_df" not in st.session_state:
    st.session_state.top_offenders_df = None

if "feature_df" not in st.session_state:
    st.session_state.feature_df = None

if "results_expander" not in st.session_state:
    st.session_state.results_expander = False

if "data_source_expander" not in st.session_state:
    st.session_state.data_source_expander = True

if "threshold" not in st.session_state:
    st.session_state.threshold = 0.6

# ---- SIDEBAR ----
with st.sidebar:
    lang = st.segmented_control(
        page_text_dict[st.session_state.lang]["home"]["language"],
        default=st.session_state.lang,
        options=["EN", "PT"],
        selection_mode="single"
    )
    st.session_state.lang = lang
    
t = page_text_dict[st.session_state.lang]["upload_and_run"]

col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    st.title(t["page"]["title"])
    st.caption(t["page"]["subtitle"])

    with st.expander(t["data_source"]["title"], expanded=st.session_state.data_source_expander):

        options = [
            t["data_source"]["options"]["demo"],
            t["data_source"]["options"]["upload"]
        ]

        selection = st.segmented_control(
            label=t["data_source"]["input_method"],
            options=options,
            default=options[0],
            width="stretch"
        )

        st.write("")

        if selection == t["data_source"]["options"]["upload"]:
            st.write(t["data_source"]["upload"]["description"])
            uploaded_file = st.file_uploader(
                t["data_source"]["upload"]["label"],
                type=["csv"],
                help=t["data_source"]["upload"]["help"]
            )
            if uploaded_file is not None:
                st.session_state.raw_data = pd.read_csv(uploaded_file)
                st.success(t["data_source"]["upload"]["success"])
        else:
            st.write(t["data_source"]["demo"]["description"])
            sample_pct = st.number_input(
                t["data_source"]["demo"]["label"],
                min_value=0.01,
                max_value=100.0,
                value=40.0,
                format="%0.1f",
                step=0.5,
                help=t["data_source"]["demo"]["help"]
            )

        st.write("")
        st.write(t["data_source"]["threshold"]["description"])

        explanability_threshold = st.number_input(
            t["data_source"]["threshold"]["label"],
            min_value=0.01,
            max_value=1.0,
            value=0.6,
            format="%0.2f",
            step=0.05,
            help=t["data_source"]["threshold"]["help"]
        )

        st.session_state.threshold = explanability_threshold

        if (st.session_state.raw_data is None and selection == t["data_source"]["options"]["upload"]):
            run_disabled = True
        else:
            run_disabled = False

        run_clicked = st.button(
            t["data_source"]["run_button"],
            disabled=run_disabled,
            use_container_width=True
        )

        if run_clicked:
            progress_bar = st.progress(0, text=t["data_source"]["progress"]["processing"])

            st.session_state.raw_data = get_raw_transactions(
                DATA_PATH,
                sample_percentage=sample_pct / 100
            )
            raw_data = st.session_state.raw_data

            progress_bar.progress(20, text=t["data_source"]["progress"]["features"])
            fg = FeatureGenerator()
            fg.fit(raw_data)
            feature_df = fg.transform(raw_data)

            progress_bar.progress(40, text=t["data_source"]["progress"]["prepare"])
            feature_columns = [c for c in feature_df.columns if c != "customer_id"]
            X = feature_df[feature_columns]

            progress_bar.progress(60, text=t["data_source"]["progress"]["training"])
            model = get_model(random_state=RANDOM_STATE)
            model.fit(X)

            progress_bar.progress(80, text=t["data_source"]["progress"]["scoring"])
            scores = model.score(X)
            feature_df["final_score"] = scores

            progress_bar.progress(95, text=t["data_source"]["progress"]["explanations"])
            explainer = SHAPExplainer(
                threshold=explanability_threshold,
                random_state=RANDOM_STATE
            )
            explanations = explainer.explain(feature_df, "final_score")
            feature_df["explanation"] = explanations

            progress_bar.progress(100, text=t["data_source"]["progress"]["done"])

            feature_df = feature_df.sort_values(by="final_score", ascending=False).reset_index(drop=True)
            top_offenders_df = feature_df[feature_df["final_score"] >= explanability_threshold]

            st.session_state.feature_df = feature_df
            st.session_state.top_offenders_df = top_offenders_df[
                ["customer_id", "final_score", "explanation"]
            ]

            st.success(t["data_source"]["success"])
            st.session_state.data_source_expander = False
            st.session_state.results_expander = True

    with st.expander(t["results"]["title"], expanded=st.session_state.results_expander):

        if st.session_state.top_offenders_df is not None and st.session_state.feature_df is not None:

            feature_df = st.session_state.feature_df
            top_df = st.session_state.top_offenders_df

            total_customers = len(feature_df)
            high_risk_customers = len(top_df)
            high_risk_pct = high_risk_customers / total_customers * 100
            avg_score = feature_df["final_score"].mean()

            st.write("")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric(t["results"]["metrics"]["total"], f"{total_customers:,}")
            col2.metric(t["results"]["metrics"]["high_risk"], f"{high_risk_customers:,}")
            col3.metric(t["results"]["metrics"]["high_risk_pct"], f"{high_risk_pct:.2f}%")
            col4.metric(t["results"]["metrics"]["avg_score"], f"{avg_score:.3f}")

            st.divider()

            fig = px.histogram(
                feature_df,
                x="final_score",
                nbins=30,
                title=t["results"]["chart"]["title"],
                opacity=0.85,
                color_discrete_sequence=["#1C6ED5"]
            )

            fig.add_vline(
                x=explanability_threshold,
                line_dash="dash",
                line_color="#E63946",
                annotation_text=t["results"]["chart"]["threshold"],
                annotation_position="top right"
            )

            fig.update_layout(
                template="plotly_white",
                bargap=0.05,
                xaxis_title=t["results"]["chart"]["x"],
                yaxis_title=t["results"]["chart"]["y"],
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=80, b=40),
                title=dict(x=0.02)
            )

            st.plotly_chart(fig, width="stretch")

            st.divider()

            st.write(t["results"]["table"]["title"])

            cols = t["results"]["table"]["columns"]

            display_df = (
                top_df.rename(columns={
                    "customer_id": cols["customer_id"],
                    "final_score": cols["final_score"],
                    "explanation": cols["explanation"]
                })
                .style.format({cols["final_score"]: "{:.3f}"})
            )

            download_df = (
                feature_df[["customer_id", "final_score", "explanation"]]
                .rename(columns={
                    "customer_id": cols["customer_id"],
                    "final_score": cols["final_score"],
                    "explanation": cols["explanation"]
                })
            )

            download_df[cols["final_score"]] = download_df[cols["final_score"]].round(3)

            st.dataframe(display_df)

            st.download_button(
                t["results"]["download"]["button"],
                data=download_df.to_csv(index=False),
                file_name=t["results"]["download"]["file_name"],
                mime="text/csv",
                type="primary"
            )

        else:
            st.write(t["results"]["empty"])