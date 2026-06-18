"""
Gmail + Claude automation: read emails, extract data, auto-reply.

Setup:
  1. Create a Google Cloud project, enable Gmail API, download credentials.json
  2. Set ANTHROPIC_API_KEY in .env
  3. pip install -r requirements.txt
  4. python gmail_claude.py  (first run opens browser for OAuth)
"""

import os
import base64
import json
from email.mime.text import MIMEText
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


def run_agent():
    global _service
    _service = get_gmail_service()

    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        tools=[list_unread_emails, get_email_body, send_reply, mark_as_read],
        messages=[{"role": "user", "content": "Process my unread emails now."}],
    )

    print("Starting Gmail agent...\n")
    final_text = ""
    for message in runner:
        for block in message.content:
            if hasattr(block, "text"):
                final_text = block.text

    print("=== Agent summary ===")
    print(final_text)


if __name__ == "__main__":
    run_agent()
