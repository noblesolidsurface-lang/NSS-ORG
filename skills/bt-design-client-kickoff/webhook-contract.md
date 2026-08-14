# Webhook Contract: GHL "design agreement signed" → BuilderTrend kickoff

What this is: the exact shape the GHL side should POST when a design retainer agreement is signed. Written from the BT side so the GHL session can build against it without a follow-up conversation. **Receiver TBD — this is the contract, not a live endpoint.** Nothing is listening yet, and nothing on this side can call BuilderTrend on its own (BT is browser automation, no API), so the payload's job is to carry everything a human or a fresh Claude Code session needs to run `bt-design-client-kickoff` end to end.

Companion file: `ghl_payload_adapter.py` in this same folder turns a payload matching this contract into the Step 0 source-material block. If you change this contract, change that script.

## Transport

| | |
|---|---|
| Method | `POST` |
| Path | `https://hooks.nsshome.co/ghl/design-agreement-signed` **(placeholder — receiver TBD)** |
| Content-Type | `application/json; charset=utf-8` |
| Body | single JSON object, shape below. Never an array, never a batch. |
| Fires on | GHL Documents "document signed / completed" trigger for template `6a7eac06b50c34728f274d6a` in location `s5n8aTTdqzD7suFgNDC5`. One POST per signed agreement. |
| Success | any `2xx`. Treat anything else as a failure and retry. |
| Retries | up to 5 attempts, exponential backoff (1m, 5m, 30m, 2h, 6h). Same `event_id` every time — the receiver dedupes on it. |

## Auth

Baseline (build this): a static shared secret in a custom header on the GHL webhook action.

```
X-NSS-Webhook-Secret: <32+ char random string, generated once, stored in 1Password>
X-NSS-Event-Id: <uuid, stable across retries of the same signing>
X-NSS-Timestamp: <ISO-8601 UTC, when the event fired>
```

The receiver rejects with `401` if the secret header is missing or wrong, and ignores any request whose `X-NSS-Event-Id` it has already processed. Do not put the secret in the URL or a query string.

Optional upgrade if the sender can compute it: `X-NSS-Signature: sha256=<hex HMAC of the exact raw request body, keyed with the same secret>`. Better than a bearer-style static header because a leaked log line of the body alone can't be replayed. GHL's native webhook action can't do HMAC today, so treat this as a nice-to-have for whenever the POST goes through a small relay instead.

**Do not build this open.** An unauthenticated endpoint at a guessable path that kicks off client onboarding is a free way for anyone to inject a fake job into BuilderTrend.

## Payload

```json
{
  "event": "design_agreement.signed",
  "event_id": "3f9c1b8e-6d21-4a77-9f0c-2b1de4a70c55",
  "sent_at": "2026-08-14T18:04:11Z",
  "source": {
    "system": "gohighlevel",
    "location_id": "s5n8aTTdqzD7suFgNDC5",
    "template_id": "6a7eac06b50c34728f274d6a",
    "contact_id": "K3nTt9xQpL2vWzYb4Rc7",
    "opportunity_id": "Op9mVv1sD4hJ8kQe2Nw6",
    "document_url": "https://link.nsshome.co/documents/…signed.pdf"
  },
  "client": {
    "first_name": "Dana",
    "last_name": "Whitmore",
    "display_name": "Dana & Ross Whitmore",
    "email": "dana.whitmore@example.com",
    "phone": "+12535550188"
  },
  "project": {
    "scope": "Full kitchen remodel: new cabinetry, quartz counters, relocate range wall, full-height backsplash, new pantry. Powder bath refresh.",
    "address": {
      "line1": "4417 N Ferdinand St",
      "city": "Tacoma",
      "state": "WA",
      "postal_code": "98407",
      "raw": "4417 N Ferdinand St, Tacoma, WA 98407"
    },
    "budget_range": "$185,000 - $225,000"
  },
  "agreement": {
    "design_retainer": 4500,
    "retainer_percent": 2.2,
    "design_hourly_rate": 150,
    "agreement_date": "2026-08-14"
  }
}
```

### Field mapping

Keys are grouped for readability on the receiving end, but every value maps 1:1 to a live GHL field. Left column is what you send, right column is where it comes from.

