#!/usr/bin/env python3
"""
Strategy Research Database Access Layer

Shared utility for Incubator skills to read/write the strategy research database.
Handles dialect translation between Snowflake and PostgreSQL, SQL generation,
execution, and structured output.

Usage:
    python3 scripts/research-db.py <command> [--json '<args>']

Commands:
    query-landscape     Query competitive landscape by capability slugs
    query-competitor    Deep-dive on a specific competitor
    query-gaps          Detect finding gaps for competitors on given capabilities
    write-finding       Write a research finding + capability links
    write-findings      Batch write multiple findings
    lookup-competitor   Get competitor ID by name
    lookup-capabilities Get capability IDs by slugs
    stats               Database health summary

Backend selection:
    Set RESEARCH_DB_BACKEND=snowflake or RESEARCH_DB_BACKEND=postgresql (default: postgresql)
"""

import argparse
import json
import os
import subprocess
import sys
import uuid
from textwrap import dedent

# ---------------------------------------------------------------------------
# Configuration — loaded from research-db-config.json (gitignored)
# ---------------------------------------------------------------------------

def _load_config():
    """Load connection config from the gitignored config file."""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research-db-config.json")
    if not os.path.exists(config_path):
        print(json.dumps({"error": f"Config file not found: {config_path}. Copy research-db-config.sample.json to research-db-config.json and fill in your connection details."}))
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)

_CONFIG = _load_config()
BACKEND = os.environ.get("RESEARCH_DB_BACKEND", "postgresql")

_pg = _CONFIG.get("postgresql", {})
PG_SSH = _pg.get("ssh_command", "")
_pg_exec_base = _pg.get("psql_exec", "")
PG_EXEC = f"{_pg_exec_base} -t -A"
PG_EXEC_FULL = _pg_exec_base

_sf = _CONFIG.get("snowflake", {})
SF_CMD = _sf.get("cli_command", "snow sql --enable-templating NONE")

DOMAIN = _CONFIG.get(BACKEND, {}).get("domain", "mastery")

# ---------------------------------------------------------------------------
# Dialect translation
# ---------------------------------------------------------------------------

def sql_array_contains(col, val):
    if BACKEND == "snowflake":
        return f"ARRAY_CONTAINS('{val}', {col})"
    return f"'{val}' = ANY({col})"

def sql_dateadd_months(n, date_col):
    if BACKEND == "snowflake":
        return f"DATEADD('month', {n}, {date_col})"
    # When n is a column reference (not a literal), use the || cast pattern
    return f"{date_col} + ({n} || ' months')::interval"

def sql_current_user():
    if BACKEND == "snowflake":
        return "CURRENT_USER()"
    return "CURRENT_USER"

def sql_json_field(col, key):
    """Extract a text field from JSON/VARIANT column."""
    if BACKEND == "snowflake":
        return f"{col}:{key}::VARCHAR"
    return f"{col}->>'{key}'"

def sql_count_if(condition):
    """Conditional count — FILTER (WHERE) for PG, COUNT_IF for Snowflake."""
    if BACKEND == "snowflake":
        return f"COUNT_IF({condition})"
    return f"COUNT(*) FILTER (WHERE {condition})"

def sql_preamble():
    if BACKEND == "snowflake":
        role = _sf.get("role", "PRODUCT_ANALYST")
        db = _sf.get("database", "PRODUCT")
        schema = _sf.get("schema", "STRATEGY_RESEARCH")
        return f"USE ROLE {role};\nUSE DATABASE {db};\nUSE SCHEMA {schema};\n"
    return "SET search_path TO strategy_research;\n"

def sql_gen_uuid():
    """Generate a UUID. For PG we use gen_random_uuid() in SQL; for SF we generate in Python."""
    return str(uuid.uuid4())

def esc(s):
    """Escape single quotes for SQL."""
    if s is None:
        return None
    return str(s).replace("'", "''")

# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def execute_sql(sql, raw_output=False):
    """Execute SQL against the configured backend. Returns stdout."""
    if BACKEND == "snowflake":
        # Write to temp file and execute
        tmp = "/tmp/research-db-query.sql"
        with open(tmp, "w") as f:
            f.write(sql)
        cmd = f"{SF_CMD} -f {tmp}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    else:
        # Write SQL to temp file, transfer and execute on PostgreSQL via SSH
        tmp_local = "/tmp/research-db-query.sql"
        with open(tmp_local, "w") as f:
            f.write(sql)
        if raw_output:
            cmd = f"cat {tmp_local} | {PG_SSH} \"{PG_EXEC_FULL} -f /dev/stdin\""
        else:
            cmd = f"cat {tmp_local} | {PG_SSH} \"{PG_EXEC} -F '|' -f /dev/stdin\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        print(json.dumps({"error": result.stderr.strip()}), file=sys.stderr)
        sys.exit(1)

    return result.stdout.strip()

def parse_pg_rows(output, columns):
    """Parse pipe-delimited PostgreSQL output into list of dicts."""
    rows = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= len(columns):
            rows.append({col: parts[i].strip() for i, col in enumerate(columns)})
    return rows

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_query_landscape(args):
    """Query competitive landscape by capability slugs.

    Returns competitors tagged to the given capabilities, with their findings
    and gap indicators. Sorted by tier then category.
    """
    caps = args.get("capabilities", [])
    if not caps:
        print(json.dumps({"error": "capabilities list required"}))
        sys.exit(1)

    cap_list = ",".join(f"'{c}'" for c in caps)
    ttl_filter = sql_dateadd_months("rf.ttl_months", "rf.created_at")

    sql = f"""{sql_preamble()}
-- Competitors for these capabilities (compact — no intelligence body)
SELECT c.id, c.name, c.category, c.market_tier, c.pricing_model,
  array_agg(DISTINCT cap.slug) AS matched_caps
FROM competitors c
JOIN competitor_capabilities cc ON c.id = cc.competitor_id
JOIN capabilities cap ON cc.capability_id = cap.id
WHERE cap.slug IN ({cap_list})
  AND c.superseded_by IS NULL
GROUP BY c.id, c.name, c.category, c.market_tier, c.pricing_model
ORDER BY
  CASE c.market_tier WHEN 'tier-1' THEN 1 WHEN 'tier-2' THEN 2 WHEN 'tier-3' THEN 3 END,
  CASE c.category WHEN 'core' THEN 1 WHEN 'adjacent' THEN 2 WHEN 'emerging' THEN 3 WHEN 'substitute' THEN 4 END;
"""

    # Single SQL with both queries separated by a marker comment
    sql = f"""{sql_preamble()}
SELECT '--- COMPETITORS ---' AS section;

SELECT c.name, c.category, c.market_tier, c.pricing_model,
  array_agg(DISTINCT cap.slug) AS matched_caps
FROM competitors c
JOIN competitor_capabilities cc ON c.id = cc.competitor_id
JOIN capabilities cap ON cc.capability_id = cap.id
WHERE cap.slug IN ({cap_list})
  AND c.superseded_by IS NULL
GROUP BY c.id, c.name, c.category, c.market_tier, c.pricing_model
ORDER BY
  CASE c.market_tier WHEN 'tier-1' THEN 1 WHEN 'tier-2' THEN 2 WHEN 'tier-3' THEN 3 END,
  CASE c.category WHEN 'core' THEN 1 WHEN 'adjacent' THEN 2 WHEN 'emerging' THEN 3 WHEN 'substitute' THEN 4 END;

SELECT '--- FINDINGS ---' AS section;

SELECT rf.category AS finding_type, rf.confidence, LEFT(rf.claim, 200) AS claim,
  LEFT(rf.evidence, 100) AS evidence, c.name AS competitor_name
FROM research_findings rf
JOIN finding_capabilities fc ON rf.id = fc.finding_id
JOIN capabilities cap ON fc.capability_id = cap.id
LEFT JOIN competitors c ON rf.competitor_id = c.id
WHERE cap.slug IN ({cap_list})
  AND rf.superseded_by IS NULL
  AND {ttl_filter} > CURRENT_DATE
GROUP BY rf.id, rf.category, rf.confidence, rf.claim, rf.evidence, c.name
ORDER BY
  CASE rf.confidence WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END,
  rf.category
LIMIT 40;
"""

    print(execute_sql(sql, raw_output=True))


