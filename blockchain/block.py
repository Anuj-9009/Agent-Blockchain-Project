"""
block.py — The fundamental building block of the blockchain.

Each Block contains:
  - An index (position in the chain)
  - A timestamp (when the block was mined)
  - Transaction data (vote information)
  - The hash of the previous block (cryptographic link)
  - A nonce (Proof-of-Work counter)
  - Its own SHA-256 hash
"""

import hashlib
import json
import time
from typing import Optional


class Block:
    """Represents a single block in the blockchain."""

    def __init__(self, index: int, data: dict, previous_hash: str, timestamp: Optional[float] = None, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Generate the SHA-256 hash of this block's contents.
        The hash is deterministic — the same inputs always produce the same output.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int = 2) -> None:
        """
        Proof-of-Work: increment the nonce until the hash starts with
        `difficulty` number of leading zeros.

        This simulates the computational effort required to add a block,
        making it expensive to tamper with the chain.
        """
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> dict:
        """Serialize the block to a dictionary for JSON responses."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, hash={self.hash[:12]}..., "
            f"prev={self.previous_hash[:12]}...)"
        )