| Payload key | GHL source | Field ID | Required | Notes |
|---|---|---|---|---|
| `event` | constant | — | yes | always the literal `design_agreement.signed` |
| `event_id` | GHL workflow execution id or a fresh uuid | — | yes | stable across retries, that's the whole point |
| `sent_at` | fire time | — | yes | ISO-8601 UTC, `Z` suffix |
| `source.location_id` | constant | — | yes | `s5n8aTTdqzD7suFgNDC5` |
| `source.template_id` | constant | — | yes | `6a7eac06b50c34728f274d6a` |
| `source.contact_id` | contact id | — | yes | so a human can jump straight to the record |
| `source.opportunity_id` | opportunity id | — | no | send if the workflow has it |
| `source.document_url` | signed doc link | — | no | strongly wanted: it's the attachment for the BT invoice step |
| `client.first_name` | `contact.first_name` | standard | yes | |
| `client.last_name` | `contact.last_name` | standard | yes | drives the BT job title, so it can't be blank |
| `client.display_name` | `contact.full_name` | standard | no | send for couples, e.g. `Dana & Ross Whitmore` |
| `client.email` | `contact.email` | standard | yes | |
| `client.phone` | `contact.phone` | standard | no | E.164 preferred |
| `project.scope` | `contact.project_scope` | `Jxm6OnhjhVwNCREfReRS` | yes | LARGE_TEXT, send verbatim, newlines intact |
| `project.address.*` | `contact.project_address` | `bNC8rLpRbD2s2gyETwQu` | yes | see address note below |
| `project.budget_range` | `contact.budget_range` | `7mSdd9jCkLnVbaM2ngSO` | yes | string is fine, e.g. `$185,000 - $225,000` |
| `agreement.design_retainer` | `contact.design_retainer` | `jlwQSwVFoUtbFMldLPBd` | yes | number preferred; `"$4,500"` is accepted and parsed |
| `agreement.retainer_percent` | `contact.retainer_percent` | `47cQOznZbQ3QjtgFxwK6` | no | number, percent units (`2.2` = 2.2%) |
| `agreement.design_hourly_rate` | `contact.design_hourly_rate` | `RKIEXkSzkvD62OzNvs9Q` | no | usually `150` |
| `agreement.agreement_date` | `contact.agreement_date` | `JIxlH4wEJpjkL5DOkimG` | yes | `YYYY-MM-DD` |

**Address:** BuilderTrend requires a zip to save a job, so send the parsed components whenever GHL has them. If the only thing available is the single-line `project_address` custom field, send it as `project.address.raw` and set the other four to `null` — the adapter does a best-effort split and flags it as unverified rather than failing. Prefer `project_address` over the contact's `full_address`: the project site and the client's mailing address are frequently different, and BT wants the project site.

**Nulls and empties:** send `null` for anything genuinely unknown. Don't send the literal strings `""`, `"N/A"`, or an unrendered merge tag like `{{contact.budget_range}}` — an unrendered tag looks like real data downstream and is worse than a null.

## What happens on receipt (informational — no server exists yet)

Whenever a receiver gets built, this is the intended behavior, in order:

1. Verify `X-NSS-Webhook-Secret`. Wrong or missing → `401`, log, stop.
2. Dedupe on `X-NSS-Event-Id`. Already seen → `200` with no side effects, so retries are safe.
3. Persist the raw body to disk verbatim, before parsing anything. That file is the audit trail if a field turns out wrong later.
4. Run `ghl_payload_adapter.py` over it to render the Step 0 source-material block.
5. Surface that block to Kyle (file on Desktop, email, or a notification) so it can be pasted into a fresh Claude Code session running `bt-design-client-kickoff`.
6. Return `200`.

The receiver never touches BuilderTrend itself. BT is driven by browser automation through the Claude-in-Chrome extension, which only exists inside a live Claude Code session — so the last mile stays a human starting a session with this block in hand.

## Explicitly out of scope for the GHL side

- Creating anything in BuilderTrend. GHL fires and forgets.
- Deciding whether the retainer was actually paid. The payload says an agreement was signed, nothing more. Payment confirmation (Joist invoice number, method) is still gathered on the BT side.
- Formatting for humans. Send structured data, let the adapter do the prose.
