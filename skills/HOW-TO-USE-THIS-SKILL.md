# Using the "design client kickoff" skill in Claude — a beginner's guide

Hi Lacy and Crystal — this is for you. A "skill" is just a saved set of instructions that Claude follows automatically when you ask it to do a certain job. You don't need to know how it works inside, you just need to know how to install it once and how to ask for it.

## Part 1: One-time setup (only do this once, ever)

**Step 1 — Make sure you have Claude Code.**
This only works inside **Claude Code** (the version that can click around in a browser and fill out websites for you), not the regular claude.ai website chat. If you're not sure whether you have it, or how to open it, ask Kyle — this is a five-minute setup he can walk you through once.

**Step 2 — Find (or create) your skills folder.**
On your computer, open **Finder**, then:
1. Click **Go** in the top menu bar, then **Go to Folder…**
2. Type exactly: `~/.claude/skills` and press Return.
3. If a folder opens showing a bunch of other skill folders, great — you're in the right place.
4. If you get an error saying it doesn't exist, type `~/.claude` instead, press Return, and create a new folder inside it named exactly `skills` (all lowercase). Then go back into that new folder.

**Step 3 — Unzip the file Kyle sent you.**
Double-click the zip file. It'll create two folders: `bt-design-client-kickoff` and `bt-new-client`. Drag **both** of these folders into the `~/.claude/skills` folder from Step 2. You need both — the first one relies on the second.

**Step 4 — Restart Claude Code.**
Fully quit it and reopen it (or just start a brand new conversation). This is what makes it notice the new skill exists.

**Step 5 — Make sure the browser piece is connected.**
This skill needs to click around inside BuilderTrend for you, which means Claude needs the **Claude-in-Chrome** browser extension installed and you need to already be logged into buildertrend.net in that browser. If you've never set this up, ask Kyle — again, a one-time thing.

That's it for setup. You never have to touch the skill files again.

## Part 2: How to actually use it, every time

**You don't need to remember any special command or skill name.** Just tell Claude what you want in your own words, like you're texting a coworker:

> "New design client, Jane Smith, just signed and paid the retainer — set up her job in BuilderTrend and draft the handoff email."

Claude recognizes this and pulls in the right instructions automatically.

**Before you ask, have the client's stuff ready to hand over.** Whatever exists — the signed Joist paperwork, meeting notes, a Canva proposal, a screenshot of the payment going through. Paste it all into the chat first, or just tell Claude "it's in [wherever]." The more it has up front, the less it has to guess or ask you about.

**Then just watch.** A browser window will open and you'll see Claude clicking through BuilderTrend live — creating the job, typing in the client's info, building the invoice. This is completely normal, even if it looks like it's double-checking itself or clicking the same thing twice. Let it work; don't click into that browser window yourself while it's running, since that can confuse it mid-click.

## Part 3: What to check before anything goes out

Claude will **never send an email on its own** in this workflow — it only ever creates a draft and stops. Two things it'll hand you to look over:

1. **Does the invoice total match the original paperwork?** If Claude flags a small mismatch (usually a tax-rounding thing), it fixes it itself and tells you it did — you don't need to do anything except glance at the final number.
2. **Read the draft email before sending it.** Claude writes a strong first draft, but it doesn't know things you or Kyle know off the top of your head — like which vendor you actually use for a certain category, or a construction detail that never made it into the meeting notes. Treat the draft as 90% done, not 100%. Add anything it's missing, cut anything that reads like it's talking to the wrong person (an email meant for the designer shouldn't have internal-only notes in it).

## When something looks off

Don't try to fix it by hand in BuilderTrend first. Just tell Claude what looks wrong, right there in the same chat — like "the phone number's wrong" or "that invoice should be $200 higher." It knows exactly what it just did and can correct it faster and more safely than editing it directly yourself.

## Quick reference

| You want to... | Do this |
|---|---|
| Install the skill (once) | Unzip → drag both folders into `~/.claude/skills` → restart Claude Code |
| Start a new client kickoff | Just describe it in plain English in a new Claude Code chat |
| Check on progress | Watch the browser window, no action needed |
| Approve something | Read the draft email / final numbers before you or Kyle hit send |
| Fix a mistake | Tell Claude in chat, don't edit BuilderTrend by hand first |
