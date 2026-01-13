# FinCorp Global — Safe-Chat Security Policy (Internal)

## Purpose
Safe-Chat is intended to improve productivity while protecting sensitive information.

## Prohibited inputs
Employees must not paste:
- Customer PII (e.g., SSNs, credit card numbers)
- Authentication secrets (API keys, passwords, tokens)
- Confidential contract language unless explicitly approved for internal tools

## Approved usage
- General conceptual questions (e.g., retirement plan comparisons)
- Internal process questions answered using approved KB documents
- Engineering questions (refactoring, troubleshooting), as long as proprietary secrets are excluded

## Guardrails expectations
- PII should be blocked outright to prevent data loss.
- Profanity may be redacted to keep model context clean while maintaining usability.

## Incident handling
If a prompt is blocked:
- User sees a security warning
- The event is logged for audit and follow-up