# Security Policy

## Reporting a vulnerability

If you discover a security issue — including a **leaked credential** in the git
history — please report it privately rather than opening a public issue:

- Use GitHub's **[Report a vulnerability](../../security/advisories/new)** (Security → Advisories), or
- Email the maintainer.

Please include steps to reproduce and the impact. We aim to respond within a few days.

## Handling secrets

This project is designed to contain **no live credentials**:

- All tokens and IDs are referenced via n8n environment variables (`{{$env.*}}`)
  or n8n credentials.
- `.env` is git-ignored; only `.env.example` (placeholders) is committed.
- CI scans every push for common secret patterns (Apify tokens, GHL private
  tokens, OpenAI keys, etc.).

### If you exposed a token

1. **Rotate it immediately** at the provider (Apify, GoHighLevel, OpenAI, Google).
2. Remove it from the working tree and history if needed.
3. Confirm CI's secret scan passes.

Rotating is always safer than trying to "scrub" a secret that has already been pushed.
