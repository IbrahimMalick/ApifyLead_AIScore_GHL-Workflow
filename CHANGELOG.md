# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-30

### Added
- Initial public release of the **Apify → AI Score → GoHighLevel** n8n workflow.
- Importable workflow JSON (`workflows/`).
- Documentation: `README.md`, `docs/SETUP.md`, `docs/CUSTOMIZATION.md`.
- `.env.example` documenting all required environment variables.
- Community files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- GitHub issue & pull-request templates.
- CI workflow (`.github/workflows/validate.yml`) that validates the workflow JSON
  and scans for leaked secrets.
- `scripts/validate_workflow.py` validator.
- MIT `LICENSE`.

### Security
- Replaced all hardcoded credentials (Apify token, GHL bearer token, GHL location
  id, Google Sheet id, n8n instance id) with `{{$env.*}}` references and
  placeholders.
- Generalized the persona-specific `BRANDON_GOOGLE_SHEET_ID` variable to
  `GOOGLE_SHEET_ID`.

[1.0.0]: https://github.com/IbrahimMalick/ApifyLead_AIScore_GHL-Workflow/releases/tag/v1.0.0
