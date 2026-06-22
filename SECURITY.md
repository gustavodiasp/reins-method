# Security Policy

## Reporting a vulnerability

If you find a security vulnerability in REINS Method, **please do not open a public
issue**. Report it privately via GitHub's
[Security Advisories](https://github.com/gustavodiasp/reins-method/security/advisories/new)
feature.

Include:
- A description of the vulnerability
- Steps to reproduce
- The potential impact
- Any suggested fix (optional)

You will receive a response within 7 days. If the vulnerability is confirmed, a fix
will be prioritized and a new release published as soon as possible.

## Scope

REINS Method is a local CLI tool. It reads and writes files under `~/.reins/` and
wires into AI agent config files on the user's machine. It makes no network requests
beyond downloading its own releases from GitHub during `reins install` / `reins update`.

Out of scope: issues in third-party tools (graphify, headroom, the AI agents
themselves). Report those to their respective maintainers.
