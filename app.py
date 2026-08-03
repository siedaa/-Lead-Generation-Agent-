import streamlit as st
from dotenv import load_dotenv
from agent.pipeline import run_pipeline

load_dotenv()

st.set_page_config(page_title="LeadGenAgent", page_icon="🔍")
st.title("🔍 LeadGenAgent")
st.caption("AI-powered lead generation — describe what you're looking for, get a spreadsheet of leads.")

prompt = st.text_input("Describe the leads you're looking for", placeholder="e.g. coffee shops in Karachi")

if st.button("Search", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a search prompt.")
    else:
        with st.spinner("Searching... this may take 30-60 seconds"):
            result = run_pipeline(prompt, headless=True)

        if result["error"]:
            st.error(result["error"])
        else:
            st.success(f"Found {len(result['leads'])} leads for \"{result['query']}\"")
            st.dataframe(result["leads"], use_container_width=True)

            with open(result["filepath"], "rb") as f:
                st.download_button(
                    label="Download Excel file",
                    data=f,
                    file_name=result["filepath"].split("\\")[-1].split("/")[-1],
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
