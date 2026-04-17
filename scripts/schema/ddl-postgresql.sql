-- PostgreSQL DDL for the strategy research schema
-- Dev/eval environment — replace schema name if needed

CREATE SCHEMA IF NOT EXISTS strategy_research;
SET search_path TO strategy_research;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Capabilities (reference vocabulary)
-- Flat capability vocabulary. Tag cloud with governance guardrails.
CREATE TABLE capabilities (
    id              UUID          NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            VARCHAR(100)  NOT NULL UNIQUE,
    display_name    VARCHAR(200)  NOT NULL,
    description     TEXT,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Competitors (entity registry)
CREATE TABLE competitors (
    id                  UUID          NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain              VARCHAR(50)   NOT NULL,
    name                VARCHAR(200)  NOT NULL,
    category            VARCHAR(20)   NOT NULL CHECK (category IN ('core', 'emerging', 'adjacent', 'substitute')),
    segments            TEXT[],                   -- {'k-12', 'higher-ed', 'workforce', 'certification'}
    pricing_model       VARCHAR(30)   CHECK (pricing_model IS NULL OR pricing_model IN ('per-seat', 'per-assessment', 'platform-fee', 'bundled', 'freemium')),
    integration_posture TEXT[],                   -- {'lti-certified', 'sis-rostering', 'api-first', 'standalone'}
    market_tier         VARCHAR(10)   CHECK (market_tier IS NULL OR market_tier IN ('tier-1', 'tier-2', 'tier-3')),
    intelligence        JSONB,                    -- freeform: funding, partnerships, GTM, deployment
    last_researched     DATE          NOT NULL,
    superseded_by       UUID          REFERENCES competitors (id),
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by          VARCHAR(100)  NOT NULL DEFAULT CURRENT_USER
);

-- 3. Competitor ↔ Capabilities (junction)
CREATE TABLE competitor_capabilities (
    competitor_id   UUID NOT NULL REFERENCES competitors (id),
    capability_id   UUID NOT NULL REFERENCES capabilities (id),

    PRIMARY KEY (competitor_id, capability_id)
);

-- 4. Research findings (fact table)
CREATE TABLE research_findings (
    id                  UUID          NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain              VARCHAR(50)   NOT NULL,
    topic               VARCHAR(30)   NOT NULL CHECK (topic IN ('competitive-landscape', 'customer-evidence', 'market-sizing', 'enrichment')),
    category            VARCHAR(30)   NOT NULL,
    agent_type          VARCHAR(30),
    claim               TEXT          NOT NULL,
    evidence            TEXT,
    source_url          TEXT,
    source_description  VARCHAR(500),
    confidence          VARCHAR(10)   NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
    ttl_months          INTEGER       NOT NULL,
    competitor_id       UUID          REFERENCES competitors (id),
    origin_context      JSONB,                    -- provenance: origin idea, agent-specific fields
    superseded_by       UUID          REFERENCES research_findings (id),
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by          VARCHAR(100)  NOT NULL DEFAULT CURRENT_USER
);

-- Index for common query patterns
CREATE INDEX idx_findings_domain_category ON research_findings (domain, category);
CREATE INDEX idx_findings_competitor ON research_findings (competitor_id) WHERE competitor_id IS NOT NULL;

-- 5. Findings ↔ Capabilities (junction)
CREATE TABLE finding_capabilities (
    finding_id      UUID NOT NULL REFERENCES research_findings (id),
    capability_id   UUID NOT NULL REFERENCES capabilities (id),

    PRIMARY KEY (finding_id, capability_id)
);

-- Materialized view: Current findings (non-stale, non-superseded)
CREATE MATERIALIZED VIEW current_findings AS
SELECT *
FROM research_findings
WHERE superseded_by IS NULL
  AND created_at + (ttl_months * INTERVAL '1 month') > CURRENT_DATE;
