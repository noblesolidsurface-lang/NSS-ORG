# BT Design Client Kickoff: Full Onboarding After a Signed Design Retainer

Purpose: everything that fires the moment a design client signs and pays their design retainer (via Joist, typically): BT job + contact (already covered by [[bt-new-client]] — run that first), a BT invoice that mirrors the Joist doc exactly and is marked paid, a team handoff email with the scope/investment ready to forward to the designer, and a full recap doc. Built and proven live on the Carol Buckingham kitchen remodel (2026-08-12).

Trigger phrases: "new design client", "[name] signed the retainer", "onboard [name]", "create the invoice for [job]", "kickoff for [name]".

## Step 0: Gather source material before touching any system

You need, in this order of reliability:
1. **Whatever Kyle pastes directly in chat** (Granola scope notes, Canva proposal screenshots, payment confirmation screenshots). This is ALWAYS the primary source — don't second-guess it against a live API pull.
2. **The Joist PDF** (design agreement + invoice) if Kyle uploads or references one — `Read` it directly, it contains the client's real name/address/phone and the exact signed scope, which is more authoritative than a Granola summary. Real client names are often anonymized as "note-taker" in Granola auto-summaries — the Joist doc has the real name.
3. **Granola transcripts** (`mcp__617d53a5...get_meeting_transcript`) — **gated behind a paid Granola tier**, will usually error with "Transcripts are only available to paid Granola tiers." Don't burn time retrying; fall back to #1.
4. **Apple Notes** (`list_notes` then `get_note_content`) — `list_notes` takes no search query, it just returns ~20 most-recent notes by title. Scan titles for the client's last name or address before assuming a note doesn't exist. `get_note_content` takes a `note_name` param (not `name`).

**Verify team member emails, don't trust memory.** Internal team names Kyle uses in chat (e.g. "Lacy", "Thomas") may not match the email address in a stale memory file — GHL sub-user emails and BuilderTrend/company emails for the same person can differ (e.g. a personal gmail used for one system, `@nssbuilt.com` for another). Cross-check via `mcp__a0a6c25a...search_threads` with `query: "<FirstName> <LastName>"` and use whatever domain shows up in real recent correspondence. Also cross-check against the job's **Internal users** tab in BT (Clients tab neighbor) — real employees show up there with their full name, confirming who's actually on the team.

## Step 1: BT job + contact

Run [[bt-new-client]] Part 1 exactly as documented. Skip Part 2b (Design Agreement generation) if the client already signed a design agreement via Joist — that's already done, don't regenerate it.

## Step 2: BT invoice matching the Joist doc, marked paid

This is new territory beyond bt-new-client's estimate-line-item flow — it's a real Financial > Invoices record, not an Estimate line.

**Navigate:** hover (don't just click — a plain click can land on the wrong already-open submenu from residual mouse state) the **Financial** top-nav item, wait ~1s for the panel, then click **Invoices**. This goes to `/app/OwnerInvoices`, a *global* invoice list scoped to whatever job was last selected — it will NOT default to your job.

**Select the right job:** the left sidebar job list may be scoped to a saved filter ("VIEW 1 OPEN AND WARRANTY JOB" or similar) that silently excludes a brand-new job. If searching the client's last name returns "no results," click **Clear Search** (via `find`, not coordinates) to reset to "ALL N JOBS," then search again — the fresh job now appears (often with a green **QB** badge meaning it's already QuickBooks-linked).

**Click "+ Invoice."** This opens a modal that renders in **two visual stages**: a small/narrow version appears first (~1-2s), then it resizes and recenters to full width. If you type into the narrow version, the resize wipes it. Always: click "+ Invoice," wait 2-3s, screenshot to confirm the FULL-WIDTH modal is showing, THEN start typing. Get fresh refs via `read_page`/`find` after every modal reflow — stale coordinates from the small-modal screenshot land on the wrong element after resize.

