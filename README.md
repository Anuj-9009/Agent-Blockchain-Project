# Blockchain Voting System 🗳️⛓️

<p>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Blockchain-Immutability-purple?style=for-the-badge&logo=ethereum&logoColor=white" alt="Blockchain" />
  <img src="https://img.shields.io/badge/AI-Agentic%20Consensus-teal?style=for-the-badge" alt="AI Agents" />
</p>

An autonomous, secure, and decentralized digital voting system powered by standard SHA-256 blockchain technology and AI-driven multi-agent consensus networks. The platform coordinates an **Auditor Agent** for continuous integrity checks and self-healing, alongside a **Consensus Agent** that validates voter identity, flags collusion anomalies, and records immutable blocks.

---

## 🧠 Why Is This Different From a Normal Database?

Standard database systems allow administrators to modify historic records or edit votes at the storage level. This blockchain architecture guarantees zero-trust security:

- **🔐 Cryptographic Chain Links:** Every block stores a SHA-256 hash of its voter payload and the previous block's hash. Editing any historical transaction immediately invalidates the cryptographic signatures of all subsequent blocks.
- **🤖 The "Agentic" Defense:** Multi-agent monitors continuously evaluate the chain's structural health. If a malicious attacker bypasses system security to force an in-memory modification on a node, the **Auditor Agent** instantly detects the hash divergence, runs a majority consensus poll against other nodes, reconstructs the valid ledger from history, and restores the node's state autonomously.

---

## 🏗️ Multi-Agent System Architecture

```
                       ┌────────────────────────────┐
                       │     Vote Transaction       │
                       └─────────────┬──────────────┘
                                     │ (Raw Vote Request)
                                     ▼
                       ┌────────────────────────────┐
                       │      Consensus Agent       │
                       │   (Rules & LLM Anomaly)    │
                       └─────────────┬──────────────┘
                                     │ (Approved Block)
                                     ▼
                       ┌────────────────────────────┐
                       │      Blockchain Core       │
                       │   (SHA-256 Ledger State)   │
                       └─────────────▲──────────────┘
                                     │ (Continuous Polling & Health Audits)
                                     │
                       ┌─────────────┴──────────────┐
                       │       Auditor Agent        │
                       │  (Block Check & Healing)   │
                       └────────────────────────────┘
```

1. **Consensus Agent:**
   - Validates voter registration details and prevents duplicate submissions.
   - Evaluates voting logs using a rule-based algorithm and custom AI modeling to flag colluding voter coordinates or systemic anomalies.
2. **Auditor Agent:**
   - Performs low-overhead hash loop verifications across the blockchain every `5 seconds`.
   - Houses custom self-healing routines to pull validated database states from adjacent distributed consensus nodes when state errors are isolated.

---

## 🚀 Getting Started

### Prerequisites
- **Python** 3.9+ installed on your host computer
- `pip` package manager

### 💻 Installation & Local Test

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Anuj-9009/Agent-Blockchain-Project.git
   cd Agent-Blockchain-Project
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the distributed voting node:**
   ```bash
   python main.py
   ```
   *Note: Open multiple terminal tabs and run the script on different ports (e.g. `python main.py --port 5001`, `python main.py --port 5002`) to verify the multi-node distributed blockchain peer-sync and self-healing features in real-time.*

---

<div align="center" style="margin-top: 40px;">
  <img src="assets/footer-v2.svg" width="100%" alt="footer">
</div>
<p style="font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; color: #8b5cf6; margin: 0; text-align: center;">
  built by ANUJ with ❤️ while pink floyd's 'Time' echoed in the background
</p>
