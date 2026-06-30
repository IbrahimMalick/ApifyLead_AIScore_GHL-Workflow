# Apify Lead Scrape → AI Score → GoHighLevel Workflow

An [n8n](https://n8n.io) automation that turns a single search query into qualified,
AI-scored sales leads inside [GoHighLevel](https://www.gohighlevel.com/) (GHL).

The workflow scrapes business leads with **Apify**, normalizes and de-duplicates
them, scores each one with an **OpenAI** model, logs everything to **Google
Sheets**, and pushes only the qualified leads into **GHL** as contacts with an AI
research note attached.

> Built for "Brandon", the owner of a US-based appointment-setting / sales-calling
> business, to research and qualify agency & SaaS prospects automatically.

---

## How it works

```
Manual Trigger
   │
   ▼
Set Apify Search ........... search query, target market, max results
   │
   ▼
Run Apify Actor – Get Leads  (HTTP → Apify run-sync-get-dataset-items)
   │
   ▼
Normalize & Dedupe Apify Leads  (Code) → maps messy scraper output to a clean schema
   │
   ▼
Append Scraped Leads to Google Sheet   (stages raw leads in the "Prospects" tab)
   │
   ▼
Message a model  (OpenAI GPT-4o-mini → scores 1–10 + research fields, JSON only)
   │
   ▼
Parse AI JSON  (Code) → merges AI output back onto each lead, builds GHL tags
   │
   ▼
Lead Score >= 7? ──── No ──► Append AI Scored Lead to Google Sheet  (review queue)
   │
  Yes
   │
   ▼
Upsert Qualified Lead to GHL   (creates/updates the GHL contact)
   │
   ▼
Add AI Research Note to GHL    (attaches the AI summary as a contact note)
   │
   ▼
Update Qualified Lead in Google Sheet  (writes back GHL contact id + "Pushed to GHL")
```

### Scoring rubric (used by the AI prompt)

| Score | Meaning |
|-------|---------|
| 9–10  | Strong agency/SaaS/company likely to need US appointment-setting or lead follow-up |
| 7–8   | Good fit — pushed to GHL automatically |
| 5–6   | Possible fit — routed to the review queue |
| 1–4   | Weak fit — local business, unclear company, or not relevant |

Only leads scoring **≥ 7** are pushed to GHL. Everything else is appended to the
sheet for manual review.

---

## Repository layout

```
.
├── workflows/
│   └── Exercise_1_Apify_Lead_Scrape_to_AI_Score_to_GHL.json   # the n8n workflow (importable)
├── docs/
│   └── SETUP.md                                               # step-by-step setup guide
├── .env.example                                               # required environment variables
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick start

1. **Import the workflow**
   In n8n: *Workflows → Import from File* → select
   `workflows/Exercise_1_Apify_Lead_Scrape_to_AI_Score_to_GHL.json`.

2. **Set environment variables**
   Copy `.env.example` to `.env`, fill in your real values, and expose them to n8n
   (see [`docs/SETUP.md`](docs/SETUP.md)). The workflow reads:
   - `APIFY_TOKEN`, `APIFY_ACTOR_TASK_ID`
   - `BRANDON_GOOGLE_SHEET_ID`
   - `GHL_API_TOKEN`, `GHL_LOCATION_ID`

3. **Connect credentials in n8n**
   - **Google Sheets** OAuth2
   - **OpenAI** API key

4. **Point the Google Sheets nodes at your spreadsheet**
   Replace the `YOUR_GOOGLE_SHEET_ID` placeholders (or use the `BRANDON_GOOGLE_SHEET_ID`
   variable) and make sure the sheet has a `Prospects` tab with the columns listed in
   [`docs/SETUP.md`](docs/SETUP.md).

5. **Run it**
   Edit *Set Apify Search* (search query + `maxResults`), then execute the workflow.

Full details are in **[docs/SETUP.md](docs/SETUP.md)**.

---

## Security

This repository ships **no live credentials**. Every secret is referenced through
n8n environment variables (`{{$env.*}}`) or n8n credentials. Before running:

- Keep your real `.env` out of git (already covered by `.gitignore`).
- If any token was ever committed or shared, **rotate it** (Apify token, GHL
  private token, OpenAI key).

---

## Tech stack

- **n8n** — workflow orchestration
- **Apify** — Google Maps / business lead scraping
- **OpenAI GPT-4o-mini** — lead scoring & research enrichment
- **Google Sheets** — staging + review queue + audit log
- **GoHighLevel (LeadConnector API)** — CRM destination

## License

Released under the [MIT License](LICENSE).
