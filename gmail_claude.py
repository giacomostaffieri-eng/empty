"""
Gmail + Claude automation: read emails, extract data, auto-reply, and follow up.

Setup:
  1. Create a Google Cloud project, enable Gmail API, download credentials.json
  2. Set ANTHROPIC_API_KEY in .env
  3. pip install -r requirements.txt
  4. python gmail_claude.py            (first run opens browser for OAuth)

Modes:
  python gmail_claude.py inbox     process unread emails and auto-reply (default)
  python gmail_claude.py followup  nudge sent threads still awaiting a reply
"""

import os
import base64
import json
import argparse
from email.mime.text import MIMEText
from email.utils import parseaddr
from dotenv import load_dotenv

import anthropic
from anthropic import beta_tool

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
MAX_EMAILS = 10  # how many unread emails to process per run

# Follow-up defaults: nudge threads where I sent the last message and it has been
# sitting without a reply for a while (but not so long it is no longer worth it).
FOLLOWUP_MIN_DAYS = 3   # give the recipient at least this many days to respond
FOLLOWUP_MAX_DAYS = 14  # don't chase threads older than this
MAX_FOLLOWUPS = 10      # how many awaiting-reply threads to surface per run


# ── Gmail auth ──────────────────────────────────────────────────────────────

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


# ── Gmail tools exposed to Claude ───────────────────────────────────────────

_service = None  # set before running the agent loop


