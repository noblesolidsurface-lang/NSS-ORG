#!/usr/bin/env python3
"""Turn a signed-design-agreement webhook payload into bt-design-client-kickoff Step 0 input.

Reads one JSON object matching `webhook-contract.md` (same folder) and prints the
source-material block a human would otherwise paste into a fresh Claude Code session
to kick off `bt-design-client-kickoff`. Structured fields in, pasteable text out.

Python 3 stdlib only, no third-party imports. Verified on python3.9.

USAGE
    ghl_payload_adapter.py [--file PATH] [--out PATH] [--strict]

    --file PATH   read the payload from PATH. Omit to read JSON from stdin.
    --out PATH    write the block to PATH as well as printing it.
    --strict      exit 2 if any contract-required field is missing or empty.
                  Default is lenient: missing fields render as "** MISSING **"
                  and land in the open-questions list, since a partial block is
                  still more useful than no block.

    cat signed.json | ghl_payload_adapter.py
    ghl_payload_adapter.py --file signed.json --out ~/Desktop/whitmore-step0.txt

EXIT CODES
    0  block rendered
    1  bad input (unreadable file, invalid JSON, payload isn't an object)
    2  --strict and something required was missing

WORKED EXAMPLE
    Loosely patterned on the Carol Buckingham kitchen job this skill was proven on,
    with invented placeholder details. Input:

        {
          "event": "design_agreement.signed",
          "event_id": "3f9c1b8e-6d21-4a77-9f0c-2b1de4a70c55",
          "sent_at": "2026-08-14T18:04:11Z",
          "source": {
            "system": "gohighlevel",
            "location_id": "s5n8aTTdqzD7suFgNDC5",
            "template_id": "6a7eac06b50c34728f274d6a",
            "contact_id": "K3nTt9xQpL2vWzYb4Rc7",
            "document_url": "https://link.nsshome.co/documents/whitmore-signed.pdf"
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
              "line1": "4417 N Ferdinand St", "city": "Tacoma",
              "state": "WA", "postal_code": "98407",
              "raw": "4417 N Ferdinand St, Tacoma, WA 98407"
            },
            "budget_range": "$185,000 - $225,000"
          },
          "agreement": {
            "design_retainer": 4500, "retainer_percent": 2.2,
            "design_hourly_rate": 150, "agreement_date": "2026-08-14"
          }
        }

    Output is the "=== NSS DESIGN CLIENT KICKOFF" block, with a BT job title of
    `ROM - Whitmore - Kitchen` derived from the last name plus the scope text.
"""

import argparse
import json
import re
import sys

MISSING = "** MISSING **"

# Scope keywords worth putting in the BT job title, checked in this order.
# bt-new-client: title format is `ROM - LastName - Scope`, scope is cosmetic.
SCOPE_KEYWORDS = [
    ("kitchen", "Kitchen"),
    ("primary bath", "Primary Bath"),
    ("master bath", "Primary Bath"),
    ("powder", "Powder Bath"),
    ("bath", "Bath"),
    ("whole home", "Whole Home"),
    ("whole house", "Whole Home"),
    ("adu", "ADU"),
    ("basement", "Basement"),
    ("laundry", "Laundry"),
    ("office", "Office"),
    ("addition", "Addition"),
    ("deck", "Deck"),
    ("exterior", "Exterior"),
]

# Things Kyle reliably adds by hand that no GHL field will ever carry.
# Straight out of the skill's Step 3 "gap" notes — surface them up front so he
# answers them in one pass instead of editing a draft that looks finished.
STANDING_QUESTIONS = [
    "Preferred vendor per category (appliances, cabinets, countertops)? Assume there IS one unless told otherwise.",
    "Any scope item above that's OPTIONAL / an upsell rather than firm? The agreement text won't distinguish.",
    "Scan/measure ordered yet (Canva/Twindo)? Routine at this stage, never in the source material.",
    "Retainer paid through Joist? Need the Joist invoice number + payment method for the BT invoice copy.",
    "Which internal people get the handoff email, and which designer is this going to?",
    "Anything walked on site that isn't in the scope text above (wing walls, removals, structural)?",
]


def _clean(value):
    """Normalize a payload value to a trimmed string, or None if it's effectively empty."""
    if value is None:
        return None
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip()
    if not text:
        return None
    if text.lower() in ("n/a", "na", "none", "null", "-"):
        return None
    # An unrendered merge tag is worse than a null: it reads like real data.
    if re.match(r"^\{\{.*\}\}$", text):
        return None
    return text


