# Contributing

Thanks for your interest in improving this project! 🎉

## Ways to contribute

- 🐛 **Report bugs** or unexpected behavior via [issues](../../issues).
- 💡 **Suggest features** or improvements.
- 📖 **Improve the docs** (setup steps, troubleshooting, customization).
- 🔧 **Submit fixes** to the workflow or tooling.

## Workflow changes

The workflow lives in `workflows/Exercise_1_Apify_Lead_Scrape_to_AI_Score_to_GHL.json`
and is edited inside n8n, then exported.

1. Import the JSON into your own n8n instance.
2. Make your change.
3. **Export** the workflow (*⋯ → Download*) back over the same file.
4. **Remove any real credentials** before committing — use `{{$env.*}}`
   expressions or n8n credentials, never hardcoded tokens.
5. Validate locally:
   ```bash
   python3 scripts/validate_workflow.py
   ```

## Pull request checklist

- [ ] No secrets, tokens, API keys, or private IDs in the diff.
- [ ] `python3 scripts/validate_workflow.py` passes.
- [ ] Docs updated if behavior or setup changed.
- [ ] Clear, descriptive commit messages and PR description.

## Code of conduct

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