def cmd_query_competitor(args):
    """Deep-dive on a specific competitor."""
    name = args.get("name")
    if not name:
        print(json.dumps({"error": "name required"}))
        sys.exit(1)

    sql = f"""{sql_preamble()}
-- Competitor profile
SELECT c.*, array_agg(DISTINCT cap.slug ORDER BY cap.slug) AS capabilities
FROM competitors c
LEFT JOIN competitor_capabilities cc ON c.id = cc.competitor_id
LEFT JOIN capabilities cap ON cc.capability_id = cap.id
WHERE c.name = '{esc(name)}' AND c.superseded_by IS NULL
GROUP BY c.id;

-- Linked findings
SELECT rf.id, rf.topic, rf.category, rf.claim, rf.evidence,
  rf.confidence, rf.source_url, rf.ttl_months, rf.created_at
FROM research_findings rf
WHERE rf.competitor_id = (SELECT id FROM competitors WHERE name = '{esc(name)}' AND superseded_by IS NULL)
  AND rf.superseded_by IS NULL
ORDER BY rf.created_at DESC;
"""
    output = execute_sql(sql, raw_output=True)
    print(output)


def cmd_query_gaps(args):
    """Detect finding gaps: competitors tagged to capabilities but with no matching findings."""
    caps = args.get("capabilities", [])
    if not caps:
        print(json.dumps({"error": "capabilities list required"}))
        sys.exit(1)

    cap_list = ",".join(f"'{c}'" for c in caps)

    sql = f"""{sql_preamble()}
SELECT c.name, c.category, c.market_tier, cap.slug AS capability,
  CASE WHEN COUNT(DISTINCT rf.id) = 0 THEN 'GAP' ELSE 'COVERED' END AS status,
  COUNT(DISTINCT rf.id) AS finding_count
FROM competitors c
JOIN competitor_capabilities cc ON c.id = cc.competitor_id
JOIN capabilities cap ON cc.capability_id = cap.id
LEFT JOIN research_findings rf ON c.id = rf.competitor_id AND rf.superseded_by IS NULL
LEFT JOIN finding_capabilities fc ON rf.id = fc.finding_id AND fc.capability_id = cap.id
WHERE cap.slug IN ({cap_list}) AND c.superseded_by IS NULL
GROUP BY c.name, c.category, c.market_tier, cap.slug
ORDER BY
  CASE WHEN COUNT(DISTINCT rf.id) = 0 THEN 0 ELSE 1 END,
  c.market_tier, c.category, c.name;
"""
    output = execute_sql(sql, raw_output=True)
    print(output)


