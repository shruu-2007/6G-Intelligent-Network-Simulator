# Project Report Content — 6G Intelligent Network Simulator

## 1. Abstract

The 6G Intelligent Network Simulator is a software-based simulation platform designed to demonstrate intelligent resource management in future wireless networks. The system models users, base stations, routers, edge servers and cloud resources and dynamically evaluates network conditions such as latency, packet loss, throughput and network load. An intelligent control layer performs resource allocation, adaptive routing and edge-server selection according to application requirements. The simulator also demonstrates predictive congestion analysis, allowing the network to prepare for expected traffic increases. The project provides a practical visualization of how AI-driven network intelligence can improve quality of service in future 6G environments.

## 2. Problem Statement

Future networks will support highly diverse applications such as extended reality, autonomous vehicles, industrial IoT, high-speed multimedia and massive machine communication. These applications have different requirements for latency, bandwidth, reliability and processing. Static resource allocation can therefore cause congestion, inefficient resource utilization and quality-of-service violations.

## 3. Objectives

- Simulate a future 6G network environment.
- Model different application traffic requirements.
- Dynamically allocate network bandwidth.
- Select efficient routes based on network conditions.
- Select suitable edge resources for latency-sensitive workloads.
- Predict possible congestion conditions.
- Compare baseline and intelligent network performance.
- Provide a visual dashboard for analysis.

## 4. Modules

### Module 1 — Network Topology
Creates virtual base stations, routers, core nodes and edge servers.

### Module 2 — Traffic Generator
Represents different application classes such as VR/AR, autonomous vehicles, video streaming and IoT.

### Module 3 — Resource Allocation
Assigns bandwidth based on traffic requirements and priority.

### Module 4 — Adaptive Routing
Selects a better route when a link or router becomes congested.

### Module 5 — Edge Computing
Chooses an edge node for latency-sensitive processing.

### Module 6 — Predictive Intelligence
Analyzes simulated traffic trends and estimates future congestion.

### Module 7 — Visualization
Displays topology, KPIs, predictions and before/after comparisons.

## 5. Expected Outcome

The system should demonstrate that intelligent resource allocation and adaptive routing can reduce simulated latency and packet loss while improving throughput and resource utilization under changing traffic conditions.

## 6. Future Scope

- NS-3 integration
- Mininet/SDN integration
- Reinforcement learning
- Network slicing
- Mobility and handover
- Energy-aware optimization
- Multi-agent network control
- Real-time telemetry