**Title, invoice date, tax, price** — fill via ref-click (not coordinates) one field at a time with a short screenshot check between the first couple, since this modal reflows more than most BT forms:
- Title textbox: plain click + type, sticks fine once the modal is settled.
- Invoice date: click the date field, type `MM/DD/YYYY`, then **click the highlighted day number in the popup calendar** to close it — do NOT press Escape. Escape on this modal is bound to "close the whole invoice" and pops an "Unsaved changes?" dialog that wipes your date if you're not careful. If that dialog appears, click its **X** (top-right of the small dialog, not "Don't save") to cancel the exit and keep editing.
- Switching **Line items → Flat fee** (or back) shows a confirm dialog "Switch to flat fee? All line items will be removed permanently upon save." — click **Use flat fee** to proceed. Do this switch *before* entering the price.
- Client price: click the `$` field, type the base number (e.g. `3500`), press Tab. Subtotal/Tax/Total recompute live.

**Tax mismatch vs. the external doc is common and expected.** BT's built-in "WA-Tacoma-L2717" (or similar) shared rate is the *official* WA DOR combined rate and will often differ slightly from what a Joist/other proposal tool computed (e.g. BT's 10.5% vs. Joist's 10.55% on the Buckingham job — a $1.75 difference on $3,500). **Do not edit the shared tax rate** — other jobs depend on it being the real DOR rate. Instead:
1. Financial > Invoices > open the invoice > click **Manage** next to Taxes.
2. Click **+ Tax rate**, name it something identifiable like `WA-<City>-Joist Match`, set the exact percentage needed to reproduce the external total (solve `rate = external_tax / base_price`), tax agency `WA Dept of Revenue`, save.
3. Close the Taxes dialog (X, top right — not Escape), back on the invoice reopen the Taxes dropdown, type a keyword from the new rate's name, select it. Total now matches exactly.

If Kyle says "make the numbers match" after seeing a mismatch, this tax-rate-clone is the fix — never fudge the base price to force a match, that misrepresents the actual retainer/contract amount.

**Title convention when the invoice is a copy of an external doc:** rename the Title to include a note, e.g. `Design Retainer (copy of Joist invoice #86855)` — makes it unambiguous in the invoice list that this BT record isn't the original source of truth.

**Save (not Send)** if the client already paid outside BT — Send would push a live payment-request email to the client for something already settled. Bottom-right **Save** button.

**Record the payment:** reopen the saved invoice, click **Record payment**. Defaults are usually already correct (Date Paid = today, Balance Due = full amount, Payment Method = Credit Card if the source doc says "Credit Card or PayPal", Received By = you). Leave **Notify client unchecked** — they already know they paid, a BT payment-recorded email is redundant/confusing. Click **Record $X Payment** then **Confirm**.

**Notes:** the invoice's **Internal notes** field is a plain textbox that in practice would not reliably accept typed input in this session (repeated attempts reverted to view mode with the text unsaved — possibly a custom widget quirk). Don't burn time fighting it. Instead put the "paid via Joist, not through BT" note in the **Invoice description** rich-text field — that field saves normally on the first try and is exactly as effective for the "mark as paid in notes" ask.

**Attach the source document:** click **Attachments > Add** in the invoice edit view. This opens an "Upload Files" dialog. **Never click "Browse device"** — it opens a native OS file picker automation tools can't see or drive. Instead: `find` the hidden file input (`query: "file input for uploading files (hidden input type=file)"`), then call `mcp__claude-in-chrome__file_upload` with that ref and the local file path directly — skips the picker entirely. Click **Upload** in the dialog once the file shows as attached, then **Save** the invoice. Uploaded invoice attachments auto-sync into the job's **Files > Documents > Attached Documents > Owner Invoices** folder — no separate upload to Files needed to make the source doc discoverable there too.

## Step 3: Team handoff emails + recap file

**Email client is Apple Mail, never Gmail — no exceptions, even though Kyle's account address is a gmail.com one.** See [[kyle-uses-apple-mail-not-gmail]]. Drive Mail.app via `mcp__Control_your_Mac__osascript`. For any body longer than a couple lines, write it to a scratch `.txt` file first and read it into the AppleScript with `read POSIX file "<path>" as «class utf8»` rather than inlining a huge quoted string — cleaner escaping, no risk of a stray quote breaking the script. Pattern:
```applescript
set bodyText to read POSIX file "/path/to/body.txt" as «class utf8»
tell application "Mail"
	activate
	set newMessage to make new outgoing message with properties {subject:"...", content:bodyText, visible:true}
	tell newMessage
		make new to recipient at end of to recipients with properties {address:"someone@nssbuilt.com"}
	end tell
end tell
```
`visible:true` opens the compose window so Kyle can see and edit it immediately — never call a send action unless he explicitly asks the email to actually go out.

