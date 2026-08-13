# BT Estimate Line Item: Design Retainer

The design phase line item that goes on the job's Estimate in BuilderTrend right after the ROM job is created. Mirrors Kyle's Joist design retainer invoice (Howe example).

## Line item fields

| BT field | Value |
|---|---|
| Title | Design Retainer |
| Cost Code | design/office code if one exists in the picker, else ask Kyle once and remember |
| Cost Type | Other |
| Quantity | 1, Unit: ls |
| Unit Cost | {{retainer_amount}} |
| Markup | none (client price = retainer) |
| Description | the block below, customized |

## Description block ({{placeholders}} customized per job)

NSS HOME — DESIGN PROCESS
{{project_title}} — {{property_address_short}}

NSS will work alongside your designer to furnish construction documents for the {{project_title_lowercase}} at {{property_address_short}}. Scope includes {{scope_description}}.

BILLING
Design is billed as a retainer, drawn down at $150 per hour for design and drafting time. Specialized consultants — septic, structural, architectural review, municipal plan review — bill against the retainer at actual cost. Any balance left at the end of design is credited to your build.

THE PROCESS
1. Measure Meeting: Full field measure on site. We document existing conditions and work through how each space needs to function.
2. Design & Redline: Plans are drafted, then refined until the drawings match the intent. Every redline is resolved between drafter, designer, and engineer, and updated on the plan.
3. Selections: Every finish, fixture, cabinet, floor, light, and piece of millwork is chosen and documented on a spec sheet, so pricing reflects what's actually going in the building.
4. Budget Check-In: Before trades price the job, we review the design against your budget. Adjustments happen here, on paper, where they're cheap.
5. Trades Day: Nothing gets priced on guesswork. All subs walk the site with our team against finished plans and confirm scope and pricing on the spot.
6. Fixed Cost Final Proposal: Plans complete, selections locked, trades priced. You get a 100% accurate, fixed-cost proposal with minimal allowances standing in for real numbers.

YOUR DELIVERABLES
Complete Spec/Selection Sheet
Final Construction Documents with renderings (if required/requested), all redlines resolved
Electrical/MEP Permit Secured
Permit-Ready Plans for Submittal
Fixed-Cost Build Proposal

## BT flow to add it

1. Open the job (Jobs sidebar → click the ROM job), then navigate to `https://buildertrend.net/app/Estimate` (loads the estimate for the currently selected job: verify the job name in the top-left before touching anything).
2. Click "Add Item" (find by ref). Fill Title, Cost Type, Qty/Unit, Unit Cost by ref-click + type. Paste the description block into Description.
3. Set Markup to none/0 so Client Price = retainer amount.
4. Save the item (cmd+s or the item's Save button by ref), screenshot to verify the line and total.
5. Do NOT send anything to the client and do NOT "Send to Budget": the estimate just holds the design phase line item at ROM stage.
