# FinCorp Engineering — Refactoring Guide (Internal)

## Principles
- Prefer small, safe changes over big rewrites
- Improve readability and test coverage as you go
- Keep behavior identical while changing structure

## Common refactoring moves
- Extract function / method
- Rename variables to express intent
- Reduce nested conditionals
- Add characterization tests before refactoring legacy code

## Suggested workflow
1) Add tests (even minimal) to lock behavior
2) Identify the most painful function/module
3) Make one small refactor
4) Re-run tests
5) Repeat