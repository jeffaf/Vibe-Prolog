# ISO Prolog Conformity Testing Results

> **Last Updated**: 2025-12-05 20:50:45
> **Test Suite**: ISO/IEC JTC1 SC22 WG17
> **Source**: https://www.complang.tuwien.ac.at/ulrich/iso-prolog/conformity_testing
> **Total Tests**: 10

## Summary

- **Passed**: 5 (50.0%)
- **Syntax Errors**: 0 (0.0%)
- **Type Errors**: 0 (0.0%)
- **Other Errors**: 5 (50.0%)

## Results by Category

### Character Escapes (Tests 1-10)

- Passed: 5/10 (50.0%)

## Detailed Results

| Test # | Query | Status | Error |
|--------|-------|--------|-------|
| 1 | `writeq('\n').` | OK |  |
| 2 | `'` | EXCEPTION | error(syntax_error(No terminal matches ''' in t... |
| 3 | `)` | EXCEPTION | error(syntax_error(No terminal matches ')' in t... |
| 4 | `)'` | EXCEPTION | error(syntax_error(No terminal matches ')' in t... |
| 5 | `.` | EXCEPTION | error(syntax_error(Unexpected end-of-input. Exp... |
| 6 | `writeq(' ').` | OK |  |
| 7 | `0'\t=0' .` | EXCEPTION | error(syntax_error(No terminal matches ''' in t... |
| 8 | `writeq('\n').` | OK |  |
| 9 | `writeq('\\n').` | OK |  |
| 10 | `writeq('\\na').` | OK |  |

## Known Issues

[Automatically populated list of failing tests with their error messages]

## Regenerating This Report

```bash
uv run python tools/conformity_test.py --output docs/CONFORMITY_TESTING.md
```
