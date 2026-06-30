# Customization Guide

This workflow ships with example values aimed at one use case (a US-based
appointment-setting business targeting agencies & SaaS). Everything below is
yours to change — here's where to look.

## 1. Who you're targeting (the AI prompt)

Node: **Message a model**

The system + user prompts define your ideal customer profile, the offer, and the
scoring rules. Edit them to describe *your* business:

- **Offer** — what you sell and the entry package.
- **Ideal prospects** — the industries/sizes you want.
- **Scoring rules** — what 9–10 vs 1–4 means for you.
- **Output keys** — keep the JSON keys in sync with the *Parse AI JSON* node if
  you add or rename fields.

> The model is set to `gpt-4o-mini` for cost. Swap it for a stronger model in the
> same node if you want better reasoning.

## 2. The qualification threshold

Node: **Lead Score >= 7?**

Change the `value2` (default `7`) to raise or lower the bar for pushing to GHL.
The *Parse AI JSON* node uses the same `>= 7` cut-off to set status/tags — update
both if you change it.

## 3. Branding: source label & tags

Several nodes contain example branding you'll want to replace:

| What | Where | Example value |
|---|---|---|
| Source label | *Normalize*, *Parse AI JSON*, *Upsert to GHL* | `AI Lead Research - Brandon Apify` |
| "Qualified" tags | *Parse AI JSON* (`fixedQualifiedTags`) | `brandon-ai-lead`, `brandon-apify`, … |
| "Review" tags | *Parse AI JSON* (`fixedReviewTags`) | `…`, `review-needed` |

Find-and-replace the `brandon-*` tags and the source string with your own.

## 4. The scraper

Node: **Run Apify Actor - Get Leads**

- Point `APIFY_ACTOR_TASK_ID` at any Apify Actor task that returns business data.
- The request body (`searchStringsArray`, `maxCrawledPlacesPerSearch`, …) matches a
  Google-Maps-style scraper. If your Actor expects different inputs, edit the
  `jsonBody`.
- The *Normalize and Dedupe* node already reads many common field names
  (`organizationName`, `companyName`, `website`, `url`, …). Add more fallbacks in the
  `first(...)` calls if your Actor uses different keys.

## 5. The spreadsheet schema

The column list lives in the Google Sheets nodes and is documented in
[SETUP.md](SETUP.md). If you add a column, add it to:

1. the output object in **Normalize and Dedupe Apify Leads**, and
2. the sheet header row.

## 6. Trigger

The workflow uses a **Manual Trigger** for testing. For production, swap it for a
**Schedule Trigger** (e.g. daily) or a **Webhook** — just rewire the first
connection.

---

Tip: after any change, run the validator locally before committing:

```bash
python3 scripts/validate_workflow.py
```
