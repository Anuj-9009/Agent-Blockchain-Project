# Agent-Driven Blockchain Voting System 🗳️🤖

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

A secure and autonomous digital voting platform that integrates SHA-256 blockchain technology with AI-driven agents. This system uses LLMs (OpenAI/Anthropic) to monitor, validate, and self-heal blockchain transactions in real-time.

![Demo GIF](https://via.placeholder.com/800x400.png?text=Insert+Architecture+Diagram+Here)

## ✨ Core Agents
* **The Consensus Agent:** Intelligently validates transactions, checking for semantic anomalies or unusual voting patterns before appending blocks.
* **The Auditor Agent:** Constantly monitors the blockchain for integrity breaches or 51% attack vectors.
* **The Self-Healing Mechanism:** If the Auditor detects a tampered block, the system autonomously forks and rolls back to the last known secure state using LLM-guided recovery protocols.

## 🏗️ Architecture
The project merges standard cryptographic data structures with modern Agentic AI workflows:
1. **The Chain:** A standard Linked List of Blocks, hashed via SHA-256.
2. **The Mempool:** Unconfirmed votes sit in a queue.
3. **The AI Layer:** Before the traditional Proof-of-Work / Consensus algorithm runs, the Mempool data is fed into an LLM via structured JSON to analyze the integrity of the data. 

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* OpenAI API Key (or Anthropic)

### Installation
```bash
git clone https://github.com/Anuj-9009/Agent-Blockchain-Project.git
cd Agent-Blockchain-Project
pip install -r requirements.txt
```

### Running the Node
```bash
export OPENAI_API_KEY="your-key-here"
python main.py
```
