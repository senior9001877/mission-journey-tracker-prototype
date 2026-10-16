import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Mission Journey Tracker — Prototype", layout="wide")

# --- Header
st.markdown("## Riverside Foodie Trail (M01)  ·  Theme: Food journey  ·  2026-04-01 → 2026-04-30")
st.markdown("**Cost THB:** 1,800,000  ·  **Target:** Thai families & office workers")

# --- Metric tiles
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
col1.metric("Participants", "2,450")
col2.metric("Completers", "412")
col3.metric("Completion %", "16.8%")
col4.metric("Total incremental spend (THB)", "1,200,000")
col5.metric("ROI (inc THB / cost THB)", "0.67")
col6.metric("Cost / completer (THB)", "4,370")

st.markdown("---")

# --- Main area: two columns
left, right = st.columns([3,2])

with left:
    st.subheader("Journey Funnel")
    # Placeholder funnel using bar chart
    steps = ["Start", "Food hall", "SOOKSIAM food", "River Park kiosk", "Dessert lane", "Concierge redeem"]
    counts = [2450, 2010, 1127, 637, 412, 412]
    df_f = pd.DataFrame({"step": steps, "count": counts})
    fig = px.bar(df_f, x="count", y="step", orientation="h", text="count",
                 labels={"count":"Reached", "step":"Step"}, width=800, height=320,
                 color="step", color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Step details")
    df_table = pd.DataFrame({
        "index":[1,2,3,4,5],
        "step":["Food hall check-in","SOOKSIAM street-food","River Park kiosk (outdoor)","Dessert lane","Redeem Concierge"],
        "reached":[2450,2010,1127,637,412],
        "pct":["100%","82%","46%","26%","16.8%"],
        "avg_minutes":[5,15,40,55,65],
        "top_comment":["","Great way to see...","Couldn't scan the QR...","Too hot, gave up","Queue 20 min"]
    })
    st.dataframe(df_table, height=240)

with right:
    st.subheader("Join channel & completion")
    channel_df = pd.DataFrame({
        "channel":["QR poster","LINE push","App banner","Tourist staff"],
        "starters":[900,1000,350,200],
        "completion_pct":[0.20,0.10,0.30,0.40]
    })
    figc = px.bar(channel_df, x="channel", y="starters", text="starters", color="completion_pct",
                  color_continuous_scale=["#E74C3C","#2E8B57"], labels={"completion_pct":"Completion %"})
    st.plotly_chart(figc, use_container_width=True, height=220)

    st.subheader("Time-of-day completion heatmap")
    heat = pd.DataFrame(np.random.randint(0,100,size=(7,24)), 
                        index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], 
                        columns=[str(h) for h in range(24)])
    st.dataframe(heat.style.background_gradient(cmap='Blues'), height=220)

    st.subheader("Segment incremental spend")
    seg = pd.DataFrame({
        "segment":["Thai family","Office worker","Gen Z","Tourist CN","Tourist other"],
        "baseline":[2400,1300,900,5200,4100],
        "avg_spend":[3000,1500,950,5200,4300]
    })
    seg["increment"] = seg["avg_spend"] - seg["baseline"]
    figseg = px.bar(seg, x="segment", y="increment", text="increment", color="increment",
                    color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(figseg, use_container_width=True, height=220)

st.markdown("---")
st.subheader("Worst step detail")
st.markdown("River Park kiosk (outdoor) — Drop-off: 36% of starters")
st.markdown("> Top comment: \"Couldn't scan the QR at River Park, network was down.\"")
st.markdown("- Evidence: 42 survey mentions of 'River Park' or 'network' or 'hot'.")
st.markdown("**Recommended fixes:** 1) Add shaded staffed kiosk, 2) Offline QR fallback, 3) Update LINE start message with landmark + map.")
st.button("Export action brief (PDF)")
st.button("Open comment list")

st.sidebar.header("Filters")
st.sidebar.selectbox("Mission", ["M01 Riverside Foodie Trail"]) 
st.sidebar.checkbox("Impute blank spend as 0", value=True)
st.sidebar.selectbox("Language", ["All", "EN", "TH", "CN"])