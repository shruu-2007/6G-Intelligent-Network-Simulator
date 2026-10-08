
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="6G Intelligent Network Simulator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(circle at 20% 0%, rgba(62, 88, 255, .12), transparent 30%),
                radial-gradient(circle at 100% 10%, rgba(0, 210, 180, .10), transparent 25%),
                #070b17;
    color: #edf2ff;
}
.block-container { padding-top: 1.4rem; max-width: 1450px; }
.hero {
    padding: 26px 30px;
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(20,29,58,.96), rgba(10,15,31,.96));
    box-shadow: 0 20px 60px rgba(0,0,0,.25);
    margin-bottom: 20px;
}
.hero h1 { font-size: 2.35rem; margin: 0; font-weight: 800; letter-spacing: -.04em; }
.hero p { color: #9eabd0; margin: 7px 0 0; font-size: 1rem; }
.badge {
    display:inline-block; padding:5px 10px; border-radius:999px;
    background:rgba(70,95,255,.14); color:#9eaeff; font-size:.78rem;
    font-weight:700; letter-spacing:.04em; margin-bottom:9px;
}
.metric {
    border:1px solid rgba(255,255,255,.08);
    border-radius:17px; padding:16px 18px; background:rgba(16,23,43,.82);
}
.metric .label { color:#8e9abd; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }
.metric .value { color:#f5f7ff; font-size:1.65rem; font-weight:800; margin-top:4px; }
.metric .delta { color:#65dfbb; font-size:.76rem; margin-top:3px; }
.section {
    font-size:1.1rem; font-weight:750; margin:24px 0 10px;
}
.info-card {
    padding:16px 18px; border-radius:16px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(16,23,43,.7);
}
.small { color:#8f9abb; font-size:.82rem; }
.status-good { color:#66e0bb; font-weight:700; }
.status-warn { color:#ffd166; font-weight:700; }
.status-bad { color:#ff7188; font-weight:700; }
div[data-testid="stSidebar"] {
    background: #0a0f20;
    border-right: 1px solid rgba(255,255,255,.07);
}
button[kind="primary"] {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Simulation ----------
SCENARIOS = {
    "Normal Traffic": {"load": 46, "latency": 8.4, "loss": 0.3, "throughput": 820, "users": 680},
    "Campus Rush": {"load": 78, "latency": 18.5, "loss": 1.8, "throughput": 710, "users": 1320},
    "Massive Congestion": {"load": 96, "latency": 78.0, "loss": 7.2, "throughput": 390, "users": 1980},
    "Emergency / Ultra-Low Latency": {"load": 84, "latency": 5.6, "loss": 1.0, "throughput": 650, "users": 420},
}

if "scenario" not in st.session_state:
    st.session_state.scenario = "Normal Traffic"
if "optimized" not in st.session_state:
    st.session_state.optimized = False

def current_metrics():
    base = SCENARIOS[st.session_state.scenario].copy()
    if st.session_state.optimized:
        base["load"] = max(35, base["load"] - 22)
        base["latency"] = max(3.2, base["latency"] * 0.36)
        base["loss"] = max(0.08, base["loss"] * 0.30)
        base["throughput"] = min(960, base["throughput"] * 1.38)
    return base

def path_stats():
    scenario = st.session_state.scenario
    if st.session_state.optimized:
        return {
            "route": "BS-01 → R2 → R4 → Edge-02",
            "hops": 3,
            "reason": "R3 congestion avoided; Edge-02 has lower queue depth."
        }
    if scenario == "Massive Congestion":
        return {
            "route": "BS-01 → R2 → R3 → Core",
            "hops": 3,
            "reason": "Primary route is overloaded."
        }
    return {
        "route": "BS-01 → R2 → R3 → Core",
        "hops": 3,
        "reason": "Lowest-cost baseline route."
    }

def network_graph():
    G = nx.Graph()
    edges = [
        ("BS-01", "R1", 12), ("BS-01", "R2", 8), ("R1", "R3", 18),
        ("R2", "R3", 9), ("R2", "R4", 7), ("R3", "Core", 11),
        ("R4", "Core", 10), ("R4", "Edge-02", 5), ("BS-02", "R4", 8),
        ("BS-02", "Edge-01", 6)
    ]
    for a,b,w in edges:
        G.add_edge(a,b,weight=w)
    return G

def topology_fig():
    G = network_graph()
    pos = {
        "BS-01": (0,1.2), "R1":(1.2,1.8), "R2":(1.2,.6),
        "R3":(2.7,1.5), "R4":(2.7,.4), "Core":(4.1,1.3),
        "BS-02":(1.0,-.8), "Edge-01":(2.2,-1.0), "Edge-02":(3.7,-.2)
    }
    route = [("BS-01","R2"),("R2","R4"),("R4","Edge-02")] if st.session_state.optimized else [("BS-01","R2"),("R2","R3"),("R3","Core")]
    fig = go.Figure()
    for a,b in G.edges():
        x=[pos[a][0],pos[b][0],None]; y=[pos[a][1],pos[b][1],None]
        is_route = (a,b) in route or (b,a) in route
        fig.add_trace(go.Scatter(x=x,y=y,mode="lines",
            line=dict(width=4 if is_route else 1.5),
            opacity=0.9 if is_route else .28,
            hoverinfo="skip", showlegend=False))
    groups = {
        "Radio": ["BS-01","BS-02"],
        "Router": ["R1","R2","R3","R4"],
        "Core": ["Core"],
        "Edge": ["Edge-01","Edge-02"]
    }
    symbols = {"Radio":"triangle-up","Router":"circle","Core":"hexagon","Edge":"square"}
    for group,nodes in groups.items():
        fig.add_trace(go.Scatter(
            x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes],
            mode="markers+text", text=nodes, textposition="bottom center",
            marker=dict(size=25, symbol=symbols[group], line=dict(width=1)),
            name=group
        ))
    fig.update_layout(
        height=440, margin=dict(l=5,r=5,t=10,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        font=dict(color="#dfe6ff"), legend=dict(orientation="h", y=-.05)
    )
    return fig

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 📡 6G Control Center")
    st.caption("Interactive network simulation")
    st.divider()

    scenario = st.selectbox("Simulation scenario", list(SCENARIOS.keys()),
                            index=list(SCENARIOS.keys()).index(st.session_state.scenario))
    if scenario != st.session_state.scenario:
        st.session_state.scenario = scenario
        st.session_state.optimized = False
        st.rerun()

    st.markdown("**Traffic intensity**")
    traffic = st.slider("User traffic", 10, 100, SCENARIOS[scenario]["load"], help="Controls the simulated network load.")
    st.markdown("**Intelligence mode**")
    predictive = st.toggle("Predictive AI", True)
    auto_opt = st.toggle("Auto optimization", False)

    if st.button("🧠 Run Intelligent Optimization", type="primary", use_container_width=True):
        st.session_state.optimized = True
        st.toast("Network optimized successfully!", icon="🧠")

    if st.button("↩ Reset Simulation", use_container_width=True):
        st.session_state.optimized = False
        st.rerun()

    st.divider()
    st.markdown("**Stack**")
    st.caption("Python • NetworkX • Plotly • Streamlit")
    st.caption("Simulation only — no physical 6G hardware required.")

# ---------- Hero ----------
m = current_metrics()
status = "OPTIMIZED" if st.session_state.optimized else (
    "CRITICAL" if m["load"] >= 90 else "STABLE" if m["load"] < 75 else "BUSY"
)
status_class = "status-good" if status=="OPTIMIZED" or status=="STABLE" else "status-bad" if status=="CRITICAL" else "status-warn"

st.markdown("""
<div class="hero">
  <div class="badge">FUTURE NETWORKING • AI • EDGE COMPUTING</div>
  <h1>6G Intelligent Network Simulator</h1>
  <p>Simulate how an intelligent 6G network predicts congestion, allocates resources, reroutes traffic and selects edge resources.</p>
</div>
""", unsafe_allow_html=True)

# ---------- KPI row ----------
cols = st.columns(5)
kpis = [
    ("Network Load", f"{m['load']}%", "Dynamic traffic"),
    ("Avg. Latency", f"{m['latency']:.1f} ms", "End-to-end"),
    ("Packet Loss", f"{m['loss']:.2f}%", "Estimated"),
    ("Throughput", f"{m['throughput']:.0f} Mbps", "Aggregate"),
    ("Network State", status, "Controller status"),
]
for c,(label,value,sub) in zip(cols,kpis):
    c.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="delta">{sub}</div></div>', unsafe_allow_html=True)

# ---------- Topology ----------
st.markdown('<div class="section">Live Network Topology</div>', unsafe_allow_html=True)
left, right = st.columns([1.75,1])
with left:
    st.plotly_chart(topology_fig(), use_container_width=True, config={"displayModeBar":False})
with right:
    ps = path_stats()
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 🧭 Intelligent Route")
    st.markdown(f"**{ps['route']}**")
    st.caption(ps["reason"])
    st.markdown("---")
    if st.session_state.optimized:
        st.markdown('<span class="status-good">● Optimization active</span>', unsafe_allow_html=True)
        st.write("Traffic has been moved away from congested links.")
        st.write("Edge-02 selected for latency-sensitive workloads.")
    else:
        st.markdown('<span class="status-warn">● Baseline routing</span>', unsafe_allow_html=True)
        st.write("Network is using its baseline route.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Allocation ----------
st.markdown('<div class="section">Intelligent Resource Allocation</div>', unsafe_allow_html=True)
apps = ["Autonomous Vehicle", "VR / AR", "Video Streaming", "IoT Sensors", "File Transfer"]
base = np.array([28,25,25,12,10], dtype=float)
if m["load"] > 80:
    if st.session_state.optimized:
        alloc = np.array([31,28,19,12,10], dtype=float)
    else:
        alloc = np.array([22,21,27,14,16], dtype=float)
else:
    alloc = base
alloc_df = pd.DataFrame({"Application":apps, "Bandwidth Share (%)":alloc})
fig = go.Figure(go.Bar(
    x=alloc_df["Application"], y=alloc_df["Bandwidth Share (%)"],
    text=[f"{x:.0f}%" for x in alloc], textposition="outside"
))
fig.update_layout(height=330, margin=dict(l=5,r=5,t=15,b=5),
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                  yaxis=dict(title="Share of allocated bandwidth (%)", gridcolor="rgba(255,255,255,.08)"),
                  xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                  font=dict(color="#dfe6ff"))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ---------- AI prediction ----------
st.markdown('<div class="section">🔮 Predictive Network Intelligence</div>', unsafe_allow_html=True)
hist_x = np.arange(12)
base_load = np.array([42,45,49,53,58,62,67,71,76,80,84,89], dtype=float)
if st.session_state.scenario == "Normal Traffic":
    base_load -= 12
elif st.session_state.scenario == "Massive Congestion":
    base_load += 4
pred = min(99, base_load[-1] + (6 if predictive else 0))
pred_df = pd.DataFrame({"Window":list(range(1,13)), "Observed Load":base_load})
future_df = pd.DataFrame({"Window":[13,14,15], "Predicted Load":[min(99,base_load[-1]+3), min(99,base_load[-1]+6), pred]})
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=pred_df["Window"], y=pred_df["Observed Load"], mode="lines+markers", name="Observed"))
fig2.add_trace(go.Scatter(x=future_df["Window"], y=future_df["Predicted Load"], mode="lines+markers", name="Predicted", line=dict(dash="dash")))
fig2.update_layout(height=310, margin=dict(l=5,r=5,t=15,b=5),
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                   yaxis=dict(title="Network load (%)", gridcolor="rgba(255,255,255,.08)"),
                   xaxis=dict(title="Time window", gridcolor="rgba(0,0,0,0)"),
                   font=dict(color="#dfe6ff"))
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

c1,c2,c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-card"><b>Prediction</b><br><span class="small">Next-window congestion probability</span><h2 style="margin:6px 0">{}%</h2></div>'.format(min(99,int(pred))), unsafe_allow_html=True)
with c2:
    decision = "Reroute + protect latency traffic" if pred >= 80 else "Maintain current routing"
    st.markdown(f'<div class="info-card"><b>Recommended action</b><br><span class="small">Controller decision</span><h4 style="margin:8px 0">{decision}</h4></div>', unsafe_allow_html=True)
with c3:
    edge = "Edge-02" if st.session_state.optimized else "Edge-01"
    st.markdown(f'<div class="info-card"><b>Edge selection</b><br><span class="small">Preferred processing node</span><h2 style="margin:6px 0">{edge}</h2></div>', unsafe_allow_html=True)

# ---------- Comparison ----------
st.markdown('<div class="section">Before vs After Intelligent Optimization</div>', unsafe_allow_html=True)
scenario_raw = SCENARIOS[st.session_state.scenario]
after = current_metrics()
comparison = pd.DataFrame({
    "Metric": ["Latency (ms)", "Packet Loss (%)", "Throughput (Mbps)", "Network Load (%)"],
    "Baseline": [scenario_raw["latency"], scenario_raw["loss"], scenario_raw["throughput"], scenario_raw["load"]],
    "Intelligent": [after["latency"], after["loss"], after["throughput"], after["load"]]
})
st.dataframe(comparison, use_container_width=True, hide_index=True)

st.markdown(
    f'<div class="small" style="text-align:center;margin-top:24px">'
    f'6G Intelligent Network Simulator • Simulation timestamp: {datetime.now().strftime("%d %b %Y, %H:%M:%S")}'
    f'</div>', unsafe_allow_html=True
)
