import streamlit as st
from google import genai
from google.genai import types
import tempfile, os

st.set_page_config(page_title="LexiTech | Tax-Trap Contract Scanner", page_icon="LEXItech.PNG", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #FFFFFF; color: #1F1F24; }
[data-testid="stSidebar"] { background-color: #FDF2F7; border-right: 1px solid #F2D5E4; }
label, .stMarkdown, p, span, h1, h2, h3, h4, li { color: #1F1F24 !important; }
.stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] {
    background-color: #FDF2F7 !important; color: #1F1F24 !important; border: 1.5px solid #E5B8CE !important; border-radius: 10px !important;
}
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[data-baseweb="select"] div { color: #1F1F24 !important; }
.lexi-hero { background: linear-gradient(135deg, #FDF2F7 0%, #FFFFFF 100%); border: 1.5px solid #E5B8CE; border-left: 6px solid #B81D6F; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; }
.lexi-card { background-color: #FDF2F7; border: 1.5px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; }
.lexitech-banner { background-color: #FDF2F7; border-left: 6px solid #B81D6F; padding: 14px 18px; border-radius: 10px; color: #1F1F24 !important; font-weight: 600; margin: 14px 0; }
.lexitech-footer { background-color: #FDF2F7; border: 1px solid #E5B8CE; border-radius: 10px; padding: 14px 18px; text-align: center; font-size: 13px; color: #1F1F24 !important; margin-top: 24px; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], [data-testid="stNotification"], .stSpinner > div { background-color: #FDF2F7 !important; color: #1F1F24 !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important; }
[data-testid="stAlert"] *, [data-testid="stAlertContainer"] *, [data-testid="stNotification"] *, .stSpinner * { color: #1F1F24 !important; }
button, .stButton > button, .stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stTextInput"] button { background-color: #B81D6F !important; color: #FFFFFF !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
button:hover, .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFileUploaderDropzone"] button:hover, [data-testid="stTextInput"] button:hover { background-color: #961559 !important; }
button *, .stButton > button *, .stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button *, [data-testid="stTextInput"] button * { color: #FFFFFF !important; }
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
.stTabs [data-baseweb="tab"] { background-color: #FDF2F7; border-radius: 8px 8px 0 0; padding: 8px 16px; border: 1px solid #E5B8CE; }
.stTabs [aria-selected="true"] { background-color: #B81D6F !important; }
.stTabs [aria-selected="true"] * { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

if os.path.exists("LEXItech.PNG"):
    st.sidebar.image("LEXItech.PNG", width=135)
st.sidebar.markdown("### 🔑 Engine Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("---")
use_sample = st.sidebar.checkbox("⚡ Use Built-In Sample Collision Case", value=False)
st.sidebar.caption("Built by **Heidi Seckman** • **LexiTech Legal & Tax AI**")

h1, h2 = st.columns((1, 5))
with h1:
    if os.path.exists("LEXItech.PNG"):
        st.image("LEXItech.PNG", width=125)
with h2:
    st.title("⚖️ Tax-Trap Contract Scanner")
    st.markdown("**Clause-to-IRS Collision Engine** • Powered by **LexiTech**")

st.markdown('<div class="lexi-hero"><strong>Dual-Document Cross-Examination:</strong> Pit any private legal agreement (Document A) directly against an official IRS tax manual (Document B) to uncover hidden tax traps, cite exact clauses & IRS pages, and draft balanced renegotiation redlines before signing.</div>', unsafe_allow_html=True)

SAMPLE_CONTRACT = """MARITAL SETTLEMENT & CUSTODY AGREEMENT (EXCERPT)
Section 4.2 (Tax Dependency Allocation): Father shall claim the minor child as a Qualifying Child dependent every year without requiring any signed IRS release forms from Mother, even though Mother has primary physical custody for 290 nights per year.
Section 4.3 (Spousal Support Deduction): Under this 2026 agreement, Payor Spouse shall deduct all monthly alimony payments of $2,500 on Schedule 1, and Recipient Spouse shall report payments as taxable income.
Section 7.1 (1099 Contractor Consulting): Spouse B will provide ongoing bookkeeping from Spouse A's office using Spouse A's computer on fixed hours (9 AM–5 PM) under direct supervision, classified strictly as a 1099-NEC Independent Contractor."""

SAMPLE_IRS = """IRS TAX REFERENCE SUMMARY (IRS PUB 4012 / PUB 4491 / PUB 17)
1. Custodial Parent Rule (IRS Pub 4012, Tab C, Page C-4; Pub 4491, Lesson 3): Under IRC § 152(e), the custodial parent has the child for more nights. A noncustodial parent CANNOT claim the child unless the custodial parent signs Form 8332 and it is attached to the return. Post-2008 divorce decrees cannot substitute for Form 8332.
2. Alimony Post-TCJA (IRS Pub 4012, Tab E, Page E-2; Pub 17): For divorce instruments executed after Dec 31, 2018, alimony is NOT deductible by the payer and NOT taxable income to the recipient.
3. Worker Classification (IRS Pub 15-A / Pub 4491): When a business controls hours, location, equipment, and methods, the worker is a W-2 employee—not a 1099 contractor—regardless of contract labels."""

if not use_sample:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="lexi-card"><h4>📄 Document A: Legal Contract</h4><p>Upload a lease, 1099 agreement, divorce settlement, or LLC operating agreement.</p></div>', unsafe_allow_html=True)
        contract_pdf = st.file_uploader("Upload Legal Contract (PDF)", type="pdf", key="doc_a")
    with c2:
        st.markdown('<div class="lexi-card"><h4>📘 Document B: IRS Tax Manual</h4><p>Upload IRS Pub 4012, Pub 4491, Pub 17, or official tax instructions.</p></div>', unsafe_allow_html=True)
        irs_pdf = st.file_uploader("Upload IRS Reference Guide (PDF)", type="pdf", key="doc_b")
else:
    st.info("⚡ Built-In Sample Case Active: Cross-examining a Marital Settlement & 1099 Agreement against IRS Pub 4012 / Pub 4491 rules.")
    with st.expander("👀 Preview Sample Documents"):
        p1, p2 = st.columns(2)
        p1.text_area("Document A (Contract)", SAMPLE_CONTRACT, height=180, disabled=True)
        p2.text_area("Document B (IRS Rules)", SAMPLE_IRS, height=180, disabled=True)

focus_area = st.selectbox("Select Collision Audit Focus:", (
    "Full Tax-Trap Collision Scan (All Clauses vs. IRS Rules)",
    "Dependent, Custody & Filing Status Collisions",
    "1099 Independent Contractor vs. W-2 Misclassification Traps",
    "Income Recognition, Alimony & Deduction Eligibility Traps"
))
custom_notes = st.text_input("Optional Specific Question or Clause to Target:", placeholder="e.g., Check if Section 4.2 violates Form 8332 custodial release rules...")

SYSTEM_INSTRUCTIONS = """You are the LexiTech Clause-to-IRS Collision Engine. Compare Document A (Legal Contract) against Document B (IRS Tax Manual). Ground every finding ONLY in Document A and Document B with exact section/tab/page citations. Format your output into three exact Markdown sections:
## SECTION 1: TAX-TRAP COLLISION MATRIX
Markdown table with columns: | Risk Level | Contract Clause (Doc A) | IRS Rule & Citation (Doc B) | Hidden Tax Trap |
## SECTION 2: RENEGOTIATION REDLINES
For each risk show: **Original Risky Language (Doc A)**, **LexiTech Recommended Replacement Clause**, and **Why This Fixes It**.
## SECTION 3: EXECUTIVE SUMMARY MEMO
Concise plain-English action briefing before signing."""

if st.button("🚀 Run Clause-to-IRS Collision Scan"):
    if not api_key:
        st.warning("Please paste your Gemini API Key in the left sidebar first!")
    elif not use_sample and (not contract_pdf or not irs_pdf):
        st.warning("Upload BOTH Document A and Document B—or check 'Use Built-In Sample Collision Case' in the sidebar!")
    else:
        with st.spinner("Cross-examining contract clauses against IRS tax rules..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"Audit Focus: {focus_area}\nNotes: {custom_notes or 'Full cross-examination.'}"
                if use_sample:
                    payload = (f"DOCUMENT A:\n{SAMPLE_CONTRACT}\n\nDOCUMENT B:\n{SAMPLE_IRS}\n\n{prompt}",)
                    src = "Sample_Collision_Case"
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as ta, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tb:
                        ta.write(contract_pdf.read())
                        tb.write(irs_pdf.read())
                        pa, pb = ta.name, tb.name
                    fa, fb = client.files.upload(file=pa), client.files.upload(file=pb)
                    os.remove(pa)
                    os.remove(pb)
                    payload = ("DOCUMENT A (CONTRACT):", fa, "DOCUMENT B (IRS MANUAL):", fb, prompt)
                    src = f"{contract_pdf.name}_vs_{irs_pdf.name}"

                models = tuple(m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name)
                for m_name in models:
                    try:
                        res = client.models.generate_content(model=m_name, contents=list(payload), config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS))
                        st.session_state["rep"], st.session_state["mod"], st.session_state["src"] = res.text, m_name, src
                        break
                    except Exception:
                        continue
            except Exception as e:
                st.error(f"Error: {e}")

if "rep" in st.session_state:
    txt = st.session_state["rep"]
    st.markdown(f"<div class='lexitech-banner'>✨ Collision Audit Complete! • Powered by LexiTech ({st.session_state['mod']})</div>", unsafe_allow_html=True)
    s1, _, rest = txt.partition("## SECTION 2:")
    s2, _, s3 = rest.partition("## SECTION 3:")
    t1, t2, t3 = st.tabs(("🚨 Tax-Trap Collision Matrix", "✍️ Renegotiation Redlines", "📄 Full Audit Memo & Export"))
    t1.markdown(s1)
    t2.markdown("## SECTION 2:" + s2 if rest else txt)
    t3.markdown("## SECTION 3:" + s3 if s3 else txt)
    t3.download_button("📥 Download Dual-Cited Audit Report (.txt)", data=txt, file_name=f"LexiTech_Audit_{st.session_state['src']}.txt", mime="text/plain")

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding—unauthorized copying or commercial redistribution is prohibited. For educational and research assistance only; not legal or tax advice.</div>', unsafe_allow_html=True)
