from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).parent
DATA = ROOT / "data"

st.set_page_config(page_title="RR Pressure Analytics | SuPeRR Selector S2", page_icon="🏏", layout="wide")

NAVY = "#101F38"
PINK = "#D21F68"
CYAN = "#55C4D8"
PALE = "#DCE7F2"

st.markdown(f"""
<style>
.stApp {{ background: linear-gradient(145deg, #0b172b 0%, {NAVY} 55%, #142844 100%); color: #f7f9fc; }}
[data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
.block-container {{ padding-top: 1.7rem; max-width: 1400px; }}
.eyebrow {{ color: {CYAN}; font-size: .82rem; letter-spacing: .14em; font-weight: 800; }}
.hero {{ border-left: 5px solid {PINK}; padding: .4rem 0 .5rem 1.1rem; margin-bottom: 1rem; }}
.hero h1 {{ color: white; font-size: 2.35rem; line-height: 1.1; margin: .35rem 0; }}
.hero p {{ color: {PALE}; font-size: 1rem; margin: .35rem 0; }}
div[data-testid="stMetric"] {{ background: #192d4b; border: 1px solid #314968; padding: 14px 16px; border-radius: 14px; }}
div[data-testid="stMetricLabel"] p {{ color: #b9c9dc !important; }}
div[data-testid="stMetricValue"] {{ color: {CYAN} !important; }}
section[data-testid="stSidebar"] {{ background: #0b1729; }}
section[data-testid="stSidebar"] * {{ color: #edf3fa; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
.stTabs [data-baseweb="tab"] {{ background: #1b3151; border-radius: 8px 8px 0 0; padding: 10px 18px; }}
div[data-testid="stDataFrame"] {{ border: 1px solid #314968; border-radius: 12px; }}
.note {{ background: #192d4b; border: 1px solid #314968; padding: 14px 18px; border-radius: 12px; color: {PALE}; }}
.small {{ color: #b9c9dc; font-size: .84rem; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    bat = pd.read_csv(DATA / "top10_batters.csv")
    bowl = pd.read_csv(DATA / "top10_bowlers.csv")
    return bat, bowl

try:
    batters, bowlers = load_data()
except Exception as exc:
    st.error(f"Could not load dashboard ranking files: {exc}")
    st.stop()

st.markdown("""
<div class="hero">
  <div class="eyebrow">SUPERR SELECTOR • SEASON 2 • ROUND 1</div>
  <h1>Pressure Performance Analytics</h1>
  <p>Evidence-led scouting shortlists for Rajasthan Royals' IPL 2027 auction preparation.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🏏 Dashboard navigation")
    section = st.radio("Go to", ["Overview", "Batters", "Bowlers", "Player comparison", "Methodology"])
    st.divider()
    st.caption("Competition-use analysis. This dashboard contains aggregated top-10 outputs only; it does not contain raw ball-by-ball data.")

# Dataset-level values are taken from the generated analysis_summary.csv for this run.
if section == "Overview":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Matches represented", "867")
    m2.metric("Delivery rows analysed", "200,961")
    m3.metric("Pressure deliveries", "53,846")
    m4.metric("Pressure share", "26.79%")
    st.markdown("### Shortlist leaders")
    left, right = st.columns(2)
    with left:
        st.markdown("#### 🏏 Top pressure batter")
        leader = batters.iloc[0]
        st.metric(str(leader["striker_name"]), f"{leader['score']:.2f} / 100", f"{int(leader['pressure_balls'])} pressure balls")
        st.caption(f"{int(leader['pressure_runs'])} pressure runs • SR {leader['pressure_sr']:.1f} • {int(leader['pressure_innings'])} pressure innings")
    with right:
        st.markdown("#### 🎯 Top pressure bowler")
        leader = bowlers.iloc[0]
        st.metric(str(leader["bowler_name"]), f"{leader['score']:.2f} / 100", f"{int(leader['pressure_legal_balls'])} pressure legal balls")
        st.caption(f"{int(leader['pressure_wickets'])} wickets • Econ {leader['pressure_econ']:.2f} • {int(leader['pressure_innings'])} pressure innings")
    st.markdown("### Top-10 score comparison")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(batters.sort_values("score"), x="score", y="striker_name", orientation="h", text="score", title="Batters — composite score", color_discrete_sequence=[PINK])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", xaxis_title="Score (0–100)", yaxis_title="", margin=dict(l=8,r=8,t=45,b=8), height=420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(bowlers.sort_values("score"), x="score", y="bowler_name", orientation="h", text="score", title="Bowlers — composite score", color_discrete_sequence=[CYAN])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", xaxis_title="Score (0–100)", yaxis_title="", margin=dict(l=8,r=8,t=45,b=8), height=420)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="note"><b>How to read this:</b> scores are role-relative composite percentiles within the eligible player pool. They are scouting indicators for the defined pressure sample—not probabilities of future success or automatic auction recommendations.</div>', unsafe_allow_html=True)

elif section == "Batters":
    st.subheader("Top 10 batters under pressure")
    st.caption("Eligibility in the underlying model: at least 50 pressure balls and 5 pressure innings.")
    view = batters.copy()
    fig = px.bar(view.sort_values("score"), x="score", y="striker_name", orientation="h", text="score", color_discrete_sequence=[PINK])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", xaxis_title="Composite score (0–100)", yaxis_title="", height=500)
    st.plotly_chart(fig, use_container_width=True)
    cols = ["rank","striker_name","score","pressure_runs","pressure_balls","pressure_innings","pressure_sr","pressure_avg","pressure_boundary_pct","pressure_dot_pct","baseline_sr","sr_change"]
    st.dataframe(view[cols].rename(columns={"rank":"Rank","striker_name":"Batter","score":"Score","pressure_runs":"Pressure runs","pressure_balls":"Pressure balls","pressure_innings":"Pressure innings","pressure_sr":"Pressure SR","pressure_avg":"Pressure average","pressure_boundary_pct":"Boundary %","pressure_dot_pct":"Dot-ball %","baseline_sr":"Baseline SR","sr_change":"SR change"}), hide_index=True, use_container_width=True)
    st.download_button("Download batter top-10 CSV", view.to_csv(index=False).encode("utf-8"), "rr_top10_batters.csv", "text/csv")

