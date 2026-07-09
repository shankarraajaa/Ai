import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Customer 360 Dashboard",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
crm = pd.read_csv("crm.csv")
support = pd.read_csv("support.csv")
emails = pd.read_csv("emails.csv")

# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI Customer 360 Dashboard")
st.write("A unified customer profile combining CRM, Support, and Email insights.")

# -----------------------------
# Customer Selection
# -----------------------------
customer = st.selectbox("Select Customer", crm["Company"])

cust = crm[crm["Company"] == customer].iloc[0]
cid = cust["CustomerID"]

tickets = support[support["CustomerID"] == cid]
mail = emails[emails["CustomerID"] == cid]

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Deal Value", f"${cust['DealValue']}")

with col2:
    st.metric("📌 Stage", cust["Stage"])

with col3:
    st.metric("📅 Renewal", cust["RenewalDate"])

with col4:
    st.metric("🎫 Open Tickets", len(tickets[tickets["Status"] == "Open"]))

st.divider()

# -----------------------------
# CRM & Support Side by Side
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("📋 CRM Details")
    st.dataframe(cust.to_frame(), use_container_width=True)

with right:
    st.subheader("🎫 Support Tickets")
    st.dataframe(tickets, use_container_width=True)

st.divider()

# -----------------------------
# Email
# -----------------------------
st.subheader("📧 Latest Customer Email")

st.info(mail.iloc[0]["Body"])

# -----------------------------
# AI Logic
# -----------------------------
risk = []

if "Open" in tickets["Status"].values:
    risk.append("Open support tickets requiring immediate attention.")

if "slow" in mail.iloc[0]["Body"].lower():
    risk.append("Customer is dissatisfied with support response times.")

if "crash" in mail.iloc[0]["Body"].lower():
    risk.append("Critical product stability issue reported.")

opp = []

if cust["Stage"] == "Negotiation":
    opp.append("High probability of closing this deal.")

if cust["Stage"] == "Proposal":
    opp.append("Follow up on proposal and answer pending questions.")

if cust["Stage"] == "Qualified":
    opp.append("Schedule a product demonstration.")

summary = f"""
### Customer Summary

**Company:** {cust['Company']}

**Sales Stage:** {cust['Stage']}

**Deal Value:** ${cust['DealValue']}

**Account Owner:** {cust['Owner']}

**Last Meeting:** {cust['LastMeeting']}

**Renewal Date:** {cust['RenewalDate']}

**Customer's Latest Feedback:**

> {mail.iloc[0]['Body']}
"""

st.divider()

# -----------------------------
# AI Summary
# -----------------------------
st.subheader("🤖 AI Customer Insights")

st.success(summary)

# -----------------------------
# Risks & Opportunities
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("⚠️ Risks")

    if risk:
        for r in risk:
            st.error(r)
    else:
        st.success("No major risks detected.")

with col2:

    st.subheader("🚀 Opportunities")

    if opp:
        for o in opp:
            st.success(o)
    else:
        st.info("No immediate opportunity identified.")

st.divider()

# -----------------------------
# Customer Health Score
# -----------------------------
st.subheader("📊 Customer Health Score")

score = 100

if len(risk) == 1:
    score = 75

if len(risk) == 2:
    score = 55

if len(risk) >= 3:
    score = 30

st.progress(score)

st.write(f"**Health Score:** {score}/100")

st.divider()

# -----------------------------
# Next Best Action
# -----------------------------
st.subheader("✅ Recommended Next Best Action")

if score <= 30:
    st.error("""
Immediately assign the issue to the Customer Success team,
resolve product problems, and schedule an executive follow-up call.
""")

elif score <= 75:
    st.warning("""
Resolve open support issues and proactively contact the customer
before discussing renewal or upselling.
""")

else:
    st.success("""
Customer is healthy.
Schedule a renewal meeting and discuss upsell opportunities.
""")

st.divider()

# -----------------------------
# Footer
# -----------------------------
st.caption("Built using Streamlit | Dummy CRM + Support + Email Data | AI Tool-Building Challenge")