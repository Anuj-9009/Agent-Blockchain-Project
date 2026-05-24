"""
app.py — Flask Web Server & Agent-Driven Blockchain Dashboard.

This is the main entry point. It:
  1. Initializes the Blockchain
  2. Starts the Auditor Agent (background thread)
  3. Creates the Consensus Agent
  4. Serves the Dashboard UI and API endpoints
"""

import threading
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

from blockchain.chain import Blockchain
from agents.auditor import AuditorAgent
from agents.consensus import ConsensusAgent

# ═══════════════════════════════════════════════
#  Initialize Core Components
# ═══════════════════════════════════════════════

app = Flask(__name__)

# Shared state
blockchain = Blockchain(difficulty=2)
agent_logs = []
log_lock = threading.Lock()

# Initialize agents
auditor = AuditorAgent(blockchain, agent_logs, log_lock, poll_interval=5.0, auto_heal=True)
consensus = ConsensusAgent(blockchain, agent_logs, log_lock)

# ═══════════════════════════════════════════════
#  Dashboard HTML Template
# ═══════════════════════════════════════════════

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent-Driven Blockchain Voting System</title>
    <meta name="description" content="An intelligent blockchain voting system powered by autonomous AI agents for auditing, consensus, and self-healing.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #06090f;
            --bg-secondary: #0c1018;
            --bg-card: rgba(12, 18, 28, 0.85);
            --bg-glass: rgba(255, 255, 255, 0.025);
            --bg-glass-hover: rgba(255, 255, 255, 0.04);
            --border: rgba(255, 255, 255, 0.06);
            --border-hover: rgba(56, 189, 248, 0.2);
            --text-primary: #e8edf5;
            --text-secondary: #8b99b0;
            --text-muted: #556275;
            --accent-sky: #38bdf8;
            --accent-teal: #2dd4bf;
            --accent-green: #4ade80;
            --accent-red: #f87171;
            --accent-yellow: #facc15;
            --accent-blue: #60a5fa;
            --gradient-primary: linear-gradient(135deg, #0ea5e9 0%, #2dd4bf 100%);
            --gradient-success: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
            --gradient-danger: linear-gradient(135deg, #f87171 0%, #dc2626 100%);
            --shadow-glow: 0 0 30px rgba(56, 189, 248, 0.1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Subtle animated background mesh */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse at 15% 10%, rgba(14, 165, 233, 0.06) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 90%, rgba(45, 212, 191, 0.04) 0%, transparent 55%);
            pointer-events: none;
            z-index: 0;
            animation: meshShift 12s ease-in-out infinite alternate;
        }

        @keyframes meshShift {
            0% { opacity: 1; }
            100% { opacity: 0.6; }
        }

        /* ── HEADER ── */
        .header {
            position: relative;
            z-index: 1;
            padding: 1.5rem 3rem;
            border-bottom: 1px solid var(--border);
            backdrop-filter: blur(24px);
            background: rgba(6, 9, 15, 0.85);
        }

        .header-content {
            max-width: 1440px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .header-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .header-title .logo {
            width: 36px; height: 36px;
            border-radius: 10px;
            background: var(--gradient-primary);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
            box-shadow: 0 4px 16px rgba(14, 165, 233, 0.25);
        }

        .header h1 {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        .header h1 span {
            font-weight: 400;
            color: var(--text-secondary);
        }

        .header-stats {
            display: flex;
            gap: 0.75rem;
        }

        .stat-chip {
            padding: 0.35rem 0.85rem;
            border-radius: 100px;
            font-size: 0.72rem;
            font-weight: 500;
            border: 1px solid var(--border);
            background: var(--bg-glass);
            display: flex;
            align-items: center;
            gap: 0.45rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
        }

        .stat-chip .dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            animation: pulse 2.5s infinite;
        }

        .dot-green { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
        .dot-sky { background: var(--accent-sky); box-shadow: 0 0 6px var(--accent-sky); }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.35; transform: scale(0.85); }
        }

        /* ── MAIN LAYOUT ── */
        .main {
            position: relative;
            z-index: 1;
            max-width: 1440px;
            margin: 0 auto;
            padding: 1.5rem 3rem 3rem;
            display: grid;
            grid-template-columns: 1fr 420px;
            gap: 1.5rem;
        }

        /* ── CARDS ── */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            backdrop-filter: blur(20px);
            overflow: hidden;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            border-color: var(--border-hover);
            box-shadow: var(--shadow-glow);
        }

        .card-header {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header h2 {
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
        }

        .card-body { padding: 1.25rem; }

        /* ── MINE FORM ── */
        .mine-form { margin-bottom: 1.5rem; }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .form-group { display: flex; flex-direction: column; gap: 0.3rem; }

        .form-group label {
            font-size: 0.68rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
        }

        .form-group input {
            padding: 0.65rem 0.9rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: rgba(0, 0, 0, 0.25);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            outline: none;
            transition: border-color 0.25s, box-shadow 0.25s;
        }

        .form-group input:focus {
            border-color: var(--accent-sky);
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1);
        }

        .form-group input::placeholder { color: var(--text-muted); }

        /* ── BUTTONS ── */
        .btn {
            padding: 0.65rem 1.4rem;
            border-radius: 8px;
            border: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .btn:active { transform: scale(0.97); }

        .btn-primary {
            background: var(--gradient-primary);
            color: #021a22;
        }

        .btn-primary:hover {
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3);
            transform: translateY(-1px);
        }

        .btn-danger {
            background: var(--gradient-danger);
            color: white;
            font-size: 0.7rem;
            padding: 0.35rem 0.7rem;
            border-radius: 6px;
        }

        .btn-danger:hover {
            box-shadow: 0 6px 20px rgba(248, 113, 113, 0.25);
            transform: translateY(-1px);
        }

        .btn-sm {
            padding: 0.35rem 0.7rem;
            font-size: 0.7rem;
            border-radius: 6px;
        }

        /* ── BLOCKCHAIN BLOCKS ── */
        .block-list {
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        .block-item {
            background: var(--bg-glass);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            transition: all 0.25s;
            position: relative;
        }

        .block-item::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 3px;
            height: 100%;
            border-radius: 10px 0 0 10px;
            background: var(--accent-teal);
            opacity: 0.5;
        }

        .block-item:hover {
            border-color: rgba(255, 255, 255, 0.08);
            background: var(--bg-glass-hover);
        }

        .block-item.invalid {
            border-color: rgba(248, 113, 113, 0.25);
            background: rgba(248, 113, 113, 0.04);
        }

        .block-item.invalid::before { background: var(--accent-red); }

        .block-item.genesis {
            border-color: rgba(56, 189, 248, 0.2);
            background: rgba(56, 189, 248, 0.03);
        }

        .block-item.genesis::before { background: var(--accent-sky); }

        .block-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .block-index {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-sky);
            font-family: 'JetBrains Mono', monospace;
        }

        .block-status {
            font-size: 0.62rem;
            font-weight: 600;
            padding: 0.18rem 0.55rem;
            border-radius: 100px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .status-valid { background: rgba(74, 222, 128, 0.1); color: var(--accent-green); }
        .status-invalid { background: rgba(248, 113, 113, 0.1); color: var(--accent-red); }
        .status-genesis { background: rgba(56, 189, 248, 0.1); color: var(--accent-sky); }

        .block-hash {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.64rem;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            word-break: break-all;
        }

        .block-data {
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-bottom: 0.4rem;
            line-height: 1.5;
        }

        .block-data strong { color: var(--text-primary); font-weight: 600; }

        .block-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.4rem;
        }

        /* ── AGENT LOGS PANEL ── */
        .logs-panel {
            height: calc(100vh - 160px);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .log-list {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
            padding: 0.9rem 1.1rem;
        }

        .log-list::-webkit-scrollbar { width: 3px; }
        .log-list::-webkit-scrollbar-track { background: transparent; }
        .log-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }

        .log-item {
            padding: 0.7rem 0.9rem;
            border-radius: 8px;
            background: var(--bg-glass);
            border: 1px solid var(--border);
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .log-item.log-critical {
            border-color: rgba(248, 113, 113, 0.25);
            background: rgba(248, 113, 113, 0.04);
            border-left: 3px solid var(--accent-red);
        }

        .log-item.log-warning {
            border-color: rgba(250, 204, 21, 0.2);
            background: rgba(250, 204, 21, 0.03);
            border-left: 3px solid var(--accent-yellow);
        }

        .log-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.35rem;
        }

        .log-agent {
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--accent-teal);
        }

        .log-time {
            font-size: 0.6rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        .log-message {
            font-size: 0.75rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .log-details {
            margin-top: 0.4rem;
            padding: 0.5rem 0.7rem;
            border-radius: 6px;
            background: rgba(0, 0, 0, 0.35);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.64rem;
            color: var(--text-muted);
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 140px;
            overflow-y: auto;
            line-height: 1.6;
        }

        /* ── TOAST ── */
        .toast {
            position: fixed;
            bottom: 1.5rem;
            right: 1.5rem;
            padding: 0.85rem 1.25rem;
            border-radius: 10px;
            font-size: 0.82rem;
            font-weight: 500;
            z-index: 1000;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            backdrop-filter: blur(20px);
            max-width: 420px;
        }

        .toast.show { transform: translateY(0); opacity: 1; }

        .toast-success {
            background: rgba(74, 222, 128, 0.12);
            border: 1px solid rgba(74, 222, 128, 0.25);
            color: var(--accent-green);
        }

        .toast-error {
            background: rgba(248, 113, 113, 0.12);
            border: 1px solid rgba(248, 113, 113, 0.25);
            color: var(--accent-red);
        }

        .toast-info {
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.25);
            color: var(--accent-sky);
        }

        .empty-state {
            text-align: center;
            padding: 2.5rem;
            color: var(--text-muted);
            font-size: 0.82rem;
        }

        .empty-state span {
            font-size: 1.8rem;
            display: block;
            margin-bottom: 0.5rem;
            opacity: 0.6;
        }

        /* ── RESPONSIVE ── */
        @media (max-width: 960px) {
            .main {
                grid-template-columns: 1fr;
                padding: 1rem;
            }
            .header { padding: 1.2rem 1.5rem; }
            .header-content { flex-direction: column; gap: 0.75rem; }
            .logs-panel { height: auto; max-height: 60vh; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-title">
                <div class="logo">⛓</div>
                <h1>Blockchain <span>Voting System</span></h1>
            </div>
            <div class="header-stats">
                <div class="stat-chip"><span class="dot dot-green"></span> Chain: <span id="chainLength">{{ chain_length }}</span> blocks</div>
                <div class="stat-chip"><span class="dot dot-sky"></span> Auditor: Active</div>
                <div class="stat-chip"><span class="dot dot-green"></span> Consensus: Ready</div>
            </div>
        </div>
    </header>

    <main class="main">
        <!-- Left: Blockchain Ledger -->
        <div>
            <!-- Mine Form -->
            <div class="card mine-form">
                <div class="card-header">
                    <h2>⛏️ Cast a Vote</h2>
                </div>
                <div class="card-body">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="voterId">Voter ID</label>
                            <input type="text" id="voterId" placeholder="e.g. VOTER-001">
                        </div>
                        <div class="form-group">
                            <label for="candidate">Candidate</label>
                            <input type="text" id="candidate" placeholder="e.g. Alice Johnson">
                        </div>
                    </div>
                    <button class="btn btn-primary" id="mineBtn" onclick="mineBlock()">
                        ⛏️ Mine & Record Vote
                    </button>
                </div>
            </div>

            <!-- Chain -->
            <div class="card">
                <div class="card-header">
                    <h2>📦 Blockchain Ledger</h2>
                    <button class="btn btn-sm btn-primary" onclick="refreshChain()">↻ Refresh</button>
                </div>
                <div class="card-body">
                    <div class="block-list" id="blockList">
                        <!-- Blocks populated by JS -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Right: Agent Logs -->
        <div class="card logs-panel">
            <div class="card-header">
                <h2>🤖 Agent Logs</h2>
                <span class="stat-chip" style="font-size:0.65rem;" id="logCount">0 entries</span>
            </div>
            <div class="log-list" id="logList">
                <div class="empty-state" id="logsEmpty">
                    <span>🔍</span>
                    Agents are monitoring the chain.<br>Logs will appear here in real-time.
                </div>
            </div>
        </div>
    </main>

    <div class="toast" id="toast"></div>

    <script>
        // ── State ──
        let currentChain = [];
        let currentLogs = [];

        // ── Toast ──
        function showToast(message, type = 'info') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = `toast toast-${type} show`;
            setTimeout(() => toast.classList.remove('show'), 3500);
        }

        // ── Mine Block ──
        async function mineBlock() {
            const voterId = document.getElementById('voterId').value.trim();
            const candidate = document.getElementById('candidate').value.trim();

            if (!voterId || !candidate) {
                showToast('Please fill in both Voter ID and Candidate', 'error');
                return;
            }

            const btn = document.getElementById('mineBtn');
            btn.disabled = true;
            btn.textContent = '⏳ Mining...';

            try {
                const res = await fetch('/mine', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        voter_id: voterId,
                        candidate: candidate,
                        timestamp: new Date().toISOString()
                    })
                });
                const data = await res.json();

                if (data.success) {
                    showToast(`✅ Block #${data.block.index} mined successfully!`, 'success');
                    document.getElementById('voterId').value = '';
                    document.getElementById('candidate').value = '';
                } else {
                    showToast(`❌ ${data.explanation || data.error}`, 'error');
                }
            } catch (err) {
                showToast('Network error — is the server running?', 'error');
            }

            btn.disabled = false;
            btn.textContent = '⛏️ Mine & Record Vote';
            refreshChain();
            refreshLogs();
        }

        // ── Render Blockchain ──
        function renderChain(chain) {
            const list = document.getElementById('blockList');
            const invalidIndices = new Set();
            for (let i = 1; i < chain.length; i++) {
                if (chain[i].previous_hash !== chain[i - 1].hash) {
                    invalidIndices.add(i);
                }
            }

            list.innerHTML = chain.map((block, i) => {
                const isGenesis = i === 0;
                const isInvalid = invalidIndices.has(i);
                const cls = isGenesis ? 'genesis' : (isInvalid ? 'invalid' : '');
                const statusCls = isGenesis ? 'status-genesis' : (isInvalid ? 'status-invalid' : 'status-valid');
                const statusText = isGenesis ? 'GENESIS' : (isInvalid ? 'TAMPERED' : 'VALID');

                const dataStr = typeof block.data === 'object'
                    ? Object.entries(block.data).map(([k, v]) => `<strong>${k}:</strong> ${v}`).join(' &middot; ')
                    : block.data;

                const tamperBtn = !isGenesis
                    ? `<button class="btn btn-danger" onclick="tamperBlock(${i})">💥 Tamper</button>`
                    : '';

                return `
                    <div class="block-item ${cls}">
                        <div class="block-top">
                            <span class="block-index">Block #${block.index}</span>
                            <span class="block-status ${statusCls}">${statusText}</span>
                        </div>
                        <div class="block-hash">🔗 ${block.hash}</div>
                        <div class="block-data">${dataStr}</div>
                        <div class="block-hash" style="font-size:0.6rem;">← prev: ${block.previous_hash.substring(0, 24)}...</div>
                        <div class="block-actions">${tamperBtn}</div>
                    </div>
                `;
            }).join('');

            document.getElementById('chainLength').textContent = chain.length;
        }

        // ── Render Logs ──
        function renderLogs(logs) {
            const list = document.getElementById('logList');
            const empty = document.getElementById('logsEmpty');

            if (logs.length === 0) {
                empty.style.display = 'block';
                return;
            }
            empty.style.display = 'none';
            document.getElementById('logCount').textContent = `${logs.length} entries`;

            const reversed = [...logs].reverse();
            list.innerHTML = reversed.map(log => {
                const levelCls = log.level === 'CRITICAL' ? 'log-critical' : (log.level === 'WARNING' ? 'log-warning' : '');
                const time = new Date(log.timestamp).toLocaleTimeString();
                const details = log.details
                    ? `<div class="log-details">${formatDetails(log.details)}</div>`
                    : '';
                return `
                    <div class="log-item ${levelCls}">
                        <div class="log-meta">
                            <span class="log-agent">${log.agent}</span>
                            <span class="log-time">${time}</span>
                        </div>
                        <div class="log-message">${log.message}</div>
                        ${details}
                    </div>
                `;
            }).join('');
        }

        function formatDetails(details) {
            if (typeof details === 'string') return details;
            if (details.explanation) return details.explanation;
            return JSON.stringify(details, null, 2);
        }

        // ── Tamper ──
        async function tamperBlock(index) {
            if (!confirm(`⚠️ Tamper with Block #${index}? This will corrupt the block to trigger the Auditor Agent.`)) return;

            try {
                const res = await fetch(`/tamper/${index}`, { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    showToast(`💥 Block #${index} tampered! Watch the Auditor Agent...`, 'error');
                } else {
                    showToast(data.error, 'error');
                }
            } catch (err) {
                showToast('Network error', 'error');
            }

            setTimeout(() => { refreshChain(); refreshLogs(); }, 2000);
        }

        // ── Refresh Data ──
        async function refreshChain() {
            try {
                const res = await fetch('/chain');
                const data = await res.json();
                currentChain = data.chain;
                renderChain(currentChain);
            } catch (err) { /* silent */ }
        }

        async function refreshLogs() {
            try {
                const res = await fetch('/logs');
                const data = await res.json();
                currentLogs = data.logs;
                renderLogs(currentLogs);
            } catch (err) { /* silent */ }
        }

        // ── Initial Load + Auto-refresh ──
        refreshChain();
        refreshLogs();
        setInterval(refreshChain, 4000);
        setInterval(refreshLogs, 3000);
    </script>
</body>
</html>
"""

# ═══════════════════════════════════════════════
#  Routes
# ═══════════════════════════════════════════════

@app.route("/")
def dashboard():
    """Serve the main dashboard UI."""
    return render_template_string(DASHBOARD_TEMPLATE, chain_length=len(blockchain))


@app.route("/chain", methods=["GET"])
def get_chain():
    """Return the full blockchain as JSON."""
    is_valid, errors = blockchain.is_chain_valid()
    return jsonify({
        "chain": blockchain.to_list(),
        "length": len(blockchain),
        "is_valid": is_valid,
        "errors": errors,
    })


@app.route("/mine", methods=["POST"])
def mine_block():
    """
    Submit a vote transaction → Consensus Agent reviews → mine block.
    Expects JSON: { "voter_id": "...", "candidate": "..." }
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No JSON data provided"}), 400

    # ── Consensus Agent reviews the transaction ──
    approved, explanation = consensus.review(data)

    if not approved:
        return jsonify({
            "success": False,
            "error": "Consensus Agent rejected the transaction",
            "explanation": explanation,
        }), 400

    # ── Mine the block ──
    block = blockchain.add_block(data)

    return jsonify({
        "success": True,
        "block": block.to_dict(),
        "consensus": explanation,
        "chain_length": len(blockchain),
    })


@app.route("/tamper/<int:index>", methods=["POST"])
def tamper(index):
    """Deliberately tamper with a block to trigger the Auditor Agent."""
    result = blockchain.tamper_block(index, {
        "voter_id": "HACKED",
        "candidate": "TAMPERED_DATA",
        "message": "This block has been maliciously modified!",
    })

    if result is None:
        return jsonify({"success": False, "error": f"Cannot tamper block {index}"}), 400

    with log_lock:
        agent_logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": "⚠️ System",
            "level": "WARNING",
            "message": f"Block #{index} was deliberately tampered for demonstration",
            "details": result,
        })

    return jsonify({"success": True, "result": result})


@app.route("/logs", methods=["GET"])
def get_logs():
    """Return all agent logs as JSON."""
    with log_lock:
        return jsonify({"logs": list(agent_logs), "count": len(agent_logs)})


@app.route("/health", methods=["GET"])
def health():
    """System health check."""
    is_valid, _ = blockchain.is_chain_valid()
    return jsonify({
        "status": "healthy",
        "blockchain_valid": is_valid,
        "chain_length": len(blockchain),
        "agents": {
            "auditor": "running" if auditor._running else "stopped",
            "consensus": "ready",
        },
    })


# ═══════════════════════════════════════════════
#  Entry Point
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  ⛓️  Agent-Driven Blockchain Voting System")
    print("  🤖 Auditor Agent: Starting...")
    print("  🤝 Consensus Agent: Ready")
    print("  🌐 Dashboard: http://localhost:5001")
    print("=" * 55 + "\n")

    # Start the Auditor Agent background thread
    auditor.start()

    # Run Flask
    app.run(host="0.0.0.0", port=5001, debug=False)
