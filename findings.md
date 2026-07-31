# Secure Coding Review — Findings Report

**Project reviewed:** Sample Python user-authentication app (`vulnerable_app.py`)
**Reviewer:** Shivani Mandoliya
**Method:** Manual code inspection + static analysis (`bandit`)
**Date:**31 July 2026

---

## Summary
This report documents a manual and automated security review of a small Python
application handling user login and file access. 5 vulnerabilities were identified,
ranging from High to Medium risk. Fixes for each are implemented in `fixed_app.py`.

---

## Findings

| ID | Vulnerability | Risk | Location |
|----|---------------|------|----------|
| VULN-1 | Hardcoded credentials/secret key | High | `SECRET_KEY`, `DB_PASSWORD` |
| VULN-2 | SQL Injection via string concatenation | High | `login()` |
| VULN-3 | Passwords stored in plain text | High | `save_password()` |
| VULN-4 | Path traversal — no input validation on file reads | Medium | `read_user_file()` |
| VULN-5 | Sensitive data exposed in logs | Medium | `debug_log()` |

---

### VULN-1: Hardcoded Credentials
**Issue:** Secret key and DB password are hardcoded directly in source code.
**Risk:** Anyone with repo access (or a leaked commit) gets full credentials.
**Fix:** Load secrets from environment variables (`os.environ.get(...)`) or a
secrets manager. Never commit `.env` files — add to `.gitignore`.

### VULN-2: SQL Injection
**Issue:** `login()` builds a SQL query by directly concatenating user input.
An attacker can input `' OR '1'='1` as the password to bypass authentication.
**Risk:** Full authentication bypass, data theft, or database manipulation.
**Fix:** Use parameterized queries (`?` placeholders) so the DB driver
escapes input automatically — implemented in `fixed_app.py`.

### VULN-3: Plain-Text Password Storage
**Issue:** Passwords saved directly to the database with no hashing.
**Risk:** A single database leak exposes every user's real password.
**Fix:** Hash passwords with `bcrypt` before storing; compare using
`bcrypt.checkpw()` at login — never decrypt or store the original password.

### VULN-4: Path Traversal
**Issue:** `read_user_file()` opens any filename passed to it, with no
validation — e.g. `"../../etc/passwd"` would work.
**Risk:** Attacker can read arbitrary files on the server.
**Fix:** Validate input against a whitelist of allowed filenames before
opening. For real-world apps, also resolve the absolute path and check it
stays within an allowed base directory.

### VULN-5: Sensitive Data in Logs
**Issue:** `debug_log()` prints full user data, including plaintext passwords,
to the console/logs.
**Risk:** Logs are often stored insecurely or shipped to third-party log
aggregators — this leaks credentials outside the app.
**Fix:** Mask sensitive fields (password, secret, token) before logging.

---

## Tools Used
- **Manual review** — line-by-line inspection for common OWASP Top 10 issues
  (Injection, Broken Authentication, Sensitive Data Exposure).
- **Bandit** (static analyzer for Python):
  ```bash
  pip install bandit
  bandit -r vulnerable_app.py
  ```
  Bandit flags the hardcoded secrets (B105/B106) and SQL injection pattern
  (B608) automatically, confirming the manual findings.

## Recommendations Going Forward
1. Never hardcode secrets — use environment variables or a vault.
2. Always use parameterized queries for any database interaction.
3. Hash passwords with bcrypt/argon2 — never store or log them in plain text.
4. Validate and whitelist all user-supplied input, especially file paths.
5. Run `bandit` (or similar SAST tools) as part of CI/CD before merging code.

---