def cmd_write_finding(args):
    """Write a single research finding + capability junction rows."""
    required = ["claim", "evidence", "confidence", "ttl_months", "category", "topic", "capabilities"]
    for field in required:
        if field not in args:
            print(json.dumps({"error": f"missing required field: {field}"}))
            sys.exit(1)

    finding_id = sql_gen_uuid()
    competitor_id = args.get("competitor_id")
    source_url = args.get("source_url")
    source_desc = args.get("source_description")
    cap_slugs = args["capabilities"]

    # Build SQL
    lines = [sql_preamble()]

    # Look up capability IDs
    cap_ids_sql = ",".join(f"'{c}'" for c in cap_slugs)

    url_val = f"'{esc(source_url)}'" if source_url else "NULL"
    desc_val = f"'{esc(source_desc)}'" if source_desc else "NULL"
    comp_val = f"'{competitor_id}'" if competitor_id else "NULL"

    lines.append(f"""
INSERT INTO research_findings (id, domain, topic, category, agent_type, claim, evidence,
  source_url, source_description, confidence, ttl_months, competitor_id)
VALUES ('{finding_id}', '{DOMAIN}', '{esc(args["topic"])}', '{esc(args["category"])}', NULL,
  '{esc(args["claim"])}', '{esc(args["evidence"])}',
  {url_val}, {desc_val}, '{esc(args["confidence"])}', {args["ttl_months"]}, {comp_val});
""")

    # Junction rows
    for slug in cap_slugs:
        lines.append(f"""
INSERT INTO finding_capabilities (finding_id, capability_id)
SELECT '{finding_id}', id FROM capabilities WHERE slug = '{slug}';
""")

    sql = "\n".join(lines)
    execute_sql(sql)
    print(json.dumps({"finding_id": finding_id, "capabilities": cap_slugs}))


def cmd_write_findings(args):
    """Batch write multiple findings using INSERT...SELECT...UNION ALL."""
    findings = args.get("findings", [])
    if not findings:
        print(json.dumps({"error": "findings list required"}))
        sys.exit(1)

    lines = [sql_preamble()]
    result_ids = []

    # Generate IDs and build batch INSERT for findings
    for f in findings:
        f["_id"] = sql_gen_uuid()
        result_ids.append({"finding_id": f["_id"], "claim_preview": f["claim"][:80]})

    if BACKEND == "snowflake":
        lines.append("INSERT INTO research_findings (id, domain, topic, category, agent_type, claim, evidence, source_url, source_description, confidence, ttl_months, competitor_id)")
        lines.append("SELECT * FROM (")
        for i, f in enumerate(findings):
            prefix = "    SELECT " if i == 0 else "    UNION ALL SELECT "
            url = f"'{esc(f.get('source_url'))}'" if f.get("source_url") else "NULL"
            desc = f"'{esc(f.get('source_description'))}'" if f.get("source_description") else "NULL"
            comp = f"'{f['competitor_id']}'" if f.get("competitor_id") else "NULL"
            lines.append(f"{prefix}'{f['_id']}', '{DOMAIN}', '{esc(f['topic'])}', '{esc(f['category'])}', NULL, '{esc(f['claim'])}', '{esc(f['evidence'])}', {url}, {desc}, '{esc(f['confidence'])}', {f['ttl_months']}, {comp}")
        lines.append(");")
    else:
        # PostgreSQL multi-row VALUES
        lines.append("INSERT INTO research_findings (id, domain, topic, category, agent_type, claim, evidence, source_url, source_description, confidence, ttl_months, competitor_id) VALUES")
        for i, f in enumerate(findings):
            url = f"'{esc(f.get('source_url'))}'" if f.get("source_url") else "NULL"
            desc = f"'{esc(f.get('source_description'))}'" if f.get("source_description") else "NULL"
            comp = f"'{f['competitor_id']}'" if f.get("competitor_id") else "NULL"
            comma = "," if i < len(findings) - 1 else ""
            lines.append(f"('{f['_id']}', '{DOMAIN}', '{esc(f['topic'])}', '{esc(f['category'])}', NULL, '{esc(f['claim'])}', '{esc(f['evidence'])}', {url}, {desc}, '{esc(f['confidence'])}', {f['ttl_months']}, {comp}){comma}")
        lines.append(";")

    # Junction rows — batch
    junction_rows = []
    for f in findings:
        for slug in f.get("capabilities", []):
            junction_rows.append((f["_id"], slug))

    if junction_rows:
        if BACKEND == "snowflake":
            lines.append("\nINSERT INTO finding_capabilities (finding_id, capability_id)")
            lines.append("SELECT fc.fid, c.id FROM (")
            for i, (fid, slug) in enumerate(junction_rows):
                prefix = "    SELECT " if i == 0 else "    UNION ALL SELECT "
                lines.append(f"{prefix}'{fid}' AS fid, '{slug}' AS slug")
            lines.append(") fc JOIN capabilities c ON fc.slug = c.slug;")
        else:
            lines.append("\nINSERT INTO finding_capabilities (finding_id, capability_id)")
            lines.append("SELECT fc.fid, c.id FROM (VALUES")
            for i, (fid, slug) in enumerate(junction_rows):
                comma = "," if i < len(junction_rows) - 1 else ""
                lines.append(f"  ('{fid}'::uuid, '{slug}'::text){comma}")
            lines.append(") AS fc(fid, slug) JOIN capabilities c ON fc.slug = c.slug;")

    sql = "\n".join(lines)
    execute_sql(sql)
    print(json.dumps({"findings_written": len(findings), "junction_rows": len(junction_rows), "ids": result_ids}))


