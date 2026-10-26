import json

import pandas as pd
import streamlit as st

from support_engine import diagnose

st.set_page_config(
    page_title="AI Support & Incident Diagnosis Copilot",
    page_icon="🛠️",
    layout="wide"
)

st.title("AI Support & Incident Diagnosis Copilot")
st.caption(
    "Independent AI engineering prototype | Synthetic and illustrative data"
)

st.info(
    "This tool provides an initial troubleshooting assessment. "
    "It is not an official Petpooja product."
)

with st.form("incident_form"):
    issue = st.text_area(
        "Describe the incident",
        placeholder=(
            "Example: Online orders are not syncing to the POS"
        ),
        max_chars=2000
    )

    log_text = st.text_area(
        "Optional diagnostic logs",
        placeholder=(
            "Example: 10:02 sync failed; 10:03 connection timeout"
        ),
        max_chars=10000
    )

    submitted = st.form_submit_button(
        "Analyze incident",
        type="primary"
    )

if submitted:
    if not issue.strip():
        st.error("Please describe the incident first.")
    else:
        try:
            with st.spinner("Analyzing incident and searching guidance..."):
                result = diagnose(issue, log_text)

            st.session_state["last_result"] = result

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

result = st.session_state.get("last_result")

if result:
    st.divider()
    st.subheader("Incident assessment")

    col1, col2, col3 = st.columns(3)
    col1.metric("Category", result["category"])
    col2.metric("Severity estimate", result["severity"])
    col3.metric("Status", result["status"])

    st.write("**Reported incident:**", result["incident"])

    st.subheader("Recommended checks")
    if result["evidence"]:
        for item in result["evidence"]:
            with st.expander(
                f'{item["source"]} | Relevance: {item["score"]:.2f}'
            ):
                st.write(item["text"])
    else:
        st.warning(
            "No matching guidance was retrieved. "
            "Escalate for human review."
        )

    st.subheader("Diagnostic log findings")
    findings = result["log_findings"]

    if findings:
        st.dataframe(
            pd.DataFrame(findings),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No diagnostic logs were provided.")

    st.subheader("Escalation")
    if result["escalation_required"]:
        st.warning("Human review is recommended.")
    else:
        st.write(
            "Verify the suggested checks before deciding whether "
            "escalation is necessary."
        )

    st.caption(result["disclaimer"])

    st.download_button(
        "Export incident report (JSON)",
        data=json.dumps(result, indent=2),
        file_name="incident_report.json",
        mime="application/json"
    )

