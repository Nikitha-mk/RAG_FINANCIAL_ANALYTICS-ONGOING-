import streamlit as st
import pandas as pd
import anthropic

# ── SYNTHETIC DATASET ──────────────────────────────────────────────────────────────
data = [
    {"date": "2024-01-07", "category": "Salary",        "desc": "Monthly Salary",     "amount": 55000, "type": "credit"},
    {"date": "2024-01-03", "category": "Food",          "desc": "Zomato Order",        "amount": 450,   "type": "debit"},
    {"date": "2024-01-05", "category": "Transport",     "desc": "Ola Ride",            "amount": 180,   "type": "debit"},
    {"date": "2024-01-09", "category": "Shopping",      "desc": "Amazon Order",        "amount": 3200,  "type": "debit"},
    {"date": "2024-01-14", "category": "Utilities",     "desc": "Electricity Bill",    "amount": 1200,  "type": "debit"},
    {"date": "2024-01-15", "category": "Entertainment", "desc": "Netflix",             "amount": 649,   "type": "debit"},
    {"date": "2024-01-20", "category": "Food",          "desc": "Restaurant Dinner",   "amount": 1800,  "type": "debit"},
    {"date": "2024-01-28", "category": "Shopping",      "desc": "Electronics Store",   "amount": 15000, "type": "debit"},
    {"date": "2024-02-01", "category": "Salary",        "desc": "Monthly Salary",      "amount": 55000, "type": "credit"},
    {"date": "2024-02-06", "category": "Rent",          "desc": "House Rent",          "amount": 12000, "type": "debit"},
    {"date": "2024-02-14", "category": "Shopping",      "desc": "Valentine Gift",      "amount": 4500,  "type": "debit"},
    {"date": "2024-02-22", "category": "Investment",    "desc": "SIP Mutual Fund",     "amount": 5000,  "type": "debit"},
    {"date": "2024-03-01", "category": "Salary",        "desc": "Monthly Salary",      "amount": 55000, "type": "credit"},
    {"date": "2024-03-07", "category": "Shopping",      "desc": "Flipkart Sale",       "amount": 8900,  "type": "debit"},
    {"date": "2024-03-15", "category": "Rent",          "desc": "House Rent",          "amount": 12000, "type": "debit"},
    {"date": "2024-03-25", "category": "Investment",    "desc": "Stock Purchase",      "amount": 10000, "type": "debit"},
]
df = pd.DataFrame(data)

# ── SIMPLE RAG KNOWLEDGE BASE ─────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "income":      "Total income is ₹1,65,000 from 3 monthly salaries of ₹55,000 each.",
    "food":        "Food spending is ₹2,250 across 2 transactions. Avg food order ₹1,125.",
    "shopping":    "Shopping total is ₹31,600. Largest: Electronics Store ₹15,000 (anomaly).",
    "rent":        "Rent is ₹12,000/month, ₹24,000 total. That's 21.8% of monthly income.",
    "investment":  "Investments: SIP ₹5,000 + Stocks ₹10,000 = ₹15,000 total.",
    "anomaly":     "Anomalies detected: Electronics Store ₹15,000 and Flipkart ₹8,900 are unusually high.",
    "savings":     "Total income ₹1,65,000 minus expenses ₹73,879 = net savings ₹91,121. Savings rate ~55%.",
    "transport":   "Transport: Ola ride ₹180 only. Very low transport spend.",
    "utilities":   "Utilities: Electricity ₹1,200 + Netflix ₹649 = ₹1,849 total.",
    "entertainment": "Entertainment: Netflix ₹649.",
    "expense":     "Total expenses ₹73,879 across 13 debit transactions.",
}

def retrieve(query: str) -> str:
    q = query.lower()
    hits = []
    for topic, fact in KNOWLEDGE_BASE.items():
        if topic in q or any(w in q for w in topic.split()):
            hits.append(fact)
    # fallback: return all if nothing matched
    if not hits:
        hits = list(KNOWLEDGE_BASE.values())
    return "\n".join(hits)

def ask_claude(question: str, api_key: str) -> str:
    context = retrieve(question)
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        system=f"""You are a financial assistant. Answer using ONLY this data:
{context}
Be concise. Use ₹ for amounts. Max 3 sentences.""",
        messages=[{"role": "user", "content": question}]
    )
    return msg.content[0].text

# ── ANOMALY DETECTION (basic z-score) ────────────────────────────────────────
def get_anomalies():
    debits = df[df["type"] == "debit"].copy()
    mean = debits["amount"].mean()
    std  = debits["amount"].std()
    return debits[debits["amount"] > mean + 1.5 * std][["date","desc","category","amount"]]

# ── STREAMLIT UI ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="FinanceRAG", page_icon="✦", layout="wide")
st.title("✦ FinanceRAG — AI Financial Assistant")
st.caption("Prototype · Synthetic dataset · RAG + Claude")

# Sidebar — API key
with st.sidebar:
    st.header("⚙️ Setup")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("---")
    st.markdown("**Dataset:** 16 transactions, Jan–Mar 2024")
    st.markdown("**Model:** Claude via Anthropic API")
    st.markdown("**Retrieval:** Keyword-based RAG")

# KPI row
total_income  = df[df["type"]=="credit"]["amount"].sum()
total_expense = df[df["type"]=="debit"]["amount"].sum()
net_savings   = total_income - total_expense

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Income",   f"₹{total_income:,.0f}")
col2.metric("💸 Expenses", f"₹{total_expense:,.0f}")
col3.metric("🏦 Savings",  f"₹{net_savings:,.0f}")
col4.metric("⚠️ Anomalies", len(get_anomalies()))

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Analytics", "⚠️ Anomalies"])

# ── TAB 1: CHAT ───────────────────────────────────────────────────────────────
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            if not api_key:
                reply = "⚠️ Please enter your Anthropic API key in the sidebar."
            else:
                with st.spinner("Thinking..."):
                    try:
                        reply = ask_claude(prompt, api_key)
                    except Exception as e:
                        reply = f"Error: {e}"
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown("**Try asking:** `How much did I spend on shopping?` · `Any anomalies?` · `What's my savings rate?`")

# ── TAB 2: ANALYTICS ──────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Spending by Category")
        cat = df[df["type"]=="debit"].groupby("category")["amount"].sum().sort_values(ascending=False)
        st.bar_chart(cat)

    with col_b:
        st.subheader("Monthly Expenses")
        df["month"] = pd.to_datetime(df["date"]).dt.strftime("%b")
        monthly = df[df["type"]=="debit"].groupby("month")["amount"].sum()
        monthly = monthly.reindex(["Jan","Feb","Mar"])
        st.bar_chart(monthly)

# ── TAB 3: ANOMALIES ──────────────────────────────────────────────────────────
with tab3:
    st.subheader("⚠️ Flagged Transactions (>1.5σ above mean)")
    anomalies = get_anomalies()
    if anomalies.empty:
        st.success("No anomalies found.")
    else:
        st.dataframe(anomalies, use_container_width=True)
        st.warning(f"{len(anomalies)} unusual transaction(s) detected. Review these for overspending or fraud.")
