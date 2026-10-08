# 📡 6G Intelligent Network Simulator

A polished educational prototype that simulates how a future intelligent 6G network can dynamically manage traffic.

## Features

- Interactive 6G network topology
- Multiple traffic scenarios
- Intelligent bandwidth allocation
- Dynamic route selection
- Edge-computing selection
- Predictive congestion visualization
- Before/after optimization comparison
- Dark futuristic dashboard UI
- No physical 6G hardware required

## Run locally

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit.

## Project concept

The simulator models a future 6G environment with users, base stations, routers, edge servers and a cloud. The intelligent controller uses simulated network metrics to decide how resources should be allocated and how traffic should be routed.

This is a simulation/academic prototype, not a physical 6G implementation.

## Suggested project title

**AI-Driven Intelligent 6G Network Simulator for Dynamic Resource Allocation, Adaptive Routing and Edge Computing**

## Suggested future extensions

1. Replace the rule-based intelligence with a trained ML congestion predictor.
2. Connect the topology to NS-3 or Mininet.
3. Add reinforcement learning for routing/resource allocation.
4. Add network slicing.
5. Add federated learning or distributed AI.
6. Add mobility and handover simulation.
7. Add energy-aware resource allocation.
