import streamlit as st
from google import genai
from google.genai import types
import tempfile, os

st.set_page_config(
    page_title="LexiTech | Tax-Trap Contract Scanner",
    page_icon="LEXItech.PNG",
    layout="wide"
)

# Signature LexiTech Berry & Blush Executive Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1F1F24; }
    [data-testid="stSidebar"] {
        background-color: #FDF2F7;
        border-right: 1px solid #F2D5E4;
    }
    label, .stMarkdown, p, span, h1, h2, h3, h4, li { color: #1F1F24 !important; }
    
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea,
    .stTextInput input,
    [data-testid="stFileUploaderDropzone"] {
        background-color: #FDF2F7 !important;
        color: #1F1F24 !important;
        border: 1.5px solid #E5B8CE !important;
        border-radius: 10px !important;
    }
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div {
        color: #1F1F24 !important;
    }

    .lexi-hero {
        background: linear-gradient(135deg, #FDF2F7 0%, #FFFFFF 100%);
        border: 1.5px solid #E5B8CE;
        border-left: 6px solid #B81D6F;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 18px;
    }
    .lexi-card {
        background-color: #FDF2F7;
        border: 1.5px solid #E5B8CE;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .lexitech-banner {
        background-color: #FDF2F7;
        border-left: 6px solid #B81D6F;
        padding: 14px 18px;
        border-radius: 10px;
        color: #1F1F24 !important;
        font-weight: 600;
        margin: 14px 0;
    }

    [data-testid="stAlert"],
    [data-testid="stAlertContainer"],
    [data-testid="stNotification"],
    .stSpinner > div {
        background-color: #FDF2F7 !important;
        color: #1F1F24 !important;
        border: 1.5px solid #B81D6F !important;
        border-radius: 10px !important;
    }
    [data-testid="stAlert"] *,
    [data-testid="stAlertContainer"] *,
    [data-testid="stNotification"] *,
    .stSpinner * {
        color: #1F1F24 !important;
    }

    button,
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stTextInput"] button {
        background-color: #B81D6F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    button:hover,
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stTextInput"] button:hover {
        background-color: #961559 !important;
    }
    button *,
    .stButton > button *,
    .stDownloadButton > button *,
    [data-testid="stFileUploaderDropzone"] button *,
    [data-testid="stTextInput"] button * {
        color: #FFFFFF !important;
    }
    [data-testid="stTextInput"] button svg {
        fill: #FFFFFF !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #FDF2F7;
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        border: 1px solid #E5B8CE;
    }
    .stTabs [aria-selected="true"] {
        background-color: #B81D6F !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
if os.path.exists("LEXItech.PNG"):
    st.sidebar.image("LEXItech.PNG", width=135)
st.sidebar.markdown("### 🔑 Engine Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get a free key from Google AI Studio")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick Demo Mode")
use_sample = st.sidebar.checkbox(
    "Use Built-In Sample Collision Case",
    value=False,
    help="Test the engine immediately without uploading PDFs using a realistic Divorce & IRS Dependent Trap scenario."
)

st.sidebar.markdown("---")
st.sidebar.caption("Built by **Heidi Seckman** • **LexiTech Legal & Tax AI**")

# --- HEADER ---
head_col1, head_col2 = st.columns([1, 4])
with head_col1:
    if os.path.exists("LEXItech.PNG"):
        st.image("LEXItech.PNG", width=120)
with head_col2:
    st.title("⚖️ Tax-Trap Contract Scanner")
    st.markdown("**Clause-to-IRS Collision Engine** • Powered by **LexiTech**")

st.markdown("""
<div class="lexi-hero">
    <strong>Dual-Document Cross-Examination:</strong> Pit any private legal agreement (Document A) directly against an official IRS tax manual (Document B) to uncover hidden tax traps, cite exact clauses & IRS pages, and draft balanced renegotiation redlines before signing.
</div>
""", unsafe_allow_html=True)

# --- SAMPLE DATA FOR ONE-CLICK DEMO ---
SAMPLE_CONTRACT = """
MARITAL SETTLEMENT & CUSTODY AGREEMENT (EXCERPT)
Section 4.2 (Tax Dependency Allocation): Regardless of where the minor child resides during the calendar year, Father shall claim the minor child as a Qualifying Child dependent on his federal tax return every tax year without requiring any signed IRS release forms from Mother, even though Mother has primary physical custody for 290 nights per year.
Section 4.3 (Spousal Support Deduction): Pursuant to this agreement executed in 2026, Payor Spouse shall deduct all monthly alimony payments of $2,500 on Schedule 1 of Form 1040, and Recipient Spouse shall report all received payments as taxable gross income.
Section 7.1 (Independent Contractor Consulting): Following divorce, Spouse B will provide ongoing bookkeeping services for Spouse A's business from Spouse A's office using Spouse A's computer, working fixed hours (9:00 AM–5:00 PM) under Spouse A's direct supervision, classified strictly as a 1099-NEC Independent Contractor with no payroll tax withholding.
"""

SAMPLE_IRS_RULES = """
IRS TAX REFERENCE SUMMARY (BENCHMARKED TO IRS PUB 4012 / PUB 4491 / PUB 17)
1. Qualifying Child & Custodial Parent Rule (IRS Pub 4012, Tab C, Page C-4; Pub 4491, Lesson 3): Under IRC § 152(e), the custodial parent is the parent with whom the child lived for the greater number of nights during the year. A noncustodial parent CANNOT claim the child as a dependent unless the custodial parent signs Form 8332 (Release/Revocation of Release of Claim to Exemption for Child by Custodial Parent) and the noncustodial parent attaches Form 8332 to their return. Private divorce decrees executed after 2008 cannot substitute for Form 8332.
2. Alimony Tax Treatment Post-TCJA (IRS Pub 4012, Tab E, Page E-2; Pub 17): For divorce or separation instruments executed after December 31, 2018, alimony or separate maintenance payments are NOT deductible by the payer spouse and are NOT includible in the gross income of the recipient spouse.
3. Worker Classification — Employee vs. Independent Contractor (IRS Pub 15-A / Pub 4491): Under common-law behavioral and financial control rules, when the business controls when, where, and how work is performed, provides the equipment, and sets fixed hours, the worker is a W-2 statutory/common-law employee—not a 1099 independent contractor—regardless of what a private contract labels them.
"""

# --- DOCUMENT INPUTS ---
if not use_sample:
    doc_col1, doc_col2 = st.columns(2)
    with doc_col1:
        st.markdown('<div class="lexi-card"><h4>📄 Document A: Legal Contract</h4><p>Upload a lease, 1099 agreement, divorce settlement, or LLC operating agreement.</p></div>', unsafe_allow_html=True)
        contract_pdf = st.file_uploader("Upload Legal Contract (PDF)", type=["pdf"], key="contract_pdf")
    with doc_col2:
        st.markdown('<div class="lexi-card"><h4>📘 Document B: IRS Tax Manual</h4><p>Upload IRS Pub 4012, Pub 4491, Pub 17, or official tax instructions.</p></div>', unsafe_allow_html=True)
        irs_pdf = st.file_uploader("Upload IRS Reference Guide (PDF)", type=["pdf"], key="irs_pdf")
else:
    st.info("⚡ **Built-In Sample Case Active:** Testing a Marital Settlement & Contractor Agreement against IRS Pub 4012 / Pub 4491 rules.")
    with st.expander("👀 Preview Sample Documents Being Cross-Examined"):
        p1, p2 = st.columns(2)
        with p1:
            st.text_area("Sample Document A (Contract)", SAMPLE_CONTRACT, height=210, disabled=True)
        with p2:
            st.text_area("Sample Document B (IRS Rules)", SAMPLE_IRS_RULES, height=210, disabled=True)

focus_area = st.selectbox("Select Collision Audit Focus:", [
    "Full Tax-Trap Collision Scan (All Clauses vs. IRS Rules)",
    "Dependent, Custody & Filing Status Collisions",
    "1099 Independent Contractor vs. W-2 Misclassification Traps",
    "Income Recognition, Alimony & Deduction Eligibility Traps"
])

custom_notes = st.text_input(
    "Optional Specific Question or Clause to Target:",
    placeholder="e.g., Check if Section 4.2 violates custodial parent release rules or if any clause triggers penalties..."
)

# --- RUN COLLISION ENGINE ---
if st.button("🚀 Run Clause-to-IRS Collision Scan"):
    if not api_key:
        st.warning("Please paste your Gemini API Key in the left sidebar first!")
    elif not use_sample and (not contract_pdf or not irs_pdf):
        st.warning("Please upload BOTH Document A (Legal Contract) and Document B (IRS Tax Manual)—or toggle 'Use Built-In Sample Collision Case' in the sidebar!")
    else:
        with st.spinner("Cross-examining contract clauses against IRS tax rules..."):
            try:
                client = genai.Client(api_key=api_key)

                system_prompt = (
                    "You are the LexiTech Clause-to-IRS Collision Engine, an elite legal-and-tax cross-examination auditor. "
                    "You are given Document A (a private legal contract) and Document B (an official IRS tax reference manual). "
