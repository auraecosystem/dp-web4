-- =====================================================
-- Universal Reputation Washing Detection Schema
-- Version: 1.0
-- =====================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

---------------------------------------------------------
-- ENTITIES
---------------------------------------------------------

CREATE TABLE entities (
    entity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL,
    display_name TEXT,
    public_key TEXT,
    wallet_address TEXT,
    email_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'ACTIVE'
);

---------------------------------------------------------
-- REPUTATION EVENTS
---------------------------------------------------------

CREATE TABLE reputation_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    event_type VARCHAR(100),
    score_delta NUMERIC(12,4),
    source TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- CURRENT SCORE
---------------------------------------------------------

CREATE TABLE reputation_scores (
    entity_id UUID PRIMARY KEY REFERENCES entities(entity_id),
    score NUMERIC(12,4) DEFAULT 0,
    trust_level VARCHAR(30),
    confidence NUMERIC(5,2),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- DEVICE FINGERPRINTS
---------------------------------------------------------

CREATE TABLE device_fingerprints (
    fingerprint_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    fingerprint_hash TEXT,
    os TEXT,
    browser TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- NETWORK HISTORY
---------------------------------------------------------

CREATE TABLE network_history (
    record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    ip_address INET,
    subnet CIDR,
    country VARCHAR(50),
    asn BIGINT,
    vpn_detected BOOLEAN DEFAULT FALSE,
    tor_detected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- IDENTITY LINKS
---------------------------------------------------------

CREATE TABLE identity_links (
    link_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_entity UUID REFERENCES entities(entity_id),
    target_entity UUID REFERENCES entities(entity_id),
    confidence NUMERIC(5,2),
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- TRANSACTIONS
---------------------------------------------------------

CREATE TABLE transactions (
    tx_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    blockchain TEXT,
    tx_hash TEXT,
    amount NUMERIC(30,8),
    token TEXT,
    direction VARCHAR(10),
    counterparty TEXT,
    timestamp TIMESTAMP
);

---------------------------------------------------------
-- BEHAVIOR FEATURES
---------------------------------------------------------

CREATE TABLE behavior_features (
    feature_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    login_frequency NUMERIC,
    session_duration NUMERIC,
    average_tx_interval NUMERIC,
    failed_logins INTEGER,
    metadata JSONB,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- REPUTATION TRANSFERS
---------------------------------------------------------

CREATE TABLE reputation_transfers (
    transfer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender UUID REFERENCES entities(entity_id),
    receiver UUID REFERENCES entities(entity_id),
    reputation_points NUMERIC,
    reason TEXT,
    transferred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- REVIEW GRAPH
---------------------------------------------------------

CREATE TABLE review_graph (
    review_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reviewer UUID REFERENCES entities(entity_id),
    reviewed UUID REFERENCES entities(entity_id),
    rating NUMERIC(4,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- RISK SCORES
---------------------------------------------------------

CREATE TABLE risk_scores (
    entity_id UUID PRIMARY KEY REFERENCES entities(entity_id),
    sybil_score NUMERIC,
    fraud_score NUMERIC,
    laundering_score NUMERIC,
    collusion_score NUMERIC,
    anomaly_score NUMERIC,
    overall_risk NUMERIC,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- ALERTS
---------------------------------------------------------

CREATE TABLE reputation_alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id),
    severity VARCHAR(20),
    rule_name TEXT,
    evidence JSONB,
    resolved BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- AUDIT LOG
---------------------------------------------------------

CREATE TABLE audit_log (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor TEXT,
    action TEXT,
    target_entity UUID,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- INDEXES
---------------------------------------------------------

CREATE INDEX idx_events_entity
ON reputation_events(entity_id);

CREATE INDEX idx_network_ip
ON network_history(ip_address);

CREATE INDEX idx_wallet
ON entities(wallet_address);

CREATE INDEX idx_tx_hash
ON transactions(tx_hash);

CREATE INDEX idx_reviewer
ON review_graph(reviewer);

CREATE INDEX idx_reviewed
ON review_graph(reviewed);

---------------------------------------------------------
-- VIEW
---------------------------------------------------------

CREATE VIEW high_risk_entities AS
SELECT
    e.entity_id,
    e.display_name,
    r.overall_risk,
    s.score
FROM entities e
JOIN risk_scores r
ON e.entity_id = r.entity_id
LEFT JOIN reputation_scores s
ON e.entity_id = s.entity_id
WHERE r.overall_risk > 75;

---------------------------------------------------------
-- DETECTION FUNCTION
---------------------------------------------------------

CREATE OR REPLACE FUNCTION detect_reputation_washing()
RETURNS TABLE(
    entity UUID,
    risk NUMERIC,
    reason TEXT
)
LANGUAGE SQL
AS $$
SELECT
    r.entity_id,
    r.overall_risk,
    CASE
        WHEN r.sybil_score > 80 THEN 'Possible Sybil Attack'
        WHEN r.collusion_score > 80 THEN 'Collusive Rating Ring'
        WHEN r.laundering_score > 80 THEN 'Reputation Transfer Detected'
        WHEN r.fraud_score > 80 THEN 'Fraudulent Activity'
        ELSE 'Unknown'
    END
FROM risk_scores r
WHERE r.overall_risk > 75;
$$;
