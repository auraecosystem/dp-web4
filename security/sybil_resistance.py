"""
sybil_resistance.py

Universal Sybil Resistance Framework

Features
--------
- Identity reputation scoring
- Device fingerprint correlation
- Wallet clustering
- IP correlation
- Graph-based trust scoring
- Behavioral analysis
- Configurable risk thresholds
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict
import math


# =====================================================
# CONFIG
# =====================================================

@dataclass
class RiskConfiguration:

    sybil_threshold: float = 75.0

    duplicate_device_penalty: float = 25

    duplicate_ip_penalty: float = 20

    wallet_cluster_penalty: float = 15

    reputation_bonus: float = 30

    age_bonus: float = 10


# =====================================================
# IDENTITY
# =====================================================

@dataclass
class Identity:

    identity_id: str

    reputation: float = 50

    created_at: datetime = field(default_factory=datetime.utcnow)

    devices: Set[str] = field(default_factory=set)

    wallets: Set[str] = field(default_factory=set)

    ip_addresses: Set[str] = field(default_factory=set)

    behavior: Dict[str, float] = field(default_factory=dict)


# =====================================================
# TRUST GRAPH
# =====================================================

class TrustGraph:

    def __init__(self):

        self.edges = defaultdict(set)

    def connect(self, a, b):

        self.edges[a].add(b)

        self.edges[b].add(a)

    def neighbors(self, node):

        return self.edges[node]

    def degree(self, node):

        return len(self.edges[node])


# =====================================================
# ENGINE
# =====================================================

class SybilResistanceEngine:

    def __init__(self):

        self.identities = {}

        self.graph = TrustGraph()

        self.config = RiskConfiguration()

    def register(self, identity: Identity):

        self.identities[identity.identity_id] = identity

    def link(self, a, b):

        self.graph.connect(a, b)

    def compute_risk(self, identity_id):

        identity = self.identities[identity_id]

        score = 0

        device_map = defaultdict(int)

        ip_map = defaultdict(int)

        wallet_map = defaultdict(int)

        for other in self.identities.values():

            if other.identity_id == identity.identity_id:
                continue

            for d in identity.devices & other.devices:
                device_map[d] += 1

            for ip in identity.ip_addresses & other.ip_addresses:
                ip_map[ip] += 1

            for w in identity.wallets & other.wallets:
                wallet_map[w] += 1

        score += len(device_map) * self.config.duplicate_device_penalty

        score += len(ip_map) * self.config.duplicate_ip_penalty

        score += len(wallet_map) * self.config.wallet_cluster_penalty

        score -= identity.reputation * 0.25

        age_days = (datetime.utcnow() - identity.created_at).days

        score -= min(age_days / 30, self.config.age_bonus)

        score += self.graph.degree(identity.identity_id)

        return max(score, 0)

    def suspicious(self, identity_id):

        return (
            self.compute_risk(identity_id)
            >= self.config.sybil_threshold
        )

    def report(self):

        reports = {}

        for identity in self.identities:

            reports[identity] = {

                "risk": self.compute_risk(identity),

                "flagged": self.suspicious(identity)

            }

        return reports


# =====================================================
# BEHAVIOR ANALYZER
# =====================================================

class BehaviorAnalyzer:

    @staticmethod
    def similarity(first, second):

        common = (
            set(first.behavior)
            &
            set(second.behavior)
        )

        if not common:

            return 0

        distance = 0

        for key in common:

            distance += abs(

                first.behavior[key]

                -

                second.behavior[key]

            )

        return 1 / (1 + distance)


# =====================================================
# REPUTATION ENGINE
# =====================================================

class ReputationEngine:

    def reward(self, identity, value):

        identity.reputation += value

        identity.reputation = min(identity.reputation, 100)

    def penalize(self, identity, value):

        identity.reputation -= value

        identity.reputation = max(identity.reputation, 0)


# =====================================================
# DEMO
# =====================================================

if __name__ == "__main__":

    engine = SybilResistanceEngine()

    alice = Identity("alice")

    bob = Identity("bob")

    alice.devices.add("device001")

    bob.devices.add("device001")

    alice.wallets.add("walletA")

    bob.wallets.add("walletA")

    alice.ip_addresses.add("192.168.1.2")

    bob.ip_addresses.add("192.168.1.2")

    engine.register(alice)

    engine.register(bob)

    engine.link("alice", "bob")

    print(engine.report())
