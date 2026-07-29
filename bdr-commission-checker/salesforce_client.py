#!/usr/bin/env python3
"""Connect to *your own* Salesforce org and pull the opportunities credited to you.

No opportunity IDs or user IDs are hard-coded: the tool authenticates as you and
discovers your own user id, then fetches the opportunities where you are the BDR.

Authentication — the first fully-configured mode wins:

  1. Salesforce CLI (easiest, browser login, no secrets stored by this tool)
     Install the `sf` CLI once and run:  sf org login web
     Then this tool reuses that session automatically. Optionally set
     SF_CLI_ALIAS to target a specific org (defaults to your default org).

  2. Session token (env):   SF_INSTANCE_URL + SF_ACCESS_TOKEN

  3. Username + password (env):
       SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN
       (optional SF_DOMAIN = "login" for production [default] or "test" for sandbox)

All three modes use the `simple-salesforce` package (see requirements.txt) to
talk to the API; the Salesforce CLI in mode 1 is just a convenient, secret-free
way to obtain a session (it opens a browser login and this tool reuses the token).

You can override auto-detection of who you are with SF_BDR_USER_ID (an 18-char
Salesforce User Id) — handy if BDR_Name__c is set to a different user than the
one you log in as.
"""
from __future__ import annotations

import json
import os
import subprocess

# Field names the audit relies on. Kept here so an org with slightly different
# API names can adjust them in one place (or via SF_* env overrides below).
BDR_FIELD = os.getenv("SF_BDR_FIELD", "BDR_Name__c")
# Account field that flags ICP compliance (for the kicker's 80%-ICP gate).
ICP_FIELD = os.getenv("SF_ICP_FIELD", "Sales_Ops_TP_Status__c")

FIELDS = [
    "Name", "StageName", "Account_Incentive_Rating__c",
    "Disco_Call_Date__c", "Discovery_Call_Status__c",
    "DateSettoP1__c", "DateSettoT1__c", "Finance_Go_Live__c",
    "LeadSource", "Commission_Hold__c", "XCommission_Hold__c",
    f"Account.{ICP_FIELD}",
]


def _soql(user_id: str) -> str:
    return (
        f"SELECT {', '.join(FIELDS)} FROM Opportunity "
        f"WHERE {BDR_FIELD} = '{user_id}' "
        f"AND (Disco_Call_Date__c != null OR DateSettoP1__c != null "
        f"OR DateSettoT1__c != null)"
    )


def _sf_cli_session() -> tuple[str, str] | None:
    """Return (instance_url, access_token) from an authenticated `sf` CLI, or None."""
    alias = os.getenv("SF_CLI_ALIAS")
    cmd = ["sf", "org", "display", "--json"]
    if alias:
        cmd += ["--target-org", alias]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    try:
        res = json.loads(out.stdout)["result"]
        return res["instanceUrl"], res["accessToken"]
    except (json.JSONDecodeError, KeyError):
        return None


def _connect():
    """Return an authenticated simple_salesforce.Salesforce, raising with guidance."""
    try:
        from simple_salesforce import Salesforce
    except ImportError as e:  # pragma: no cover - env dependent
        raise SystemExit(
            "This needs the 'simple-salesforce' package. Install it with:\n"
            "    pip install -r requirements.txt\n"
            "(or use the Salesforce CLI auth mode: `sf org login web`)."
        ) from e

    inst, tok = os.getenv("SF_INSTANCE_URL"), os.getenv("SF_ACCESS_TOKEN")
    if inst and tok:
        return Salesforce(instance_url=inst, session_id=tok)

    user, pwd, token = (
        os.getenv("SF_USERNAME"), os.getenv("SF_PASSWORD"), os.getenv("SF_SECURITY_TOKEN"),
    )
    if user and pwd and token:
        return Salesforce(
            username=user, password=pwd, security_token=token,
            domain=os.getenv("SF_DOMAIN", "login"),
        )

    cli = _sf_cli_session()
    if cli:
        return Salesforce(instance_url=cli[0], session_id=cli[1])

    raise SystemExit(
        "No Salesforce credentials found. Pick ONE:\n"
        "  • Salesforce CLI:  run `sf org login web` once, then re-run this tool.\n"
        "  • Session:         set SF_INSTANCE_URL and SF_ACCESS_TOKEN.\n"
        "  • User/password:   set SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN.\n"
        "See SETUP.md for step-by-step help."
    )


def current_user_id(sf) -> str:
    """The logged-in user's 18-char Id (or SF_BDR_USER_ID override)."""
    override = os.getenv("SF_BDR_USER_ID")
    if override:
        return override.strip()
    me = sf.restful("chatter/users/me")
    return me["id"]


def fetch_records() -> list[dict]:
    """Return the raw Salesforce opportunity records for the logged-in BDR."""
    sf = _connect()
    uid = current_user_id(sf)
    result = sf.query_all(_soql(uid))
    return result.get("records", [])


def fetch_to_file(path) -> int:
    """Fetch and write {"records": [...]} to `path`; return the record count."""
    records = fetch_records()
    from pathlib import Path
    Path(path).write_text(json.dumps({"records": records}, indent=2, default=str))
    return len(records)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "sf_opps.json"
    n = fetch_to_file(out)
    print(f"Fetched {n} opportunities to {out}")