@beta_tool
def list_unread_emails(max_results: int = MAX_EMAILS) -> str:
    """List unread emails from the inbox.

    Args:
        max_results: Maximum number of emails to return (default 10).
    """
    results = _service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results,
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        return json.dumps({"emails": []})
    emails = []
    for msg in messages:
        meta = _service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()
        headers = {h["name"]: h["value"] for h in meta["payload"]["headers"]}
        emails.append({
            "id": msg["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "snippet": meta.get("snippet", ""),
        })
    return json.dumps({"emails": emails})


@beta_tool
def get_email_body(email_id: str) -> str:
    """Get the full text body of an email.

    Args:
        email_id: The Gmail message ID.
    """
    msg = _service.users().messages().get(
        userId="me", id=email_id, format="full"
    ).execute()

    def extract_text(payload):
        mime = payload.get("mimeType", "")
        if mime == "text/plain":
            data = payload.get("body", {}).get("data", "")
            return base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
        if mime.startswith("multipart/"):
            for part in payload.get("parts", []):
                text = extract_text(part)
                if text:
                    return text
        return ""

    body = extract_text(msg["payload"])
    return json.dumps({"email_id": email_id, "body": body or msg.get("snippet", "")})


@beta_tool
def send_reply(email_id: str, reply_text: str) -> str:
    """Send a reply to an email.

    Args:
        email_id: The Gmail message ID to reply to.
        reply_text: The plain-text body of the reply.
    """
    original = _service.users().messages().get(
        userId="me", id=email_id, format="metadata",
        metadataHeaders=["From", "Subject", "Message-ID"],
    ).execute()
    headers = {h["name"]: h["value"] for h in original["payload"]["headers"]}
    thread_id = original["threadId"]

    subject = headers.get("Subject", "")
    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    mime = MIMEText(reply_text)
    mime["To"] = headers.get("From", "")
    mime["Subject"] = subject
    mime["In-Reply-To"] = headers.get("Message-ID", "")
    mime["References"] = headers.get("Message-ID", "")

    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
    _service.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": thread_id},
    ).execute()

    # Mark original as read
    _service.users().messages().modify(
        userId="me", id=email_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()

    return json.dumps({"status": "sent", "email_id": email_id})


@beta_tool
def mark_as_read(email_id: str) -> str:
    """Mark an email as read without replying.

    Args:
        email_id: The Gmail message ID.
    """
    _service.users().messages().modify(
        userId="me", id=email_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()
    return json.dumps({"status": "marked_as_read", "email_id": email_id})


# ── Follow-up tools ──────────────────────────────────────────────────────────

_my_address = None  # cached lowercase email address of the authenticated user


def _get_my_address() -> str:
    """Return (and cache) the authenticated user's own email address, lowercased."""
    global _my_address
    if _my_address is None:
        profile = _service.users().getProfile(userId="me").execute()
        _my_address = profile.get("emailAddress", "").lower()
    return _my_address


@beta_tool
def find_sent_awaiting_reply(
    min_days_ago: int = FOLLOWUP_MIN_DAYS,
    max_days_ago: int = FOLLOWUP_MAX_DAYS,
    max_results: int = MAX_FOLLOWUPS,
) -> str:
    """Find email threads where I sent the last message and no one has replied.

    Scans recently sent mail and keeps only threads whose most recent message
    was sent by me, meaning I'm still awaiting a reply.

    Args:
        min_days_ago: Only include threads whose last message is at least this
            many days old (gives the recipient time to respond). Default 3.
        max_days_ago: Ignore threads whose last message is older than this many
            days (too stale to chase). Default 14.
        max_results: Maximum number of threads to return. Default 10.
    """
    me = _get_my_address()
    # Sent by me, last activity within [min_days_ago, max_days_ago].
    query = f"in:sent newer_than:{max_days_ago}d older_than:{min_days_ago}d"
    results = _service.users().messages().list(
        userId="me", q=query, maxResults=max_results * 4,
    ).execute()
    messages = results.get("messages", [])

    seen_threads = set()
    awaiting = []
    for msg in messages:
        thread_id = msg.get("threadId")
        if not thread_id or thread_id in seen_threads:
            continue
        seen_threads.add(thread_id)

        thread = _service.users().threads().get(
            userId="me", id=thread_id, format="metadata",
            metadataHeaders=["From", "To", "Subject", "Date"],
        ).execute()
        thread_msgs = thread.get("messages", [])
        if not thread_msgs:
            continue

        last = thread_msgs[-1]
        headers = {h["name"]: h["value"] for h in last["payload"]["headers"]}
        last_from = parseaddr(headers.get("From", ""))[1].lower()
        # If someone replied after me, the last message won't be from me.
        if last_from != me:
            continue

        first_headers = {h["name"]: h["value"] for h in thread_msgs[0]["payload"]["headers"]}
        awaiting.append({
            "thread_id": thread_id,
            "to": headers.get("To", ""),
            "subject": first_headers.get("Subject", ""),
            "last_sent_date": headers.get("Date", ""),
            "message_count": len(thread_msgs),
            "snippet": last.get("snippet", ""),
        })
        if len(awaiting) >= max_results:
            break

    return json.dumps({"awaiting_reply": awaiting})


@beta_tool
def send_followup(thread_id: str, followup_text: str) -> str:
    """Send a follow-up message on an existing thread I'm awaiting a reply on.

    Args:
        thread_id: The Gmail thread ID (from find_sent_awaiting_reply).
        followup_text: The plain-text body of the follow-up message.
    """
    me = _get_my_address()
    thread = _service.users().threads().get(
        userId="me", id=thread_id, format="metadata",
        metadataHeaders=["From", "To", "Subject", "Message-ID", "References"],
    ).execute()
    thread_msgs = thread.get("messages", [])
    if not thread_msgs:
        return json.dumps({"status": "error", "reason": "empty thread", "thread_id": thread_id})

    last = thread_msgs[-1]
    headers = {h["name"]: h["value"] for h in last["payload"]["headers"]}
    last_from = parseaddr(headers.get("From", ""))[1].lower()
    if last_from != me:
        return json.dumps({
            "status": "skipped",
            "reason": "recipient already replied since last check",
            "thread_id": thread_id,
        })

    subject = headers.get("Subject", "")
    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    # Reply to the people I originally addressed (the "To" of my last message).
    recipient = headers.get("To", "")

    last_message_id = headers.get("Message-ID", "")
    references = headers.get("References", "")
    references = (references + " " + last_message_id).strip() if references else last_message_id

    mime = MIMEText(followup_text)
    mime["To"] = recipient
    mime["Subject"] = subject
    mime["In-Reply-To"] = last_message_id
    mime["References"] = references

    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
    _service.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": thread_id},
    ).execute()

    return json.dumps({"status": "sent", "thread_id": thread_id, "to": recipient})


# ── Agent loop ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an intelligent email assistant with access to Gmail.

Your job for each run:
1. List unread emails in the inbox.
2. For each email, fetch the full body.
3. Extract any relevant data (order numbers, requests, questions, etc.).
4. Decide whether to reply automatically:
   - Reply if the email contains a clear question or actionable request.
   - Mark as read (without replying) if it is a newsletter, notification, or does not need a response.
5. Keep replies professional, concise, and in the same language as the original email.
6. After processing all emails, output a JSON summary:
   {
     "processed": <count>,
     "replied": [{"id": ..., "subject": ...}],
     "skipped": [{"id": ..., "subject": ..., "reason": ...}],
     "extracted_data": [{"id": ..., "data": {...}}]
   }

Never reply to automated system emails, mailing lists, or spam.
"""


FOLLOWUP_SYSTEM_PROMPT = """You are an email assistant that sends polite follow-ups.

Your job for each run:
1. Call find_sent_awaiting_reply to get threads where I sent the last message and
   the recipient has not replied yet.
2. For each thread, decide whether a follow-up is warranted:
   - Send a follow-up if it looks like I asked a question or expected a response
     (a request, a proposal, a scheduling ask, etc.).
   - Skip threads that clearly don't need a nudge (e.g. I sent a "thanks" or a
     final acknowledgement, a one-way FYI, or an automated/no-reply recipient).
