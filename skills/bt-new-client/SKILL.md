---
name: bt-new-client
description: Onboard a new NSS Home client into BuilderTrend fast. Creates the ROM job + client contact (no portal invite) the moment a prospect becomes a design client / ROM is presented. Part 2 adds the Design Retainer line item to the job's Estimate and generates the customized Design Agreement from Kyle's standard template. Use when Kyle says "new ROM client", "add [name] to buildertrend", "bt new client", "onboard [name]", "design retainer for [job]", "design agreement for [job]", or pastes client info for a new design job. Handles one client or a batch list.
---

# BT New Client: ROM Job + Contact Onboarding

Purpose: get a new design client into BuilderTrend (Noble Solid Service account) in under 3 minutes. One job shell + one client contact, no portal invite. This is the CRM onboarding step that fires when a ROM is presented.

## Data needed per client (ask for anything missing, in ONE question)

| Field | Required | Notes |
|---|---|---|
| Client first + last name | yes | couples: First = "Kari Lou & Justin", Last = "Pavlovich" |
| Job title | yes | format: `ROM - LastName - Scope`. If no scope given, use `ROM - LastName - Remodel`. Don't ask about scope, it's cosmetic. |
| Project address (street, city, state, zip) | yes | zip is BT-required |
| Email | strongly wanted | job saves without it, but get it if Kyle has it |
| Phone | nice to have | skip if unknown, don't block |

Job TYPE does not matter. Always select "Whole Home Remodel" (reliable filter: type "whole"). Never ask Kyle about type.

If Kyle says the info is "in joist": search pro.joistapp.com/dashboard/clients. Use `find` for the search box ref, then `form_input` to set the search value (click+type does NOT trigger Joist's filter), then `get_page_text`. But don't make Joist a requirement: pasted info is faster and preferred.

## Prerequisites

- Real Chrome connected via Claude-in-Chrome extension, logged into buildertrend.net (and pro.joistapp.com if scrubbing Joist)
- If the extension drops mid-run, retry once: it's usually transient

## The BT flow (per client, ~6 tool calls)

**Golden rules learned the hard way:**
1. ALWAYS click fields by accessibility ref (`read_page` filter interactive, or `find`). NEVER pixel coordinates: the page scrolls unpredictably and repaints stale screenshots.
2. The Add Job form WIPES all input when its background data-fetch settles (~5-10s after load, timing varies). Fill the form, screenshot, and if it came back blank, just fill it again: the second pass always sticks. Budget for the double-fill, don't fight it.
3. Save with `cmd+s`, never the Save button (clicks on it frequently don't register).
4. After saving a contact, a "Client contact" summary modal often reopens and SWALLOWS cmd+s. Close it first (find the dialog Close button ref), then cmd+s.
5. Verify saves by screenshot: look for the "Job saved" / "Contact Saved" toast and the title changing from "Add Job / Draft" to the job name with "Open" badge.

**Steps:**

1. `navigate` to `https://buildertrend.net/app/JobPage/0/1?openCondensed=true` (direct Add Job form), wait ~6s, `read_page` (interactive) to get refs. Typical refs: Title=first labeled textbox, Type=combobox "Type", address=the 4 unlabeled textboxes after Type's Manage link (street, city, state, then zip after an Info button).
2. Fill by ref-click + type: Title, street, city, state, zip. Then Type combobox: click ref, type `whole`, wait 1.5s, press Down, press Return. (If Return grabs the wrong option because the filter reset, cmd+a, retype `whole`, wait, click the single filtered option.)
3. Screenshot. If wiped (all blank, schedule color changed), refill: same refs still work.
4. Press Escape (close type dropdown), click the Clients tab ref, wait, `find` the "+ Contact" button, click it, wait 3s, `read_page` to get the dialog refs (First name, Last name, 4 address textboxes, Phone, Primary email, and the footer's second button = Save).
5. Fill contact by ref-click + type: first, last, street, city, state, zip, phone, email. Display name auto-fills from first+last; override it only for couples/odd cases (click, cmd+a, retype). Screenshots may paint-lag behind the dialog: trust the ref actions, verify on the next capture.
6. Click the dialog Save ref, wait 3s. CRITICAL: do NOT touch "Send invite". Login Access stays Inactive. Kyle never wants portal invites at ROM stage.
7. Close the contact summary modal if it reopened (Close ref), then `cmd+s`, wait 5s, screenshot. Confirm "Job saved" toast + job title with Open badge. A yellow "unable to link to QuickBooks" banner is normal and harmless: ROM jobs don't get QB-linked.

## Batch mode

For multiple clients, loop the flow. Report progress per job ("3 of 5 saved"). At the end, verify by loading `https://buildertrend.net/app/Landing` and checking the open-jobs count went up by the batch size.

## Part 2: Design Phase (estimate line item + agreement)

Runs when the ROM is being presented. Kyle triggers it with the retainer amount ("design retainer for Hogan, 3500") or as part of onboarding if he gives the numbers up front.

**Extra data needed (ask in ONE question if missing):**
- Retainer amount (= design fee; the "Full Design & Feasibility Study" number)
- Preliminary construction budget range (low - high)
- Scope description (rooms/areas list, e.g. "Kitchen, Primary Bath, Laundry")
- Project title (e.g. "Full Office Remodel"; default `{Scope} Remodel`)

**2a. Estimate line item in BT:** follow `design-estimate-lineitem.md` in this skill folder. One line: "Design Retainer" at the retainer amount, description = the NSS Design Process block with placeholders filled. No markup, no send-to-budget, nothing sent to the client.

**2b. Design Agreement:** fill `design-agreement-template.md` (same folder) with the job's fields. NEVER reword the numbered legal sections: only placeholders change. Flag the two known source-doc quirks (stray "august 2023" date in Section 2, "this contact" in Section 3) every time until Kyle rules on them. Output a Word doc via the docx skill (or PDF if Kyle asks) saved to ~/Desktop as `Design Agreement - {LastName}.docx` for Kyle to review, sign, and upload to the BT job's Files. Do not email or send it anywhere.

## Report back

One line per client: job name, client name, email/phone captured, address, and (if Part 2 ran) retainer amount + agreement file path. Flag anything missing (no email, unconfirmed address, unanswered template quirks) so Kyle can backfill. Start the response with "ok kyle" per global rules, colons not em dashes.
