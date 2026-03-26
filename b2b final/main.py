import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.metric-card {
    background:#0f172a;
    padding:20px;
    border-radius:15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
.metric-title {
    font-size:18px;
    color:#94a3b8;
}
.metric-value {
    font-size:40px;
    font-weight:bold;
    margin-top:10px;
}
.border-blue {border-left:6px solid #3b82f6;}
.border-green {border-left:6px solid #22c55e;}
.border-yellow {border-left:6px solid #facc15;}
.border-red {border-left:6px solid #ef4444;}
.section-header {
    font-size:26px;
    margin-top:25px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Supplier Risk Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("Supplier_Risk_Dataset_5000 AP Group 5.xlsx")
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# ---------------- COLUMN DETECTION ----------------
def find_col(keys):
    for col in df.columns:
        for key in keys:
            if key in col:
                return col
    return None

supplier = find_col(["supplier","name"])
delivery = find_col(["delivery"])
cost = find_col(["cost"])
quality = find_col(["quality"])
risk = find_col(["risk"])
performance = find_col(["performance","score","rating"])

# ---------------- CREATE PERFORMANCE IF MISSING ----------------
if performance is None:
    df["performance_score"] = (df[quality]*0.6) - (df[delivery]*0.2)
    performance = "performance_score"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

selected_risk = st.sidebar.multiselect(
    "Select Risk Level",
    options=df[risk].unique(),
    default=df[risk].unique()
)

df = df[df[risk].isin(selected_risk)]

# ---------------- COLOR MAP ----------------
color_map = {
    "Low": "#22c55e",
    "Medium": "#facc15",
    "High": "#ef4444"
}

# ---------------- KPI CARDS ----------------
st.markdown('<div class="section-header">Key Business Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card border-blue">
<div class="metric-title">Total Suppliers</div>
<div class="metric-value">{len(df)}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card border-green">
<div class="metric-title">Avg Delivery Time</div>
<div class="metric-value">{df[delivery].mean():.2f}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card border-yellow">
<div class="metric-title">Avg Cost</div>
<div class="metric-value">₹{df[cost].mean():.0f}</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card border-red">
<div class="metric-title">High Risk Suppliers</div>
<div class="metric-value">{df[df[risk]=="High"].shape[0]}</div>
</div>
""", unsafe_allow_html=True)

# ---------------- TOP DASHBOARD ----------------
st.markdown('<div class="section-header">Supplier Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1, col2 = st.columns(2)

col1, col2 = st.columns(2)

# ---------------- DASHBOARD ----------------
st.markdown('<div class="section-header">Supplier Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ---------------- GRAPH 1: SUPPLIER PERFORMANCE ----------------
with col1:
    fig1 = px.box(
        df,
        x=risk,
        y=performance,
        color=risk,
        color_discrete_map=color_map,
        title="Supplier Performance"
    )

    fig1.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="Risk Level",
        yaxis_title="Performance"
    )

    st.plotly_chart(fig1, use_container_width=True)
# ---------------- GRAPH 2: RISK DISTRIBUTION ----------------
with col2:
    risk_counts = df[risk].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]

    fig2 = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        hole=0.5,
        color="Risk Level",
        color_discrete_map=color_map,
        title="Risk Distribution"
    )

    fig2.update_traces(
        textinfo='percent+label',   # 🔥 shows label + %
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
    )

    fig2.update_layout(template="plotly_dark", height=350)

    st.plotly_chart(fig2, use_container_width=True)


# ---------------- GRAPH 3: COST VS QUALITY ----------------
st.markdown('<div class="section-header">Cost vs Quality Analysis</div>', unsafe_allow_html=True)

fig3 = px.scatter(
    df.sample(1000),
    x=cost,
    y=quality,
    color=risk,
    color_discrete_map=color_map,
    opacity=0.7,
    hover_data=[supplier],   # 🔥 supplier visible on hover
    title="Cost vs Quality Analysis"
)

fig3.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- DATA ----------------
st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)