**This step produces TWO distinct drafts, not one** — don't conflate them:

1. **Internal team recap email** — to whichever internal people Kyle names (verified real addresses per Step 0), full detail: scope, investment, process/pricing internals (draw percentages, Trades Day mechanics, permit notes), open decisions, next steps. This is Kyle's team briefing, so contractor-internal financial mechanics belong here.

2. **"Forward to the designer" draft** — also addressed to the internal team (Kyle forwards through people, not directly to outside vendors, unless he says otherwise), but the *content* is written as if speaking directly to the designer, with a one-line instruction at the top ("Please forward the block below to Sheila"). This version must be scoped to only what the designer actually needs: client contact, the scope itself, budget context so she can plan selections, and anything that affects her scheduling or design choices (e.g. client's travel dates, undecided items she should raise in her first meeting). **Cut everything internal-only**: payment draw percentages, Trades Day/fixed-price mechanics, and — the mistake made live on the Buckingham job — self-referential lines like "add the client to the chat with [the designer]" written INTO the content meant to go TO that same designer. Read the draft back once as if you were the external recipient before finalizing; anything that only makes sense from Kyle's internal seat gets cut.

If Kyle says a draft has "stupid" stuff in it, it's almost always this: internal-only content that leaked into an external-facing version. Rewrite for the audience, don't just trim word count.

**Treat the designer-forward draft as a strong first pass, not a finished email — Kyle will layer in business judgment your source material doesn't contain.** Verified live on Buckingham by comparing the draft against what Kyle actually sent Sheila. The gap wasn't tone, it was *missing information a Granola/Canva summary never captures*:
- **A preferred vendor.** Kyle added "I prefer to use Albert Lee" for appliances — a standing vendor preference, not something the client said. If a category (appliances, cabinets, countertops) doesn't name a vendor in your source material, don't assume there isn't one — flag it as a question ("confirm preferred appliance vendor") rather than omitting the line, since Kyle has default vendors for most categories that just weren't in the meeting notes.
- **Optional vs. firm scope.** Draft had "full-height backsplash" as committed scope; Kyle changed it to "(AS AN OPTION)." Site-visit notes often don't distinguish "will do" from "offered as an upsell" — when scope items feel like standard-but-not-explicitly-confirmed inclusions, hedge them as options rather than firm commitments, or flag the ambiguity instead of picking a side.
- **Construction details Kyle knows but didn't dictate into Granola.** He added "and remove wing wall in kitchen" to the pantry line — a real scope item that never appeared in any source material this session had access to. The meeting notes are not a complete scope; expect the person who walked the site to add things a transcript missed.
- **Curation instructions to the trade, misattributed as client preference.** Draft said budget context was about the *client* not wanting to max out every line; Kyle's actual reason was "don't want to show her certain cabinet lines or doors" — that's Kyle directing Sheila's presentation, not restating what Carol said. When budget/selection guidance doesn't have a clear client quote behind it, don't invent a client-motivation frame for it — state it as guidance to the designer instead.
- **Standing kickoff steps that aren't in any one client's notes.** Kyle added "I already took the liberty of ordering the scan from Canva/Twindo for the kitchen" — a 3D scan/measure service he orders as a matter of course at this stage. Ask whether a scan/measure service has been ordered as part of Step 0 gathering, since it's apparently a routine kickoff action that won't show up in Granola or Canva content.

Net: don't try to eliminate this gap by guessing harder — call out the categories above as open questions in the draft itself if the source material is silent on them (preferred vendor per category, firm-vs-optional on ambiguous scope items, whether a scan's been ordered) so Kyle catches them in one edit pass instead of the draft looking "finished" while quietly missing his real business logic.

**Cut just as aggressively as you add.** Confirmed on the same comparison — Kyle also *removed* things the draft had: a closing line asking the designer to confirm a measure-meeting date and loop him in, and a specific brand exclusion ("no Sub-Zero") folded into a plain budget number instead. The pattern: this email is a one-way information handoff, not a request for a reply or a status check-in — don't add closing asks/CTAs ("let me know when...", "confirm and I'll...") unless Kyle's source material explicitly wants a response tracked. Keep brand/vendor specifics only when they're a real standing preference (see Albert Lee above), not as a default "also mention what NOT to use" reflex — one clear preferred vendor beats a preferred vendor plus a list of excluded ones.

