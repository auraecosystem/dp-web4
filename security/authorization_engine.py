# ==========================================================
# authorization_engine.py
# ==========================================================

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Callable
import secrets
import hashlib

# ----------------------------------------------------------
# SESSION
# ----------------------------------------------------------

@dataclass
class Session:

    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    metadata: dict = field(default_factory=dict)

    def expired(self):

        return datetime.utcnow() >= self.expires_at


# ----------------------------------------------------------
# DELEGATION
# ----------------------------------------------------------

@dataclass
class Delegation:

    delegator: str
    delegate: str
    permissions: Set[str]
    expires_at: datetime

    def valid(self):

        return datetime.utcnow() < self.expires_at


# ----------------------------------------------------------
# ROLE INHERITANCE
# ----------------------------------------------------------

class RoleHierarchy:

    def __init__(self):

        self.roles = {}

    def add(self, role):

        self.roles[role.name] = role

    def permissions(self, role_name):

        visited = set()

        perms = set()

        def walk(name):

            if name in visited:
                return

            visited.add(name)

            role = self.roles.get(name)

            if not role:
                return

            perms.update(role.permissions)

            for parent in role.inherits:
                walk(parent)

        walk(role_name)

        return perms


# ----------------------------------------------------------
# CACHE
# ----------------------------------------------------------

class AuthorizationCache:

    def __init__(self):

        self.cache = {}

    def make_key(self, user, permission, resource):

        raw = f"{user}:{permission}:{resource}"

        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, user, permission, resource):

        return self.cache.get(
            self.make_key(user, permission, resource)
        )

    def put(self, user, permission, resource, result):

        self.cache[
            self.make_key(user, permission, resource)
        ] = result

    def clear(self):

        self.cache.clear()


# ----------------------------------------------------------
# SESSION MANAGER
# ----------------------------------------------------------

class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create(self, user_id, ttl_minutes=60):

        sid = secrets.token_hex(32)

        session = Session(
            session_id=sid,
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes),
        )

        self.sessions[sid] = session

        return session

    def validate(self, sid):

        session = self.sessions.get(sid)

        if not session:
            return False

        return not session.expired()

    def revoke(self, sid):

        self.sessions.pop(sid, None)


# ----------------------------------------------------------
# DELEGATION MANAGER
# ----------------------------------------------------------

class DelegationManager:

    def __init__(self):

        self.records = []

    def delegate(

        self,
        owner,
        delegate,
        permissions,
        hours=12,

    ):

        self.records.append(

            Delegation(
                delegator=owner,
                delegate=delegate,
                permissions=set(permissions),
                expires_at=datetime.utcnow() + timedelta(hours=hours),
            )

        )

    def check(

        self,
        delegate,
        permission,

    ):

        for d in self.records:

            if d.delegate != delegate:
                continue

            if not d.valid():
                continue

            if permission in d.permissions:
                return True

        return False


# ----------------------------------------------------------
# EVENT BUS
# ----------------------------------------------------------

class AuthorizationEvents:

    def __init__(self):

        self.before = []

        self.after = []

    def before_authorize(self, func):

        self.before.append(func)

    def after_authorize(self, func):

        self.after.append(func)

    def run_before(self, *args):

        for fn in self.before:
            fn(*args)

    def run_after(self, *args):

        for fn in self.after:
            fn(*args)


# ----------------------------------------------------------
# ZERO TRUST POLICY
# ----------------------------------------------------------

class ZeroTrustPolicy(Policy):

    def evaluate(

        self,
        user,
        permission,
        resource,

    ):

        if not user.active:

            return Decision.DENY

        risk = user.attributes.get("risk", 0)

        if risk > 70:

            return Decision.DENY

        return Decision.ABSTAIN


# ----------------------------------------------------------
# MFA POLICY
# ----------------------------------------------------------

class MFAPolicy(Policy):

    def evaluate(

        self,
        user,
        permission,
        resource,

    ):

        if permission.name.startswith("admin"):

            if not user.attributes.get("mfa", False):

                return Decision.DENY

        return Decision.ABSTAIN


# ----------------------------------------------------------
# RATE LIMIT POLICY
# ----------------------------------------------------------

class RateLimitPolicy(Policy):

    def __init__(self):

        self.counter = {}

    def evaluate(

        self,
        user,
        permission,
        resource,

    ):

        value = self.counter.get(user.id, 0)

        value += 1

        self.counter[user.id] = value

        if value > 100:

            return Decision.DENY

        return Decision.ABSTAIN
