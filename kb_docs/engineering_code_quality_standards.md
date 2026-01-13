# FinCorp Engineering — Code Quality Standards (Internal)

## Baseline expectations
- Functions should have a single responsibility
- Avoid hidden side effects and global state
- Prefer clear naming over cleverness
- Logging should not contain secrets or PII

## Reviews
- PRs should be small enough to review in <30 minutes when possible
- Include context: why the change is needed

## AI usage
- Do not paste customer data or production secrets into AI prompts
- Use Safe-Chat for conceptual guidance and approved internal docs