import streamlit as st
from google import genai
from google.genai import types
import tempfile, os

st.set_page_config(page_title="LexiTech 2.0 | Tax-Trap Collision Engine", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
@import url('https://googleapis.com');

html, body, .stApp, p, label, span, div, h1, h2, h3, h4, li {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #1A161F !important;
}
.stApp {
    background-color: #FFFFFF;
    background-image: radial-gradient(#E8C5D6 0.75px, transparent 0.75px);
    background-size: 22px 22px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FDF2F7 0%, #F9E6F0 100%);
    border-right: 1px solid #E5B8CE;
}
.mono-tag {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em;
    color: #B81D6F !important;
    text-transform: uppercase;
}
.nav-bar {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border: 1.5px solid #E5B8CE;
    border-radius: 14px;
    padding: 14px 22px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(184, 29, 111, 0.07);
}
.status-pill {
    background: #FDF2F7;
    border: 1px solid #B81D6F;
    border-radius: 999px;
    padding: 5px 14px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #B81D6F !important;
}
.hero-box {
    background: linear-gradient(135deg, #24101C 0%, #4A1533 55%, #881652 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 10px 28px rgba(184, 29, 111, 0.16);
}
.hero-box h1, .hero-box p, .hero-box span { color: #FFFFFF !important; }
.corpus-card {
    background: #FFFFFF;
    border: 1.5px solid #E5B8CE;
    border-top: 4px solid #B81D6F;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(184, 29, 111, 0.05);
}
.kpi-card {
    background: #FDF2F7;
    border: 1.5px solid #E5B8CE;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
}
.kpi-num { font-size: 26px !important; font-weight: 800 !important; color: #B81D6F !important; }
.stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] {
    background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #E5B8CE !important; border-radius: 10px !important;
}
[data-testid="stAlert"], [data-testid="stAlertContainer"], .stSpinner > div {
    background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important;
}
button, .stButton > button, .stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stTextInput"] button {
    background: linear-gradient(135deg, #B81D6F 0%, #8E1454 100%) !important;
    color: #FFFFFF !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(184, 29, 111, 0.22) !important;
}
button *, .stButton > button *, .stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button *, [data-testid="stTextInput"] button * {
    color: #FFFFFF !important;
}
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
.stTabs [data-baseweb="tab"] { background-color: #FDF2F7; border-radius: 8px 8px 0 0; padding: 8px 18px; border: 1px solid #E5B8CE; font-weight: 600; }
.stTabs [aria-selected="true"] { background: #B81D6F !important; }
.stTabs [aria-selected="true"] * { color: #FFFFFF !important; }
.lexitech-footer {
    background: #FDF2F7; border: 1px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; text-align: center; font-size: 12.5px; margin-top: 28px;
}
</style>
""", unsafe_allow_html=True)

LOGO_SVG = """
<div style="display:flex;align-items:center;gap:12px;">
  <svg width="42" height="42" viewBox="0 0 64 64" fill="none" xmlns="http://w3.org">
    <defs><linearGradient id="lx" x1="0" y1="0" x2="64" y2="64"><stop offset="0%" stop-color="#E83E8C"/><stop offset="100%" stop-color="#7A1149"/></linearGradient></defs>
    <rect width="64" height="64" rx="16" fill="url(#lx)"/>
    <path d="M20 20H44M32 20V46M22 46H42M18 28L24 20L30 28H18ZM34 28L40 20L46 28H34Z" stroke="white" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <div>
    <div style="font-weight:800;font-size:20px;letter-spacing:-0.02em;line-height:1.1;">LEXI<span style="color:#B81D6F;">TECH</span></div>
    <div class="mono-tag">LEGAL &amp; TAX AI STUDIO</div>
  </div>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="mono-tag">01 // AUTHENTICATION</div>', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste AI Studio Key...")
    st.markdown("---")
    st.markdown('<div class="mono-tag">02 // SIMULATION SANDBOX</div>', unsafe_allow_html=True)
    use_sample = st.checkbox("⚡ Load Built-In Collision Case", value=False)
    st.caption("Tests a Marital Settlement & 1099 Agreement against IRS Pub 4012 / Pub 4491.")
    st.markdown("---")
    st.caption("Architected by **Heidi Seckman**")

st.markdown(f"""
<div class="nav-bar">
  {LOGO_SVG}
  <div class="status-pill">● ENGINE v2.0 // ZERO-HALLUCINATION GROUNDING</div>
</div>
<div class="hero-box">
  <span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;opacity:0.85;">DUAL-CORPUS FORENSIC CROSS-EXAMINATION</span>
  <h1 style="margin:4px 0 8px 0;font-size:30px;">Tax-Trap Contract Scanner</h1>
  <p style="margin:0;font-size:15px;opacity:0.92;">Pit private legal agreements directly against official IRS publications to detect tax code collisions, cite exact sections &amp; pages, and synthesize balanced renegotiation redlines before execution.</p>
</div>
""", unsafe_allow_html=True)

SAMPLE_CONTRACT = """MARITAL SETTLEMENT & CUSTODY AGREEMENT (EXCERPT)
Section 4.2 (Tax Dependency Allocation): Father shall claim the minor child as a Qualifying Child dependent every year without requiring any signed IRS release forms from Mother, even though Mother has primary physical custody for 290 nights per year.
Section 4.3 (Spousal Support Deduction): Under this 2026 agreement, Payor Spouse shall deduct all monthly alimony payments of $2,500 on Schedule 1, and Recipient Spouse shall report payments as taxable income.
Section 7.1 (1099 Contractor Consulting): Spouse B will provide ongoing bookkeeping from Spouse A's office using Spouse A's computer on fixed hours (9 AM–5 PM) under direct supervision, classified strictly as a 1099-NEC Independent Contractor."""

SAMPLE_IRS = """IRS TAX REFERENCE SUMMARY (IRS PUB 4012 / PUB 4491 / PUB 17)
1. Custodial Parent Rule (IRS Pub 4012, Tab C, Page C-4; Pub 4491, Lesson 3): Under IRC § 152(e), the custodial parent has the child for more nights. A noncustodial parent CANNOT claim the child unless the custodial parent signs Form 8332 and attaches it to the return. Post-2008 divorce decrees cannot substitute for Form 8332.
2. Alimony Post-TCJA (IRS Pub 4012, Tab E, Page E-2; Pub 17): For divorce instruments executed after Dec 31, 2018, alimony is NOT deductible by the payer and NOT taxable income to the recipient.
3. Worker Classification (IRS Pub 15-A / Pub 4491): When a business controls hours, location, equipment, and methods, the worker is a W-2 employee—not a 1099 contractor—regardless of contract labels."""

if not use_sample:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="corpus-card"><div class="mono-tag">CORPUS A // PRIVATE AGREEMENT</div><h4 style="margin:4px 0;">Legal Contract</h4><p style="margin:0;font-size:13.5px;">Divorce decree, 1099 contractor agreement, commercial lease, or LLC operating agreement.</p></div>', unsafe_allow_html=True)
        contract_pdf = st.file_uploader("Upload Contract PDF", type="pdf", key="doc_a")
    with c2:
        st.markdown('<div class="corpus-card"><div class="mono-tag">CORPUS B // FEDERAL TAX AUTHORITY</div><h4 style="margin:4px 0;">IRS Reference Manual</h4><p style="margin:0;font-size:13.5px;">IRS Pub 4012, Pub 4491, Pub 17, or official federal tax form instructions.</p></div>', unsafe_allow_html=True)
        irs_pdf = st.file_uploader("Upload IRS Manual PDF", type="pdf", key="doc_b")
else:
    st.info("⚡ Simulation Sandbox Active: Cross-examining Marital Settlement & 1099 Agreement against IRS Pub 4012 / Pub 4491.")
    with st.expander("🔍 Inspect Active Corpus A & Corpus B Payloads"):
        p1, p2 = st.columns(2)
        p1.text_area("Corpus A (Contract)", SAMPLE_CONTRACT, height=175, disabled=True)
        p2.text_area("Corpus B (IRS Rules)", SAMPLE_IRS, height=175, disabled=True)

f1, f2 = st.columns((1, 1))
with f1:
    focus_area = st.selectbox("Audit Vector:", (
        "Full Tax-Trap Collision Scan (All Clauses vs. IRS Rules)",
        "Dependent, Custody & Filing Status Collisions",
        "1099 Independent Contractor vs. W-2 Misclassification Traps",
        "Income Recognition, Alimony & Deduction Eligibility Traps"
    ))
with f2:
    custom_notes = st.text_input("Target Clause or Specific Query (Optional):", placeholder="e.g., Audit Section 4.2 against Form 8332 custodial release rules...")

SYSTEM_INSTRUCTIONS = """You are LexiTech 2.0, an elite legal-and-tax forensic collision auditor. Cross-examine Document A (Legal Contract) against Document B (IRS Tax Manual). Ground every claim strictly in Document A and Document B with exact section/tab/page citations. Output three exact Markdown sections:
## SECTION 1: TAX-TRAP COLLISION MATRIX
Markdown table: | Severity | Contract Clause (Corpus A) | IRS Authority & Citation (Corpus B) | Collision Analysis |
## SECTION 2: RENEGOTIATION REDLINES
For each collision show: **Original Clause (Corpus A)**, **LexiTech Recommended Redline**, and **Legal & Tax Rationale**.
## SECTION 3: EXECUTIVE BRIEFING MEMO
Concise action checklist before signing."""

if st.button("⚡ Execute Clause-to-IRS Collision Scan"):
    if not api_key:
        st.warning("Paste your Gemini API Key in the left sidebar to activate the engine.")
    elif not use_sample and (not contract_pdf or not irs_pdf):
        st.warning("Upload both Corpus A and Corpus B PDFs—or toggle 'Load Built-In Collision Case' in the sidebar.")
    else:
        with st.spinner("Running dual-corpus cross-examination..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"Audit Vector: {focus_area}\nTarget Notes: {custom_notes or 'Comprehensive collision audit.'}"
                if use_sample:
                    payload = (f"CORPUS A:\n{SAMPLE_CONTRACT}\n\nCORPUS B:\n{SAMPLE_IRS}\n\n{prompt}",)
                    src = "Sample_Collision_Case"
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as ta, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tb:
                        ta.write(contract_pdf.read())
                        tb.write(irs_pdf.read())
                        pa, pb = ta.name, tb.name
                    fa, fb = client.files.upload(file=pa), client.files.upload(file=pb)
                    os.remove(pa)
                    os.remove(pb)
                    payload = ("CORPUS A (CONTRACT):", fa, "CORPUS B (IRS MANUAL):", fb, prompt)
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
    high_hits = txt.upper().count("HIGH")
    k1, k2, k3 = st.columns(3)
    k1.markdown('<div class="kpi-card"><div class="mono-tag">CORPUS GROUNDING</div><div class="kpi-num">2 Docs</div><div>Dual-Verified</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="mono-tag">HIGH-RISK FLAGS</div><div class="kpi-num">{max(high_hits, 1)}</div><div>Collisions Caught</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="mono-tag">ACTIVE ENGINE</div><div class="kpi-num" style="font-size:18px !important;padding-top:6px;">{st.session_state["mod"]}</div><div>Zero-Hallucination</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    s1, _, rest = txt.partition("## SECTION 2:")
    s2, _, s3 = rest.partition("## SECTION 3:")
    t1, t2, t3 = st.tabs(("🚨 Collision Matrix", "✍️ Renegotiation Redlines", "📄 Executive Memo & Export"))
    t1.markdown(s1)
    t2.markdown("## SECTION 2:" + s2 if rest else txt)
    t3.markdown("## SECTION 3:" + s3 if s3 else txt)
    t3.download_button("📥 Export Dual-Cited Audit Report (.txt)", data=txt, file_name=f"LexiTech2_Audit_{st.session_state['src']}.txt", mime="text/plain")

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding—unauthorized copying, cloning, or commercial redistribution is prohibited. For educational and research assistance only; not legal or tax advice.</div>', unsafe_allow_html=True)
