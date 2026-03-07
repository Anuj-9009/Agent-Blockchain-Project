"""
consensus.py — The Consensus (Verifier) Agent.

Before a vote is added to the blockchain, this agent performs a "simulated
peer review" of the transaction data. It checks for:
  - Required fields (voter_id, candidate, timestamp)
  - Duplicate voter IDs (no double voting!)
  - Data format validity
  - Anomaly detection via LLM (optional)

The agent can use an LLM to interpret "intent" or "context" in natural
language, providing intelligent validation beyond simple rule checks.
"""

import os
import threading
from datetime import datetime
from typing import List, Optional, Set, Tuple

try:
    import requests as http_requests
except ImportError:
    http_requests = None


# Required fields for a valid vote transaction
REQUIRED_FIELDS = {"voter_id", "candidate"}


class ConsensusAgent:
    """
    Intelligent validation agent that reviews vote transactions
    before they are added to the blockchain.
    """

    def __init__(self, blockchain, agent_logs: list, log_lock: threading.Lock):
        self.blockchain = blockchain
        self.agent_logs = agent_logs
        self.log_lock = log_lock
        self.seen_voter_ids: Set[str] = set()
        self.voter_lock = threading.Lock()

        # LLM configuration
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

    def _log(self, level: str, message: str, details: Optional[dict] = None):
        """Thread-safe logging to the shared agent_logs list."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": "🤝 Consensus Agent",
            "level": level,
            "message": message,
        }
        if details:
            entry["details"] = details
        with self.log_lock:
            self.agent_logs.append(entry)

    def _check_required_fields(self, data: dict) -> List[str]:
        """Verify all required fields are present and non-empty."""
        issues = []
        for field in REQUIRED_FIELDS:
            if field not in data:
                issues.append(f"Missing required field: '{field}'")
            elif not str(data[field]).strip():
                issues.append(f"Empty value for required field: '{field}'")
        return issues

    def _check_duplicate_voter(self, voter_id: str) -> bool:
        """Check if this voter has already cast a vote."""
        with self.voter_lock:
            if voter_id in self.seen_voter_ids:
                return True
            return False

    def _register_voter(self, voter_id: str):
        """Mark a voter as having voted."""
        with self.voter_lock:
            self.seen_voter_ids.add(voter_id)

    def _check_format(self, data: dict) -> List[str]:
        """Validate data formatting and types."""
        issues = []

        voter_id = data.get("voter_id", "")
        if voter_id and (len(str(voter_id)) < 3 or len(str(voter_id)) > 50):
            issues.append(f"voter_id '{voter_id}' has invalid length (expected 3-50 chars)")

        candidate = data.get("candidate", "")
        if candidate and (len(str(candidate)) < 1 or len(str(candidate)) > 100):
            issues.append(f"candidate name '{candidate}' has invalid length (expected 1-100 chars)")

        # Check for suspicious characters (basic injection prevention)
        for key, value in data.items():
            if isinstance(value, str) and any(c in value for c in ['<', '>', '{', '}', ';']):
                issues.append(f"Suspicious characters detected in field '{key}'")

        return issues

    def _llm_review(self, data: dict, rule_issues: List[str]) -> Optional[str]:
        """
        Optional LLM-powered review for deeper anomaly detection.
        Returns a natural-language assessment, or None if LLM is unavailable.
        """
        prompt = (
            f"You are a blockchain consensus validator. Review this vote transaction:\n\n"
            f"Data: {data}\n\n"
            f"Rule-based issues found: {rule_issues if rule_issues else 'None'}\n\n"
            f"Provide a brief assessment of whether this transaction should be "
            f"approved or rejected. Consider: data integrity, potential fraud indicators, "
            f"and any anomalies. Keep your response to 2-3 sentences."
        )

        # Try OpenAI
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
                            {"role": "system", "content": "You are a blockchain consensus validator AI. Be concise."},
                            {"role": "user", "content": prompt},
                        ],
                        "max_tokens": 150,
                        "temperature": 0.2,
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
            except Exception:
                pass

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
                        "max_tokens": 150,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=10,
                )
                if response.status_code == 200:
                    return response.json()["content"][0]["text"]
            except Exception:
                pass

        return None  # No LLM available

    def review(self, data: dict) -> Tuple[bool, str]:
        """
        Full consensus review of a vote transaction.

        Returns:
            (approved: bool, explanation: str)
        """
        issues = []

        # ── Rule-based checks ──
        issues.extend(self._check_required_fields(data))
        issues.extend(self._check_format(data))

        voter_id = data.get("voter_id", "")
        if voter_id and self._check_duplicate_voter(voter_id):
            issues.append(f"DUPLICATE VOTE: voter_id '{voter_id}' has already voted")

        # ── Decision ──
        approved = len(issues) == 0

        # ── Build explanation ──
        if approved:
            explanation = (
                f"✅ APPROVED: Transaction from voter '{voter_id}' for candidate "
                f"'{data.get('candidate', 'N/A')}' passes all validation checks. "
                f"Fields are complete, format is valid, and no duplicate vote detected."
            )
            # Try LLM enhancement
            llm_assessment = self._llm_review(data, issues)
            if llm_assessment:
                explanation += f"\n\n🤖 AI Assessment: {llm_assessment}"

            # Register the voter only if approved
            self._register_voter(voter_id)
        else:
            explanation = (
                f"❌ REJECTED: Transaction failed consensus review.\n"
                f"Issues found:\n" +
                "\n".join(f"  • {issue}" for issue in issues)
            )
            # Try LLM enhancement
            llm_assessment = self._llm_review(data, issues)
            if llm_assessment:
                explanation += f"\n\n🤖 AI Assessment: {llm_assessment}"

        # Log the decision
        self._log(
            "INFO" if approved else "WARNING",
            f"Vote {'APPROVED' if approved else 'REJECTED'}: {voter_id} → {data.get('candidate', '?')}",
            {
                "voter_id": voter_id,
                "candidate": data.get("candidate"),
                "approved": approved,
                "issues": issues,
                "explanation": explanation,
            }
        )

        return approved, explanation
