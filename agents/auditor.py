"""
auditor.py — The Auditor Agent.

A background agent that continuously monitors the blockchain for integrity
violations. When tampering is detected, it uses an LLM (or a local fallback)
to generate a natural-language explanation of what went wrong and why.

Features:
  - Runs on a daemon thread, polling the chain every few seconds
  - Thread-safe logging via threading.Lock
  - Self-healing: can trigger chain revert on tamper detection
  - Graceful LLM fallback — works without any API key
"""

import os
import time
import threading
from datetime import datetime
from typing import List, Optional

# Optional LLM imports — only used if API keys are set
try:
    import requests as http_requests
except ImportError:
    http_requests = None


class AuditorAgent:
    """
    Autonomous agent that audits the blockchain for integrity violations.
    Runs as a background daemon thread.
    """

    def __init__(self, blockchain, agent_logs: list, log_lock: threading.Lock,
                 poll_interval: float = 5.0, auto_heal: bool = True):
        self.blockchain = blockchain
        self.agent_logs = agent_logs
        self.log_lock = log_lock
        self.poll_interval = poll_interval
        self.auto_heal = auto_heal
        self._running = False
        self._thread = None

        # LLM configuration
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

    def _log(self, level: str, message: str, details: Optional[dict] = None):
        """Thread-safe logging to the shared agent_logs list."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": "🔍 Auditor Agent",
            "level": level,
            "message": message,
        }
        if details:
            entry["details"] = details
        with self.log_lock:
            self.agent_logs.append(entry)

    def _generate_llm_explanation(self, errors: List[dict]) -> str:
        """
        Use an LLM to generate a natural-language explanation of the
        blockchain integrity violations.

        Falls back to rule-based explanation if no API key is configured.
        """
        prompt = self._build_prompt(errors)

        # Try OpenAI first
        if self.openai_api_key and http_requests:
            try:
                response = http_requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": (
                                "You are a blockchain security auditor AI. "
                                "Explain blockchain integrity violations clearly "
                                "and concisely for a technical audience. Be specific "
                                "about which blocks are affected and why."
                            )},
                            {"role": "user", "content": prompt},
                        ],
                        "max_tokens": 300,
                        "temperature": 0.3,
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
            except Exception:
                pass  # Fall through to local fallback

        # Try Anthropic
        if self.anthropic_api_key and http_requests:
            try:
                response = http_requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_api_key,
                        "Content-Type": "application/json",
                        "anthropic-version": "2023-06-01",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 300,
                        "messages": [
                            {"role": "user", "content": (
                                "You are a blockchain security auditor AI. "
                                "Explain these blockchain integrity violations clearly:\n\n"
                                + prompt
                            )},
                        ],
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    return response.json()["content"][0]["text"]
            except Exception:
                pass  # Fall through to local fallback

        # ── Local rule-based fallback ──
        return self._local_explanation(errors)

    def _build_prompt(self, errors: List[dict]) -> str:
        """Build a structured prompt describing the detected errors."""
        lines = ["The following integrity violations were detected in the blockchain:\n"]
        for err in errors:
            if err["error_type"] == "hash_mismatch":
                lines.append(
                    f"• Block #{err['block_index']}: Hash mismatch detected. "
                    f"The stored hash no longer matches the recalculated hash. "
                    f"Block data: {err['data']}"
                )
            elif err["error_type"] == "link_broken":
                lines.append(
                    f"• Block #{err['block_index']}: Chain link broken. "
                    f"The previous_hash pointer does not match the preceding block's hash."
                )
        lines.append("\nExplain what likely happened, the security implications, "
                      "and recommend corrective actions.")
        return "\n".join(lines)

    def _local_explanation(self, errors: List[dict]) -> str:
        """
        Intelligent rule-based explanation — no LLM needed.
        This ensures the project works out of the box.
        """
        explanations = []
        for err in errors:
            idx = err["block_index"]
            if err["error_type"] == "hash_mismatch":
                explanations.append(
                    f"⚠️  HASH MISMATCH at Block #{idx}: "
                    f"The data in this block has been modified after mining. "
                    f"The stored hash ({err['stored_hash'][:16]}...) no longer matches "
                    f"the recalculated hash ({err['recalculated_hash'][:16]}...). "
                    f"This is a classic sign of data tampering — someone changed the "
                    f"block's contents without re-mining it. "
                    f"SECURITY IMPLICATION: The integrity of all subsequent blocks "
                    f"in the chain is now compromised."
                )
            elif err["error_type"] == "link_broken":
                explanations.append(
                    f"🔗 CHAIN LINK BROKEN at Block #{idx}: "
                    f"This block's previous_hash pointer does not match the hash "
                    f"of the preceding block. This means either this block or the "
                    f"previous block has been tampered with, breaking the cryptographic "
                    f"chain of custody."
                )

        if self.auto_heal:
            explanations.append(
                "\n🩹 CORRECTIVE ACTION: The self-healing protocol will revert "
                "the chain to its last known valid state, removing all tampered blocks."
            )

        return "\n\n".join(explanations)

    def _audit_cycle(self):
        """Perform one audit cycle: validate chain, report and heal if needed."""
        is_valid, errors = self.blockchain.is_chain_valid()

        if is_valid:
            return  # Chain is healthy, nothing to report

        # Generate explanation
        explanation = self._generate_llm_explanation(errors)

        self._log("CRITICAL", "🚨 BLOCKCHAIN INTEGRITY VIOLATION DETECTED", {
            "violations_found": len(errors),
            "affected_blocks": [e["block_index"] for e in errors],
            "explanation": explanation,
        })

        # Self-healing
        if self.auto_heal:
            removed = self.blockchain.revert_to_valid_state()
            if removed > 0:
                self._log("INFO", f"🩹 Self-healing complete: reverted {removed} block(s)", {
                    "blocks_removed": removed,
                    "chain_length": len(self.blockchain),
                })

    def _run_loop(self):
        """Main daemon loop."""
        self._log("INFO", "Auditor Agent started — monitoring blockchain integrity")
        while self._running:
            try:
                self._audit_cycle()
            except Exception as e:
                self._log("ERROR", f"Audit cycle failed: {str(e)}")
            time.sleep(self.poll_interval)

    def start(self):
        """Start the auditor as a background daemon thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the auditor."""
        self._running = False
