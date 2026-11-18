# ⚖️ LexiTech — Tax-Trap Contract Scanner
### Dual-Document "Clause-to-IRS Collision Engine" (Legal & Tax AI)

**LexiTech — Tax-Trap Contract Scanner** is an AI-powered dual-document cross-examination engine built with **Python**, **Streamlit**, and the **Google GenAI SDK (`google-genai`)**. 

Unlike standard single-document chatbots, this application ingests **both** a private legal contract and an official IRS tax publication simultaneously—pitting contract language directly against federal tax rules to uncover hidden tax liabilities before a contract is signed.

🔗 **Live Demo:** *(Add your Streamlit Community Cloud URL here once deployed)*

---

## 🚀 Key Features

* **Dual-Document Cross-Examination:** Upload **Document A (Legal Contract)**—such as a divorce settlement, 1099 independent contractor agreement, LLC operating agreement, or commercial lease—alongside **Document B (Official IRS Tax Manual)** such as IRS Pub 4012, Pub 4491, or Pub 17.
* **Clause-to-IRS Collision Detection:** Scans for hidden "tax traps" where contract wording conflicts with federal dependency, worker classification, income recognition, or deduction eligibility rules.
* **Strict Dual-Citation Grounding:** Every flagged risk is anchored with **both** the exact Contract Section/Clause (Document A) and the exact IRS Publication Tab/Page/Section (Document B) using a strict closed-book, zero-hallucination system prompt.
* **Balanced Renegotiation Redlines:** Automatically drafts protective, ready-to-propose replacement contract language ("Renegotiation Fix") to neutralize each tax trap prior to execution.
* **Dynamic Gemini Model Failover:** Automatically selects and routes requests across available Gemini Flash models for fast, reliable multimodal document processing.
* **One-Click Audit Export:** Download the complete dual-cited Tax-Trap Audit Report as a formatted `.txt` file for legal and tax review.

---

## 🛠️ Tech Stack

* **Frontend & UI:** Streamlit (Custom LexiTech berry-magenta & blush-pink theme)
* **AI & Multimodal Document Engine:** Google GenAI SDK (`google-genai`) with `client.files.upload()`
* **Language:** Python 3.10+

---

## 📂 Repository Structure

```text
lexitech-tax-trap-contract-scanner/
├── .streamlit/
│   └── config.toml        # Custom LexiTech UI theme configuration
├── app.py                 # Main Streamlit dual-document audit application
├── requirements.txt       # Python dependencies (streamlit, google-genai, etc.)
├── LEXItech.PNG           # LexiTech studio brand logo
└── README.md              # Project documentation
```

---

## 💻 Local Setup & Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd lexitech-tax-trap-contract-scanner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. **Enter your Google AI Studio API Key** in the left sidebar when prompted, upload a legal contract and an IRS tax reference PDF, and run your collision scan.

---

## ⚠️ Disclaimer
*This application is a portfolio project built for educational and document-analysis demonstration purposes. It does not constitute formal legal or tax advice.*

---

**© 2026 LexiTech by Heidi Seckman** | Legal & Tax AI Portfolio
