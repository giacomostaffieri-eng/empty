# Connecting the tool to *your* Salesforce

`--sf-fetch` logs in as you and pulls the opportunities where you are the BDR
(`BDR_Name__c`). It auto-detects your own user id — nothing is hard-coded. Pick
**one** of the three auth methods below. All of them use the `simple-salesforce`
package, so first:

```bash
pip install -r requirements.txt
```

---

## Method 1 — Salesforce CLI (recommended, no secrets to manage)

Best if you'd rather not handle passwords/tokens. Install the Salesforce CLI once
(https://developer.salesforce.com/tools/salesforcecli), then log in through your
browser — the same SSO you use every day:

```bash
sf org login web
```

That's it. Re-run the tool with `--sf-fetch` and it reuses that session
automatically. If you have several orgs authenticated, point at one with:

```bash
export SF_CLI_ALIAS=my-org-alias      # optional
```

## Method 2 — Session token

If you can grab a live session (e.g. from the CLI: `sf org display`), set:

```bash
export SF_INSTANCE_URL="https://YOURDOMAIN.my.salesforce.com"
export SF_ACCESS_TOKEN="00D...your-session-id..."
```

## Method 3 — Username + password + security token

Classic API login. Your **security token** is emailed to you from Salesforce
(Settings → Reset My Security Token):

```bash
export SF_USERNAME="you@company.com"
export SF_PASSWORD="your-password"
export SF_SECURITY_TOKEN="your-token"
export SF_DOMAIN="login"     # use "test" for a sandbox
```

Tip: put these in a `.env` file (it's git-ignored) and `source .env` before
running, so they aren't saved in your shell history.

---

## Field / user overrides (only if your org differs)

The defaults match the standard BDR setup. Override via env vars only if needed:

| Variable | Purpose | Default |
|---|---|---|
| `SF_BDR_FIELD` | API name of the "BDR" field on Opportunity | `BDR_Name__c` |
| `SF_BDR_USER_ID` | Force which user's opps to pull (18-char Id) | your logged-in user |

## Verify the connection

```bash
python3 salesforce_client.py my_opps.json
# -> "Fetched N opportunities to my_opps.json"
```

If you see an auth error, the message tells you exactly which variables or CLI
step are missing. Nothing is sent anywhere except your own Salesforce org.
