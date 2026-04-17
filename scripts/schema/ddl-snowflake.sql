-- Snowflake DDL for PRODUCT.STRATEGY_RESEARCH
-- Run with PRODUCT_ANALYST role

USE ROLE PRODUCT_ANALYST;
USE DATABASE PRODUCT;

CREATE SCHEMA IF NOT EXISTS STRATEGY_RESEARCH;
USE SCHEMA STRATEGY_RESEARCH;

-- 1. Capabilities (reference vocabulary)
-- Flat capability vocabulary. Tag cloud with governance guardrails.
CREATE TABLE capabilities (
    id              VARCHAR(36)   NOT NULL PRIMARY KEY,
    slug            VARCHAR(100)  NOT NULL UNIQUE,
    display_name    VARCHAR(200)  NOT NULL,
    description     TEXT,
    created_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. Competitors (entity registry)
CREATE TABLE competitors (
    id                  VARCHAR(36)   NOT NULL PRIMARY KEY,
    domain              VARCHAR(50)   NOT NULL,
    name                VARCHAR(200)  NOT NULL,
    category            VARCHAR(20)   NOT NULL,  -- 'core' | 'emerging' | 'adjacent' | 'substitute'
    segments            ARRAY,                    -- ['k-12', 'higher-ed', 'workforce', 'certification']
    pricing_model       VARCHAR(30),              -- 'per-seat' | 'per-assessment' | 'platform-fee' | 'bundled' | 'freemium'
    integration_posture ARRAY,                    -- ['lti-certified', 'sis-rostering', 'api-first', 'standalone']
    market_tier         VARCHAR(10),              -- 'tier-1' | 'tier-2' | 'tier-3'
    intelligence        VARIANT,                  -- freeform: funding, partnerships, GTM, deployment
    last_researched     DATE          NOT NULL,
    superseded_by       VARCHAR(36),              -- self-FK: points to replacement
    created_at          TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by          VARCHAR(100)  DEFAULT CURRENT_USER(),

    CONSTRAINT chk_competitor_category CHECK (category IN ('core', 'emerging', 'adjacent', 'substitute')),
    CONSTRAINT chk_market_tier CHECK (market_tier IS NULL OR market_tier IN ('tier-1', 'tier-2', 'tier-3')),
    CONSTRAINT chk_pricing_model CHECK (pricing_model IS NULL OR pricing_model IN ('per-seat', 'per-assessment', 'platform-fee', 'bundled', 'freemium')),
    CONSTRAINT fk_competitor_superseded FOREIGN KEY (superseded_by) REFERENCES competitors (id)
);

-- 3. Competitor ↔ Capabilities (junction)
CREATE TABLE competitor_capabilities (
    competitor_id   VARCHAR(36) NOT NULL,
    capability_id   VARCHAR(36) NOT NULL,

    PRIMARY KEY (competitor_id, capability_id),
    CONSTRAINT fk_cc_competitor FOREIGN KEY (competitor_id) REFERENCES competitors (id),
    CONSTRAINT fk_cc_capability FOREIGN KEY (capability_id) REFERENCES capabilities (id)
);

-- 4. Research findings (fact table)
CREATE TABLE research_findings (
    id                  VARCHAR(36)   NOT NULL PRIMARY KEY,
    domain              VARCHAR(50)   NOT NULL,
    topic               VARCHAR(30)   NOT NULL,  -- 'competitive-landscape' | 'customer-evidence' | 'market-sizing' | 'enrichment'
    category            VARCHAR(30)   NOT NULL,  -- topic-specific vocabulary
    agent_type          VARCHAR(30),              -- 'educator-sme' | 'edtech-sme' | 'divergent-thinking' | null for manual
    claim               TEXT          NOT NULL,
    evidence            TEXT,
    source_url          TEXT,
    source_description  VARCHAR(500),
    confidence          VARCHAR(10)   NOT NULL,  -- 'high' | 'medium' | 'low'
    ttl_months          INTEGER       NOT NULL,
    competitor_id       VARCHAR(36),              -- FK: when finding is about a named competitor
    origin_context      VARIANT,                  -- provenance: origin idea, agent-specific fields
    superseded_by       VARCHAR(36),              -- self-FK: points to replacement
    created_at          TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by          VARCHAR(100)  DEFAULT CURRENT_USER(),

    CONSTRAINT chk_topic CHECK (topic IN ('competitive-landscape', 'customer-evidence', 'market-sizing', 'enrichment')),
    CONSTRAINT chk_confidence CHECK (confidence IN ('high', 'medium', 'low')),
    CONSTRAINT fk_finding_competitor FOREIGN KEY (competitor_id) REFERENCES competitors (id),
    CONSTRAINT fk_finding_superseded FOREIGN KEY (superseded_by) REFERENCES research_findings (id)
);

-- Cluster research_findings for query performance
ALTER TABLE research_findings CLUSTER BY (domain, category);

-- 5. Findings ↔ Capabilities (junction)
CREATE TABLE finding_capabilities (
    finding_id      VARCHAR(36) NOT NULL,
    capability_id   VARCHAR(36) NOT NULL,

    PRIMARY KEY (finding_id, capability_id),
    CONSTRAINT fk_fc_finding FOREIGN KEY (finding_id) REFERENCES research_findings (id),
    CONSTRAINT fk_fc_capability FOREIGN KEY (capability_id) REFERENCES capabilities (id)
);

-- View: Current findings (non-stale, non-superseded)
-- Default query surface for consumers.
CREATE OR REPLACE VIEW current_findings AS
SELECT *
FROM research_findings
WHERE superseded_by IS NULL
  AND DATEADD('month', ttl_months, created_at) > CURRENT_DATE();