def cmd_lookup_competitor(args):
    """Get competitor ID and basic info by name."""
    name = args.get("name")
    if not name:
        print(json.dumps({"error": "name required"}))
        sys.exit(1)

    sql = f"""{sql_preamble()}
SELECT id, name, category, market_tier FROM competitors
WHERE name ILIKE '%{esc(name)}%' AND superseded_by IS NULL
ORDER BY name;
"""
    output = execute_sql(sql)
    rows = parse_pg_rows(output, ["id", "name", "category", "market_tier"])
    print(json.dumps(rows))


def cmd_lookup_capabilities(args):
    """Get capability IDs by slugs."""
    slugs = args.get("slugs", [])
    if not slugs:
        sql = f"{sql_preamble()}\nSELECT slug, id FROM capabilities ORDER BY slug;"
    else:
        slug_list = ",".join(f"'{s}'" for s in slugs)
        sql = f"{sql_preamble()}\nSELECT slug, id FROM capabilities WHERE slug IN ({slug_list}) ORDER BY slug;"

    output = execute_sql(sql)
    rows = parse_pg_rows(output, ["slug", "id"])
    print(json.dumps(rows))


def cmd_stats(args):
    """Database health summary."""
    active_comp = sql_count_if("superseded_by IS NULL")
    active_find = sql_count_if("superseded_by IS NULL")
    sql = f"""{sql_preamble()}
SELECT 'competitors' AS entity, COUNT(*) AS total,
  {active_comp} AS active FROM competitors
UNION ALL SELECT 'findings', COUNT(*), {active_find} FROM research_findings
UNION ALL SELECT 'capabilities', COUNT(*), COUNT(*) FROM capabilities
UNION ALL SELECT 'comp_caps', COUNT(*), COUNT(*) FROM competitor_capabilities
UNION ALL SELECT 'find_caps', COUNT(*), COUNT(*) FROM finding_capabilities;

SELECT COUNT(*) AS stale_findings FROM research_findings
WHERE superseded_by IS NULL
  AND {sql_dateadd_months("ttl_months", "created_at")} < CURRENT_DATE;
"""
    output = execute_sql(sql, raw_output=True)
    print(output)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

COMMANDS = {
    "query-landscape": cmd_query_landscape,
    "query-competitor": cmd_query_competitor,
    "query-gaps": cmd_query_gaps,
    "write-finding": cmd_write_finding,
    "write-findings": cmd_write_findings,
    "lookup-competitor": cmd_lookup_competitor,
    "lookup-capabilities": cmd_lookup_capabilities,
    "stats": cmd_stats,
}

def main():
    parser = argparse.ArgumentParser(description="Strategy Research Database Access Layer")
    parser.add_argument("command", choices=COMMANDS.keys())
    parser.add_argument("--json", type=str, default="{}", help="JSON arguments")
    parsed = parser.parse_args()

    try:
        args = json.loads(parsed.json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    COMMANDS[parsed.command](args)

if __name__ == "__main__":
    main()
