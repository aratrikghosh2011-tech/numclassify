# Security Policy

## Supported Versions

**Only the latest release on PyPI is supported.** There are no backports or
patch releases for older versions. Always upgrade to the newest version before
reporting an issue.

```bash
pip install --upgrade numclassify
```

| Version | Supported |
|---------|-----------|
| Latest (0.4.x) | ✅ |
| Any older version | ❌ |

## Reporting a Vulnerability

To report a security vulnerability, email **aratrikghosh2011@gmail.com** with
the subject line `[numclassify] Security Report`.

Please include:
- A clear description of the vulnerability
- Steps to reproduce it
- The version you are using (`python -c "import numclassify; print(numclassify.__version__)"`)
- Potential impact

You can expect an acknowledgment within 48 hours.

## Scope

`numclassify` is a pure computation library. It has:
- No network access
- No file system writes
- No external dependencies (stdlib only)
- No execution of user-supplied code

The attack surface is therefore very small. Realistic vulnerabilities are
limited to algorithmic issues such as infinite loops or excessive memory use
on crafted inputs (e.g. extremely large integers). If you find such an issue,
please report it — especially if it can be triggered via the public API.

## Out of Scope

- Vulnerabilities in Python itself or the standard library
- Issues requiring physical access to the machine
- Theoretical attacks with no practical exploit path
