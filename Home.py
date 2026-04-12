import streamlit as st

st.set_page_config(
    layout="wide", 
    page_title="AML Analysis"
)

col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.title("AML Customer Scoring")
    st.caption("Upload transaction data and detect suspicious activity with explanations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Run Analysis")
    st.write("Upload your transaction file and generate AML risk scores.")
    
    if st.button("Go to Upload & Run"):
        st.switch_page("pages/1_Upload_and_Run.py")

with col2:
    st.subheader("How it Works")
    st.write("Understand how scores and explanations are generated.")
    
    if st.button("See Explanation"):
        st.switch_page("pages/2_Explanation.py")
