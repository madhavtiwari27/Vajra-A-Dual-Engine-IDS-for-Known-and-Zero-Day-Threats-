# Vajra: A Dual Engine IDS for Known and Zero Day Threats
**Vajra: A Dual Engine IDS for Known and Zero Day Threats** is a high-performance, real-time Hybrid Intrusion Detection System (H-IDS). By moving away from standalone models that suffer from high false-positive rates and classification bottlenecks, Vajra introduces a parallel, multi-threaded dual-engine architecture. It combines a high-speed **Signature-Based Engine (S-IDS)** using an optimized Decision Tree with a high-precision **Anomaly-Based Engine (A-IDS)** powered by XGBoost and a Genetic Algorithm feature selector.


The system features an interactive, real-time monitoring dashboard built with PyQt5, capable of automated packet sniffing, live feature engineering, sliding-window temporal analysis, and instant security alerting.


## 🚀 Key Architectural Features

### 1. Dual-Engine Hybrid Detection Pipeline

The system implements a non-blocking parallel processing workflow to eliminate classification bottlenecks:

- **Signature-Based IDS (S-IDS):** Processes network packets using a tailored **Decision Tree Classifier** optimized via post-pruning _(max_depth=12, min_samples_leaf=5)_ to resolve legacy classification inconsistencies. It targets fast matching against known attack signatures.
- **Anomaly-Based IDS (A-IDS):** Leverages an **XGBoost Classifier** configured with early stopping and a Genetic Algorithm wrapper for feature reduction. It isolates zero-day behavior by reducing the input to the 19 most impactful behavioral markers.

### 2. Live Packet Ingestion & Temporal Windowing

- Multi-threaded network sniffing powered by _pyshark_ capturing raw streams over live interfaces.
- Stateful parsing of layer-specific contexts using dedicated modules for TCP _(tcp_packet_attributes)_ and UDP _(udp_packet_attributes)_.
- A **60-second sliding history buffer** that calculates packet frequency variations over time to catch volumetric threats (e.g., DoS, Probing) instead of treating packets as isolated events.

### 3. Conflict Resolution & Aggregation Logic

An architectural aggregation pipeline checks the outputs of both engines synchronously. In cases where the anomaly engine flags behavioral deviations but the signature library reports normal traffic, a centralized conflict-resolution routine overrides the pipeline to label the packet as a potential zero-day exploit, maintaining a resilient defensive stance.


## 📈 Validated Empirical Performance

The models have been thoroughly evaluated against combinations of standard network baselines **(UNSW-NB15 and KDD Cup '99)**:

### Anomaly Engine (XGBoost Classifier)

- **Accuracy:** _98.71%_
- **Precision:** _1.0000_
- **Recall:** _0.7210_
- **F1-Score:** _0.8379_

### Signature Engine (Decision Tree Classifier)

- Optimized to handle high-throughput data smoothly, capturing over **98,318 True Positives and 50,040 True Negatives** during validation testing with high classification sensitivity.


## 🛠️ Repository Structure

```
├── ABNIDS.py               # Main application entry point & PyQt5 Dashboard GUI
├── Signature-train-test.py # Standalone evaluation script for the S-IDS Decision Tree
├── classifier.py           # Core machine learning wrappers for prediction & state logging
├── tree.py                 # Genetic Algorithm implementation for optimized feature selection
├── Preprocess.py           # Dataset refinement and continuous scaling pipeline
├── packet.py               # Live network packet parsing (pyshark layer bindings)
└── res/                    # Directory containing model evaluation telemetry and logs
```
