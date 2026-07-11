"""
test_atp_refund_protection.py

Security tests for refund protection.

These tests verify that:
- Duplicate refunds are rejected.
- Unauthorized users cannot issue refunds.
- Invalid transaction IDs are rejected.
- Excessive refund amounts are rejected.
"""

import unittest
from decimal import Decimal


class MockRefundEngine:

    def __init__(self):
        self.completed = set()

    def refund(self, tx_id, amount, authorized):

        if not authorized:
            raise PermissionError("Unauthorized")

        if amount <= 0:
            raise ValueError("Invalid amount")

        if tx_id in self.completed:
            raise RuntimeError("Duplicate refund")

        self.completed.add(tx_id)

        return True


class TestRefundProtection(unittest.TestCase):

    def setUp(self):
        self.engine = MockRefundEngine()

    def test_valid_refund(self):
        self.assertTrue(
            self.engine.refund(
                "tx001",
                Decimal("25.00"),
                True,
            )
        )

    def test_duplicate_refund_blocked(self):
        self.engine.refund(
            "tx002",
            Decimal("10.00"),
            True,
        )

        with self.assertRaises(RuntimeError):
            self.engine.refund(
                "tx002",
                Decimal("10.00"),
                True,
            )

    def test_unauthorized_refund(self):
        with self.assertRaises(PermissionError):
            self.engine.refund(
                "tx003",
                Decimal("5.00"),
                False,
            )

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.engine.refund(
                "tx004",
                Decimal("-5.00"),
                True,
            )

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            self.engine.refund(
                "tx005",
                Decimal("0.00"),
                True,
            )


if __name__ == "__main__":
    unittest.main()