**The bigger recap document** (client info, full scope, full line-item construction ROM breakdown, process/pricing, open decisions, next steps) — build as a `.docx` via **python-docx**, not the `docx` (npm/docx-js) skill's default approach: this machine has no `node`, `pandoc`, or `soffice` installed, only `python3`. Check with `python3 -c "import docx"` before assuming either toolchain is available; if neither is, plain Markdown is an acceptable fallback but docx via python-docx is preferred when available (it is, as of 2026-08-12) since it reads professionally when opened in Word/Google Docs by the designer.

**Attaching files:** for Apple Mail drafts, attach directly in the AppleScript rather than skipping the attachment — Mail.app attachments don't have the base64-context-cost problem the Gmail API attachment path has, since AppleScript references the file on disk instead of requiring you to read and embed its encoded bytes as a literal parameter:
```applescript
tell newMessage
	make new attachment with properties {file name:(POSIX file "/path/to/file.docx" as alias)} at after the last paragraph
end tell
```
Add this inside the same `tell newMessage` block as the recipients, before the `tell` block ends. Still deliver the recap doc to Kyle directly via `SendUserFile` too, so he has it standalone regardless of which draft it ends up attached to.

## Golden rules learned the hard way (apply project-wide, not just this flow)

1. **Every BT modal can re-render mid-interaction.** The pattern is: open → renders small/incomplete → 1-2s later resizes/repositions to final layout. Screenshot AFTER the resize settles, get fresh refs, THEN fill fields. Filling immediately on open is the #1 cause of wiped inputs across this entire flow (job address, invoice title, invoice date all hit this).
2. **Prefer `ref`-based clicks over raw coordinates** everywhere in BT — the app's layout shifts pixel positions between renders of the "same" screen (viewport can literally report different dimensions turn to turn), so coordinates that worked one screenshot ago silently miss on the next.
3. **Escape is dangerous in BT edit modals** — it's frequently bound to "attempt to close/exit" rather than "close this one popup," surfacing an Unsaved-changes confirmation you then have to navigate out of. Close date pickers and dropdowns by clicking their selection or clicking elsewhere in the form, not Escape.
4. **Never click a native file-picker trigger** ("Browse device" or similar) — always `find` the underlying `<input type=file>` and drive it with `file_upload`.
5. **Don't fight a field that silently refuses typed input after 2 clean attempts** — try once more via `ref` instead of coordinates, and if it still doesn't stick, route the same information into a nearby field that clearly does work (e.g. Invoice description instead of Internal notes) rather than burning many turns on one stubborn textbox.

## Report back

One message: job name + link, client name/contact captured, invoice total and confirmation it matches the source doc exactly (or the tax-rate-fix note if not), payment recorded, files attached where. Then: draft email created (recipients, not sent), recap doc delivered to Kyle. Flag anything you couldn't verify (e.g. a field that wouldn't save) so Kyle can spot-check it in BT directly. Start with "ok kyle" per global rules, colons not em dashes.

## Where this skill lives and how it stays in sync

`~/.claude/skills/bt-design-client-kickoff` and `~/.claude/skills/bt-new-client` are **symlinks** into `~/nss-org-repo/skills/` — that repo (github.com/noblesolidsurface-lang/NSS-ORG) is the actual source of truth, not the `.claude/skills` folder. Editing the skill through Claude Code edits the real file in the repo automatically because of the symlink — no extra copy step needed.

**Pushing is automatic**, not something to remember to do by hand: a LaunchAgent (`com.nss.autopushskills`, defined in `~/Library/LaunchAgents/com.nss.autopushskills.plist`) runs `~/nss-org-repo/auto_push_skills.sh` every 10 minutes. That script checks for uncommitted changes in the repo and, if there are any, commits and pushes them to GitHub on its own. If you edit this skill and want the push to happen immediately instead of waiting up to 10 minutes, just run the script directly: `bash ~/nss-org-repo/auto_push_skills.sh`. Check `~/nss-org-repo/auto_push.log` to confirm a push went through.