def _get(payload, path, default=None):
    """Fetch a dotted path out of nested dicts, cleaning the result."""
    node = payload
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    cleaned = _clean(node)
    return default if cleaned is None else cleaned


def _money(value):
    """Render 4500, '4500', or '$4,500.00' as '$4,500.00'. Pass odd input through as-is."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    else:
        stripped = re.sub(r"[^0-9.\-]", "", str(value))
        if not stripped:
            return str(value)
        try:
            number = float(stripped)
        except ValueError:
            return str(value)
    return "${:,.2f}".format(number)


def parse_address(address):
    """Return (line1, city, state, zip, unverified_flag).

    Prefers the parsed components. Falls back to a best-effort split of `raw`,
    which BT needs because a job won't save without a zip.
    """
    if not isinstance(address, dict):
        address = {}
    line1 = _clean(address.get("line1"))
    city = _clean(address.get("city"))
    state = _clean(address.get("state"))
    postal = _clean(address.get("postal_code"))
    raw = _clean(address.get("raw"))

    if line1 and city and state and postal:
        return line1, city, state, str(postal), False

    if raw:
        # "4417 N Ferdinand St, Tacoma, WA 98407" and close variants.
        match = re.match(
            r"^\s*(?P<line1>.+?)\s*,\s*(?P<city>[^,]+?)\s*,\s*"
            r"(?P<state>[A-Za-z]{2})\.?\s+(?P<zip>\d{5}(?:-\d{4})?)\s*$",
            str(raw),
        )
        if match:
            return (
                line1 or match.group("line1"),
                city or match.group("city"),
                state or match.group("state").upper(),
                postal or match.group("zip"),
                True,
            )
        return (line1 or raw, city, state, postal, True)

    return line1, city, state, postal, bool(line1 or city or state or postal)


def scope_label(scope):
    """Short cosmetic scope word for the BT job title."""
    if not scope:
        return "Remodel"
    low = str(scope).lower()
    hits = []
    for needle, label in SCOPE_KEYWORDS:
        if needle in low and label not in hits:
            hits.append(label)
    # Drop generic labels swallowed by a more specific one ("Bath" vs "Primary Bath").
    hits = [h for h in hits if not any(h != other and h in other for other in hits)]
    if hits:
        return " + ".join(hits[:2])
    first = str(scope).strip().splitlines()[0].strip(" .:-")
    return (first[:40] if first else "Remodel")


def render(payload, strict=False):
    """Build the Step 0 block. Returns (text, list_of_missing_required_fields)."""
    first = _get(payload, "client.first_name")
    last = _get(payload, "client.last_name")
    display = _get(payload, "client.display_name") or " ".join(
        p for p in (first, last) if p
    )
    email = _get(payload, "client.email")
    phone = _get(payload, "client.phone")

    scope = _get(payload, "project.scope")
    budget = _get(payload, "project.budget_range")
    line1, city, state, postal, addr_unverified = parse_address(
        (payload.get("project") or {}).get("address")
        if isinstance(payload.get("project"), dict)
        else None
    )

    retainer = _money(_get(payload, "agreement.design_retainer"))
    percent = _get(payload, "agreement.retainer_percent")
    hourly = _money(_get(payload, "agreement.design_hourly_rate"))
    signed_on = _get(payload, "agreement.agreement_date")

    contact_id = _get(payload, "source.contact_id")
    doc_url = _get(payload, "source.document_url")
    event_id = _get(payload, "event_id")
    sent_at = _get(payload, "sent_at")

    missing = []
    for label, value in (
        ("client.first_name", first),
        ("client.last_name", last),
        ("client.email", email),
        ("project.scope", scope),
        ("project.budget_range", budget),
        ("project.address (street/city/state/zip)", postal and line1),
        ("agreement.design_retainer", retainer),
        ("agreement.agreement_date", signed_on),
    ):
        if not value:
            missing.append(label)

    def show(value):
        return value if value else MISSING

    job_title = "ROM - {} - {}".format(last or "LASTNAME", scope_label(scope))

    lines = []
    lines.append("=== NSS DESIGN CLIENT KICKOFF - SOURCE MATERIAL ===")
    lines.append(
        "Source: GHL design agreement, e-signed. This is Step 0 source #1: structured data "
        "from the agreement the client actually signed. It outranks a chat paste, a Joist PDF, "
        "Granola notes and Apple Notes. Don't go re-derive any of it."
    )
    lines.append(
        "Provenance: event {} | fired {} | GHL contact {}".format(
            show(event_id), show(sent_at), show(contact_id)
        )
    )
    if doc_url:
        lines.append("Signed document: {}".format(doc_url))
    lines.append("")

    lines.append("CLIENT")
    lines.append("  First name:        {}".format(show(first)))
    lines.append("  Last name:         {}".format(show(last)))
    lines.append("  Display name:      {}".format(show(display)))
    lines.append("  Email:             {}".format(show(email)))
    lines.append("  Phone:             {}".format(show(phone) if phone else "(none on file)"))
    lines.append("")

    lines.append("PROJECT ADDRESS (job site, not mailing)")
    lines.append("  Street:            {}".format(show(line1)))
    lines.append("  City:              {}".format(show(city)))
    lines.append("  State:             {}".format(show(state)))
    lines.append("  Zip:               {}".format(show(postal)))
    if addr_unverified:
        lines.append(
            "  !! Address was split from a single-line field, not sent pre-parsed. "
            "Eyeball it before saving the BT job: a wrong zip blocks the save."
        )
    lines.append("")

    lines.append("BT JOB")
    lines.append("  Job title:         {}".format(job_title))
    lines.append("  Job type:          Whole Home Remodel (always, per bt-new-client)")
    lines.append("  Portal invite:     NO. Login Access stays Inactive.")
    lines.append("")

    lines.append("SCOPE (verbatim from the signed agreement)")
    if scope:
        for line in str(scope).splitlines():
            lines.append("  {}".format(line.rstrip()))
    else:
        lines.append("  {}".format(MISSING))
    lines.append("")

    lines.append("MONEY")
    lines.append("  Design retainer:   {}".format(show(retainer)))
    lines.append("  Construction budget (preliminary): {}".format(show(budget)))
    lines.append(
        "  Retainer as % of budget: {}".format(
            "{}%".format(percent) if percent not in (None, "") else "(not sent)"
        )
    )
    lines.append(
        "  Design hourly rate: {}".format("{}/hr".format(hourly) if hourly else "(not sent)")
    )
    lines.append("  Agreement signed:  {}".format(show(signed_on)))
    lines.append("")

    lines.append("WHAT TO RUN")
    lines.append("  bt-design-client-kickoff, starting at Step 1.")
    lines.append("  Step 1: bt-new-client Part 1 (job + contact). Skip Part 2b - the design")
    lines.append("          agreement is already signed in GHL, do not regenerate it.")
    lines.append("  Step 2: BT invoice mirroring the payment doc, Save (not Send), record payment.")
    lines.append("  Step 3: internal recap email + designer-forward draft + recap doc.")
    lines.append("")

    lines.append("OPEN QUESTIONS FOR KYLE (this payload can't answer these)")
    for question in STANDING_QUESTIONS:
        lines.append("  - {}".format(question))
    if missing:
        lines.append("")
        lines.append("  Missing from the webhook payload, needed before/while running:")
        for field in missing:
            lines.append("  - {}".format(field))
    lines.append("")
    lines.append("=== END SOURCE MATERIAL ===")

    return "\n".join(lines), missing


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Render bt-design-client-kickoff Step 0 source material from a signed "
            "design-agreement webhook payload (see webhook-contract.md)."
        )
    )
    parser.add_argument("--file", help="payload JSON file; omit to read stdin")
    parser.add_argument("--out", help="also write the rendered block to this path")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 2 if any contract-required field is missing",
    )
    args = parser.parse_args(argv)

    try:
        if args.file:
            with open(args.file, "r") as handle:
                raw = handle.read()
        else:
            raw = sys.stdin.read()
    except IOError as exc:
        sys.stderr.write("could not read payload: {}\n".format(exc))
        return 1

    if not raw.strip():
        sys.stderr.write("no payload on stdin (use --file PATH, or pipe JSON in)\n")
        return 1

    try:
        payload = json.loads(raw)
    except ValueError as exc:
        sys.stderr.write("payload is not valid JSON: {}\n".format(exc))
        return 1

    if not isinstance(payload, dict):
        sys.stderr.write("payload must be a single JSON object, not a list or scalar\n")
        return 1

    event = payload.get("event")
    if event and event != "design_agreement.signed":
        sys.stderr.write(
            "warning: event is '{}', expected 'design_agreement.signed'\n".format(event)
        )

    text, missing = render(payload, strict=args.strict)
    sys.stdout.write(text + "\n")

    if args.out:
        try:
            with open(args.out, "w") as handle:
                handle.write(text + "\n")
            sys.stderr.write("wrote {}\n".format(args.out))
        except IOError as exc:
            sys.stderr.write("could not write --out file: {}\n".format(exc))
            return 1

    if args.strict and missing:
        sys.stderr.write(
            "strict: {} required field(s) missing: {}\n".format(len(missing), ", ".join(missing))
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