elif section == "Bowlers":
    st.subheader("Top 10 bowlers under pressure")
    st.caption("Eligibility in the underlying model: at least 50 pressure legal balls and 5 pressure innings.")
    view = bowlers.copy()
    fig = px.bar(view.sort_values("score"), x="score", y="bowler_name", orientation="h", text="score", color_discrete_sequence=[CYAN])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", xaxis_title="Composite score (0–100)", yaxis_title="", height=500)
    st.plotly_chart(fig, use_container_width=True)
    cols = ["rank","bowler_name","score","pressure_wickets","pressure_legal_balls","pressure_innings","pressure_econ","pressure_wicket_rate","pressure_dot_pct","baseline_econ","econ_improvement"]
    st.dataframe(view[cols].rename(columns={"rank":"Rank","bowler_name":"Bowler","score":"Score","pressure_wickets":"Pressure wickets","pressure_legal_balls":"Pressure legal balls","pressure_innings":"Pressure innings","pressure_econ":"Pressure economy","pressure_wicket_rate":"Wickets / 100 balls","pressure_dot_pct":"Dot-ball %","baseline_econ":"Baseline economy","econ_improvement":"Economy improvement"}), hide_index=True, use_container_width=True)
    st.download_button("Download bowler top-10 CSV", view.to_csv(index=False).encode("utf-8"), "rr_top10_bowlers.csv", "text/csv")

elif section == "Player comparison":
    st.subheader("Compare shortlisted players")
    role = st.selectbox("Player role", ["Batter", "Bowler"])
    if role == "Batter":
        df = batters.copy(); name_col = "striker_name"
        options = df[name_col].tolist()
        chosen = st.multiselect("Choose up to 4 batters", options, default=options[:2], max_selections=4)
        metric_cols = ["pressure_sr", "pressure_avg", "pressure_boundary_pct", "pressure_dot_pct", "score"]
        labels = ["Pressure SR", "Pressure average", "Boundary %", "Dot-ball %", "Composite score"]
    else:
        df = bowlers.copy(); name_col = "bowler_name"
        options = df[name_col].tolist()
        chosen = st.multiselect("Choose up to 4 bowlers", options, default=options[:2], max_selections=4)
        metric_cols = ["pressure_econ", "pressure_wicket_rate", "pressure_dot_pct", "score"]
        labels = ["Pressure economy", "Wickets / 100 balls", "Dot-ball %", "Composite score"]
    selected = df[df[name_col].isin(chosen)].copy()
    if not selected.empty:
        display = selected[[name_col] + metric_cols].set_index(name_col)
        st.dataframe(display, use_container_width=True)
        long = selected.melt(id_vars=[name_col], value_vars=metric_cols, var_name="Metric", value_name="Value")
        long["Metric"] = long["Metric"].map(dict(zip(metric_cols, labels)))
        fig = px.bar(long, x="Metric", y="Value", color=name_col, barmode="group", title=f"{role} comparison")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=430)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one player to compare.")

else:
    st.subheader("Methodology at a glance")
    st.markdown("""
**Data scope for this analysis run**
- Formats: T20 and T20I; innings 1 and 2.
- Match dates represented: 22 January 2022 to 1 November 2026.
- 867 matches with ball-by-ball data; 200,961 scoped delivery rows.
- 53,846 deliveries flagged as pressure deliveries (26.79%).

**Pressure-state rules**
- **Chase:** required run rate ≥ 10.5 with ≤ 15 overs remaining; or ≤ 30 runs needed in the final 5 overs; or ≤ 3 wickets remaining with ≤ 10 overs left while the target is outstanding.
- **First innings:** final 3 overs; or ≤ 3 wickets remaining after at least 5 overs, with ≤ 10 overs left.

**Eligibility**
- Batters: at least 50 pressure balls faced across at least 5 pressure innings.
- Bowlers: at least 50 pressure legal balls across at least 5 pressure innings.

**Scoring approach**
- Batter weights: adjusted pressure strike rate 30%, adjusted average 20%, boundary percentage 15%, inverse dot-ball percentage 10%, strike-rate change vs baseline 10%, consistency 10%, pressure-ball sample size 5%.
- Bowler weights: inverse adjusted pressure economy 30%, adjusted wicket rate 25%, dot-ball percentage 15%, economy improvement vs baseline 10%, consistency 10%, pressure legal-ball sample size 10%.
- Shrinkage confidence = n / (n + 60), where n is pressure balls faced (batter) or pressure legal balls (bowler); adjusted pressure metrics are blended with the player's non-pressure baseline.

**Interpretation and limitations**
- Composite scores are percentile-weighted and relative to the eligible role pool.
- This version does not adjust for venue, opposition strength, player role, squad composition, auction price or availability.
- Thresholds and weights are modelling choices; the shortlist should support—not replace—scouting judgement.
""")
    st.warning("This is an independent analytical model based on the supplied competition pack. It is not an official Rajasthan Royals model or endorsement.")

st.markdown("---")
st.markdown('<p class="small">SuPeRR Selector Season 2 • Round 1 | Dashboard uses aggregated top-10 ranking outputs only. Raw competition data is not included.</p>', unsafe_allow_html=True)
