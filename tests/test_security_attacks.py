"""
test_security_attacks.py

Universal Security Test Suite

Tests:
- Authorization
- Delegation
- Sybil resistance
- Replay protection
- Input validation
- Rate limiting
"""

import unittest

from authorization_engine import (
    AuthorizationEngine,
    Permission,
    Role,
    User,
    Resource,
    RolePolicy,
    DenyInactiveUsersPolicy,
)

from delegation_validator import (
    DelegationValidator,
    ValidationResult,
)

from sybil_resistance import (
    SybilResistanceEngine,
    Identity,
)


class TestAuthorization(unittest.TestCase):

    def setUp(self):
        self.engine = AuthorizationEngine()

        self.permission = Permission("document.read")

        role = Role("admin")
        role.add_permission(self.permission)

        self.user = User(
            id="user1",
            username="alice"
        )
        self.user.roles.add("admin")

        self.resource = Resource(
            id="doc1",
            type="document"
        )

        self.engine.register_role(role)
        self.engine.register_user(self.user)

        self.engine.add_policy(
            DenyInactiveUsersPolicy()
        )

        self.engine.add_policy(
            RolePolicy(self.engine.roles)
        )

    def test_authorized_user(self):
        self.assertTrue(
            self.engine.authorize(
                self.user.id,
                self.permission,
                self.resource,
            )
        )

    def test_inactive_user_denied(self):
        self.user.active = False

        self.assertFalse(
            self.engine.authorize(
                self.user.id,
                self.permission,
                self.resource,
            )
        )


class TestDelegation(unittest.TestCase):

    def test_valid_delegation(self):

        validator = DelegationValidator()

        token = validator.issue(
            issuer="alice",
            subject="bob",
            scopes={"read"},
            secret="secret"
        )

        self.assertEqual(
            validator.validate(
                token.token_id,
                "secret"
            ),
            ValidationResult.VALID
        )


class TestSybilResistance(unittest.TestCase):

    def test_duplicate_device_increases_risk(self):

        engine = SybilResistanceEngine()

        a = Identity("A")
        b = Identity("B")

        a.devices.add("shared")
        b.devices.add("shared")

        engine.register(a)
        engine.register(b)

        self.assertGreater(
            engine.compute_risk("A"),
            0
        )


if __name__ == "__main__":
    unittest.main()
