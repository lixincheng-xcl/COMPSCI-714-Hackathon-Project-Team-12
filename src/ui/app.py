import json
import sys
import tempfile
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.review_pipeline import ReviewPipeline


st.set_page_config(
    page_title="Research Contract Adviser Agent",
    page_icon="📄",
    layout="wide",
)


@st.cache_resource
def load_pipeline():
    return ReviewPipeline()


def run_review(file_path: str):
    pipeline = load_pipeline()
    output = pipeline.run(file_path)

    loaded = output["loaded"]
    classification = output["classification"]
    clauses = output["clauses"]
    payload = output["payload"]
    markdown_report = output["markdown_report"]
    json_report = json.dumps(payload, indent=2, ensure_ascii=False)

    return loaded, classification, clauses, payload, markdown_report, json_report


def flag_badge(flag: str) -> str:
    mapping = {
        "Green": "🟢 Green",
        "Amber": "🟠 Amber",
        "Red": "🔴 Red",
        "Blue": "🔵 Blue",
    }
    return mapping.get(flag, flag)


def render_result_card(item):
    reference = item.get("reference", {})

    with st.expander(
        f"{flag_badge(item['flag'])} | Clause {item['clause_number']}: {item['clause_title']}",
        expanded=item["flag"] in {"Red", "Amber"},
    ):
        col1, col2, col3 = st.columns(3)
        col1.metric("Topic", item.get("topic", ""))
        col2.metric("Confidence", item.get("confidence", ""))
        col3.metric("Human Review", "Required" if item.get("human_review_required") else "No")

        st.markdown("**Clause Text**")
        st.info(item.get("clause_text", ""))

        st.markdown("**Rationale**")
        st.write(item.get("rationale", ""))

        if item.get("risk_indicators"):
            st.markdown("**Detected Risk Indicators**")
            for risk in item["risk_indicators"]:
                st.code(risk)

        st.markdown("**Retrieved Reference**")
        st.write(f"**Source File:** {reference.get('source_file', '')}")
        st.write(f"**Reference Type:** {reference.get('reference_type', '')}")
        st.write(f"**Contract Type Hint:** {reference.get('contract_type_hint', '')}")
        st.write(f"**Reference Topic:** {reference.get('chunk_topic', '')}")
        st.write(f"**Retrieval Score:** {reference.get('score', 0.0)}")

        st.markdown("**Reference Snippet**")
        st.caption(reference.get("snippet", ""))


st.title("📄 Research Contract Adviser Agent")
st.caption("COMPSCI 714 Hackathon Project · Team 12 · Human-in-the-loop contract review support")

st.warning(
    "This is an academic proof-of-concept system. It supports human review only. "
    "It does not provide legal advice, approve contracts, or replace professional judgement."
)

st.info(
    "Azure / Microsoft Foundry integration is available for the final demo. "
    "A Microsoft Foundry Agent named Research-Contract-Adviser-Agent-Team-12 has been created using the gpt-4o deployment. "
    "For AutoDL demo stability, live Azure calls are disabled by default, while the Foundry Agent can be demonstrated separately in the Azure portal."
)

with st.sidebar:
    st.header("Demo Controls")

    demo_choice = st.radio(
        "Choose input mode",
        [
            "Upload a contract",
            "Use safe sample contract",
            "Use risky sample contract",
        ],
    )

    st.markdown("---")
    st.markdown("### Supported files")
    st.write("- TXT")
    st.write("- PDF")
    st.write("- DOCX")

    st.markdown("### Reference knowledge base")
    st.write("UoA templates and Contracting Positions are loaded from local server files.")
    st.markdown("---")
    st.markdown("### Azure / Microsoft Foundry")
    st.write("- Foundry Agent: Research-Contract-Adviser-Agent-Team-12")
    st.write("- Model deployment: gpt-4o")
    st.write("- Purpose: Azure-based explanation support")
    st.write("- Live Azure calls are disabled in AutoDL runtime for demo stability.")

uploaded_file = None
input_path = None

if demo_choice == "Upload a contract":
    uploaded_file = st.file_uploader(
        "Upload a contract file",
        type=["txt", "pdf", "docx"],
    )

    if uploaded_file is not None:
        temp_dir = tempfile.mkdtemp()
        upload_path = Path(temp_dir) / uploaded_file.name
        upload_path.write_bytes(uploaded_file.getvalue())
        input_path = str(upload_path)

elif demo_choice == "Use safe sample contract":
    input_path = str(PROJECT_ROOT / "data" / "sample_contracts" / "sample_contract.txt")
    st.success("Using safe sample contract.")

else:
    input_path = str(PROJECT_ROOT / "data" / "sample_contracts" / "risky_contract.txt")
    st.error("Using risky sample contract with deliberately high-risk clauses.")

run_button = st.button("Run Contract Review", type="primary")

if run_button:
    if not input_path:
        st.error("Please upload a contract file first.")
    else:
        with st.spinner("Running contract review pipeline..."):
            try:
                loaded, classification, clauses, payload, markdown_report, json_report = run_review(input_path)

                st.success("Review completed.")

                st.subheader("1. Document Summary")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("File", loaded["file_name"])
                c2.metric("Contract Type", classification["contract_type"])
                c3.metric("Confidence", f"{classification['confidence']:.2f}")
                c4.metric("Clauses", len(clauses))

                st.subheader("2. Flag Counts")

                counts = payload["flag_counts"]

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🔴 Red", counts["Red"])
                m2.metric("🟠 Amber", counts["Amber"])
                m3.metric("🔵 Blue", counts["Blue"])
                m4.metric("🟢 Green", counts["Green"])

                st.subheader("3. Review Results")

                grouped = payload["grouped_results"]

                tabs = st.tabs(
                    [
                        "🔴 Red Flags",
                        "🟠 Amber Flags",
                        "🔵 Blue Flags",
                        "🟢 Green Flags",
                    ]
                )

                flag_order = ["Red", "Amber", "Blue", "Green"]

                for tab, flag in zip(tabs, flag_order):
                    with tab:
                        items = grouped.get(flag, [])
                        if not items:
                            st.info(f"No {flag} flags.")
                        else:
                            for item in items:
                                render_result_card(item)

                st.subheader("4. Download Reports")

                d1, d2 = st.columns(2)

                d1.download_button(
                    label="Download Markdown Report",
                    data=markdown_report,
                    file_name=f"{Path(loaded['file_name']).stem}_review_report.md",
                    mime="text/markdown",
                )

                d2.download_button(
                    label="Download JSON Report",
                    data=json_report,
                    file_name=f"{Path(loaded['file_name']).stem}_review_report.json",
                    mime="application/json",
                )

                with st.expander("Preview Markdown Report"):
                    st.markdown(markdown_report)

            except Exception as e:
                st.error(f"Review failed: {e}")