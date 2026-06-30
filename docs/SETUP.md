# Setup Guide

This guide walks through configuring the **Apify Lead Scrape → AI Score → GHL**
workflow from a fresh n8n instance.

## 1. Prerequisites

| Service | What you need |
|---------|---------------|
| [n8n](https://n8n.io) | Self-hosted or cloud instance (workflow uses the Code, HTTP Request, Set, IF, Google Sheets and LangChain OpenAI nodes) |
| [Apify](https://apify.com) | Account + API token + a configured lead-scraper **Actor task** |
| [OpenAI](https://platform.openai.com) | API key with access to `gpt-4o-mini` |
| [Google Sheets](https://sheets.google.com) | A spreadsheet with a `Prospects` tab |
| [GoHighLevel](https://www.gohighlevel.com) | A location/sub-account + a Private Integration Token |

## 2. Import the workflow

1. In n8n, open **Workflows → Import from File**.
2. Select `workflows/Exercise_1_Apify_Lead_Scrape_to_AI_Score_to_GHL.json`.
3. Save the workflow.

## 3. Environment variables

Copy the example file and fill in real values:

```bash
cp .env.example .env
```

| Variable | Used by | Description |
|----------|---------|-------------|
| `APIFY_TOKEN` | Run Apify Actor node | Apify API token |
| `APIFY_ACTOR_TASK_ID` | Run Apify Actor node | Actor task id, e.g. `username~leads-scraper-for-brandon` |
| `BRANDON_GOOGLE_SHEET_ID` | Append AI Scored Lead node | Target spreadsheet id |
| `GHL_API_TOKEN` | GHL Upsert / Note nodes | GHL Private Integration Token (Bearer) |
| `GHL_LOCATION_ID` | GHL Upsert node | GHL location / sub-account id |

> n8n only exposes host environment variables to `{{$env.*}}` when
> `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` (the default). For n8n Cloud, set these
> under **Variables** instead and reference them accordingly.

After editing `.env`, restart n8n (or export the variables in its environment) so
the `{{$env.*}}` expressions resolve.

## 4. Credentials inside n8n

Create these under **Credentials**:

1. **Google Sheets OAuth2** — used by the three Google Sheets nodes.
2. **OpenAI API** — used by *Message a model*.

Re-select your credentials on each node after import (imported workflows keep the
original credential *names* but must be re-linked to your account).

## 5. Prepare the Google Sheet

Create a tab named **`Prospects`** with these column headers (row 1), in order:

```
Prospect ID, Company Name, Website, Country, State/Region, Company Size,
Target Market, Services Offered, Decision Maker Name, Decision Maker Title,
LinkedIn URL, Email, Phone, Why They Are a Fit, Pain Point,
Personalized Opening Line, Suggested Pitch, Lead Score, Status, Next Step,
GHL Tags, GHL Contact ID, Notes, Source, Apify Run ID, Address, City,
Category, Google Maps URL, Rating, Reviews Count, Duplicate Check Key
```

Then update the Google Sheets nodes so they point at your spreadsheet
(replace the `YOUR_GOOGLE_SHEET_ID` placeholder with your real id, or wire the
`BRANDON_GOOGLE_SHEET_ID` variable).

## 6. Configure GHL

- Generate a **Private Integration Token** for your location and set it as
  `GHL_API_TOKEN`.
- Set `GHL_LOCATION_ID` to your sub-account id.
- The workflow calls:
  - `POST /contacts/upsert` — create/update the contact
  - `POST /contacts/{id}/notes` — attach the AI research summary
- Confirm any **required custom fields** and duplicate-handling settings in your
  GHL location before running.

## 7. Run

1. Open **Set Apify Search** and set:
   - `searchQuery` (e.g. `digital marketing agencies in Florida`)
   - `maxResults` (keep low while testing)
2. Click **Execute Workflow**.
3. Check:
   - the `Prospects` sheet for staged + scored rows,
   - GHL for new/updated contacts with the AI note,
   - rows with score `< 7` stay in the review queue.

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| `Could not find AI JSON in OpenAI node output` row marked *review needed* | Model returned non-JSON; the *Parse AI JSON* node falls back to a manual-review record |
| Apify 401 / 403 | Bad `APIFY_TOKEN` or wrong `APIFY_ACTOR_TASK_ID` |
| GHL 401 | Bad `GHL_API_TOKEN` or expired Private Integration Token |
| Wrong GHL contact id in the note URL | Adjust the id path in *Add AI Research Note to GHL* (`$json.contact?.id || $json.id`) |
| Duplicate rows for qualified leads | Expected: scraped row is appended, then updated by `Prospect ID` after GHL push |

## Notes & known limitations

- **De-duplication is per-run only.** The *Normalize and Dedupe* node de-dupes
  within a single execution; it does not check existing sheet rows.
- The *Append AI Scored Lead to Google Sheet* node is the review-queue branch
  (score `< 7`); qualified leads are updated in place by `Prospect ID`.
