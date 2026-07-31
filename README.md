# CodeAlpha_SecureCodingReview

## 📌 Task
Secure Coding Review — **CodeAlpha Cyber Security Internship (Task 3)**.
A manual + automated security review of a sample Python application, identifying
common vulnerabilities and providing fixed, remediated code.

## 📂 Files
- `vulnerable_app.py` — Sample app with 5 intentional vulnerabilities (labeled `[VULN-x]`)
- `fixed_app.py` — Same app, remediated (labeled `[FIX-x]`)
- `findings.md` — Full report: risk levels, explanations, and recommendations

## 🛠 Tools Used
- Manual code inspection (OWASP Top 10 lens)
- [`bandit`](https://bandit.readthedocs.io/) — Python static security analyzer

## ▶️ How to Run the Review Yourself

1. Install bandit:
   ```bash
   pip install bandit
   ```
2. Run it against the vulnerable file:
   ```bash
   bandit -r vulnerable_app.py
   ```
   You'll see it flag hardcoded secrets and injection risks automatically.
3. Compare against `fixed_app.py` — run bandit on it too, findings should be gone
   (bcrypt import will need `pip install bcrypt` first).

## 🔍 Key Vulnerabilities Found
1. Hardcoded credentials/secret key
2. SQL Injection (string-concatenated queries)
3. Plain-text password storage
4. Path traversal (no input validation on file reads)
5. Sensitive data exposed in logs

Full details, risk ratings, and fixes → see [`findings.md`](./findings.md).

## 👤 Author
Shivani Mandoliya — CodeAlpha Cyber Security Intern