3. When following up, write a short, friendly, professional message that:
   - Gently references the previous email without repeating it verbatim.
   - Restates the specific ask or question so it's easy to respond to.
   - Matches the language of the original thread.
   - Never sounds pushy or guilt-trips the recipient.
4. After processing all threads, output a JSON summary:
   {
     "checked": <count>,
     "followed_up": [{"thread_id": ..., "subject": ..., "to": ...}],
     "skipped": [{"thread_id": ..., "subject": ..., "reason": ...}]
   }

Send at most one follow-up per thread per run.
"""


def _run(system_prompt, tools, user_message, banner):
    """Drive the tool_runner loop and print the agent's final summary."""
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=system_prompt,
        tools=tools,
        messages=[{"role": "user", "content": user_message}],
    )

    print(banner + "\n")
    final_text = ""
    for message in runner:
        for block in message.content:
            if hasattr(block, "text"):
                final_text = block.text

    print("=== Agent summary ===")
    print(final_text)


def run_followup_agent():
    global _service
    _service = get_gmail_service()
    _run(
        FOLLOWUP_SYSTEM_PROMPT,
        [find_sent_awaiting_reply, send_followup, get_email_body],
        "Check for emails awaiting a reply and send follow-ups where appropriate.",
        "Starting Gmail follow-up agent...",
    )


def run_agent():
    global _service
    _service = get_gmail_service()
    _run(
        SYSTEM_PROMPT,
        [list_unread_emails, get_email_body, send_reply, mark_as_read],
        "Process my unread emails now.",
        "Starting Gmail agent...",
    )


def main():
    parser = argparse.ArgumentParser(description="Gmail + Claude automation agent.")
    parser.add_argument(
        "mode",
        nargs="?",
        default="inbox",
        choices=["inbox", "followup"],
        help="inbox: process unread emails and auto-reply (default). "
             "followup: nudge sent threads still awaiting a reply.",
    )
    args = parser.parse_args()

    if args.mode == "followup":
        run_followup_agent()
    else:
        run_agent()


if __name__ == "__main__":
    main()
