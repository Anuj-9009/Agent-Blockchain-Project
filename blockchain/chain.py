"""
chain.py — Blockchain management logic.

Manages the ordered list of Blocks, including:
  - Genesis block creation
  - Adding new blocks (with Consensus Agent pre-approval)
  - Full chain validation
  - Deliberate tampering (for demo purposes)
  - Self-healing revert to last known good state
"""

import threading
from typing import List, Optional, Tuple
from blockchain.block import Block


class Blockchain:
    """Manages the entire blockchain ledger."""

    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.lock = threading.Lock()
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Create the first block in the chain with no predecessor."""
        genesis = Block(
            index=0,
            data={"message": "Genesis Block — Chain Initialized", "type": "system"},
            previous_hash="0" * 64,
        )
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def get_latest_block(self) -> Block:
        """Return the most recently added block."""
        return self.chain[-1]

    def add_block(self, data: dict) -> Block:
        """
        Mine and append a new block to the chain.

        NOTE: The Consensus Agent should validate `data` BEFORE calling this.
        This method only handles the cryptographic side of block creation.
        """
        with self.lock:
            previous_block = self.get_latest_block()
            new_block = Block(
                index=len(self.chain),
                data=data,
                previous_hash=previous_block.hash,
            )
            new_block.mine(self.difficulty)
            self.chain.append(new_block)
            return new_block

    def is_chain_valid(self) -> Tuple[bool, List[dict]]:
        """
        Walk the entire chain and verify:
          1. Each block's stored hash matches its recalculated hash
          2. Each block's previous_hash matches the prior block's hash

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check 1 — hash integrity
            recalculated = current.calculate_hash()
            if current.hash != recalculated:
                errors.append({
                    "block_index": i,
                    "error_type": "hash_mismatch",
                    "stored_hash": current.hash,
                    "recalculated_hash": recalculated,
                    "data": current.data,
                })

            # Check 2 — chain linkage
            if current.previous_hash != previous.hash:
                errors.append({
                    "block_index": i,
                    "error_type": "link_broken",
                    "expected_previous_hash": previous.hash,
                    "actual_previous_hash": current.previous_hash,
                })

        is_valid = len(errors) == 0
        return is_valid, errors

    def tamper_block(self, index: int, new_data: dict) -> Optional[dict]:
        """
        Deliberately corrupt a block's data WITHOUT re-mining.
        This simulates an attack — the hash will no longer match.

        Used for demo purposes to trigger the Auditor Agent.
        """
        if index <= 0 or index >= len(self.chain):
            return None

        with self.lock:
            block = self.chain[index]
            old_data = block.data
            block.data = new_data
            # Intentionally do NOT recalculate the hash — this is the "tamper"
            return {
                "block_index": index,
                "old_data": old_data,
                "new_data": new_data,
                "hash_before": block.hash,
                "hash_after": block.calculate_hash(),
                "tampered": True,
            }

    def revert_to_valid_state(self) -> int:
        """
        Self-healing protocol: remove all blocks from the first invalid one
        onward, restoring the chain to its last known-good state.

        Returns the number of blocks removed.
        """
        with self.lock:
            removed = 0
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                previous = self.chain[i - 1]
                recalculated = current.calculate_hash()

                if current.hash != recalculated or current.previous_hash != previous.hash:
                    removed = len(self.chain) - i
                    self.chain = self.chain[:i]
                    return removed
            return removed

    def to_list(self) -> List[dict]:
        """Serialize the entire chain to a list of dicts."""
        return [block.to_dict() for block in self.chain]

    def __len__(self) -> int:
        return len(self.chain)
